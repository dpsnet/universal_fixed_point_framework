# -*- coding: utf-8 -*-
"""R3h：DESI coadd FITS 按需读取器（HTTP Range / 本地文件两用）v7
- 正确解析多块 header（读到 END 卡为止）
- BINTABLE 列偏移：TBCOL 缺失时按 TFORM 宽度累计
- image 行读取：B_FLUX[row]
验证：本地 7110 文件对照 astropy"""
import numpy as np
import requests
import os

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

class DesiCoadd:
    def __init__(self, src):
        self.src = src
        self._local = os.path.isfile(src) if isinstance(src, str) else False
        self._buf = None
        if self._local:
            with open(src, "rb") as f:
                self._buf = f.read()
        self.hdus = []
        self._parse()

    def _read_bytes(self, offset, length):
        if self._local:
            b = self._buf[offset:offset + length]
            if len(b) < length:
                raise EOFError("short read at %d" % offset)
            return b
        r = requests.get(self.src, headers=dict(UA, Range="bytes=%d-%d" % (offset, offset + length - 1)), timeout=60)
        if r.status_code == 206:
            return r.content
        raise IOError("range fail %s %s" % (r.status_code, r.text[:80]))

    def _read_header(self, off):
        """从 off 读一个 HDU 的完整 header（含 END 卡），返回 (cards, order, nblocks)"""
        cards = {}
        order = []
        nblocks = 0
        while True:
            buf = self._read_bytes(off + nblocks * 2880, 2880)
            nblocks += 1
            for i in range(0, 2880, 80):
                c = buf[i:i + 80].decode("ascii", "replace")
                if c.startswith("END"):
                    return cards, order, nblocks
                k = c[:8].strip()
                if k:
                    cards[k] = c[10:].strip()
                    order.append(k)

    def _parse(self):
        off = 0
        try:
            while True:
                cards, order, nblocks = self._read_header(off)

                def get(key, default=None):
                    v = cards.get(key, default)
                    if v is None:
                        return None
                    v = v.split(" / ")[0].strip()
                    if v.startswith("'") and v.endswith("'"):
                        v = v[1:-1].strip()
                    return v

                xt = get("XTENSION", get("SIMPLE", "F"))
                dlen = 0
                shape = None
                bps = 1
                ttypes = {}
                name = get("EXTNAME", get("HDUNAME", str(len(self.hdus))))
                if name.startswith("'") and name.endswith("'"):
                    name = name[1:-1].strip()
                if xt == "BINTABLE":
                    naxis2 = int(get("NAXIS2", "1") or 1)
                    naxis1 = int(get("NAXIS1", "0") or 0)
                    pcount = int(get("PCOUNT", "0") or 0)
                    gcount = int(get("GCOUNT", "1") or 1)
                    dlen = (naxis1 * naxis2 + pcount) * gcount
                    shape = naxis2
                    def tf_width(tf):
                        import re
                        m = re.match(r"(\d*)([A-Za-z])", tf.strip())
                        rep = int(m.group(1) or 1)
                        code = m.group(2)
                        base = {"B": 1, "I": 2, "J": 4, "K": 8, "E": 4, "D": 8, "A": 1, "L": 4, "C": 8, "M": 16}.get(code, 4)
                        return rep * base

                    colinfos = []
                    for k in order:
                        if k.startswith("TTYPE"):
                            col = k[5:]
                            tf = get("TFORM" + col, "?")
                            colinfos.append((int(col), cards[k].strip("'").strip(), tf,
                                             get("TBCOL" + col, "")))
                    colinfos.sort(key=lambda x: x[0])
                    off2 = 1
                    for cnum, cname, tf, tbcol in colinfos:
                        if tbcol:
                            off2 = int(tbcol)
                        ttypes[cname] = (str(cnum), tf, off2)
                        off2 += tf_width(tf)
                else:
                    bitpix = int(get("BITPIX", "8"))
                    bps = abs(bitpix) // 8
                    naxis = int(get("NAXIS", "0") or 0)
                    shape = []
                    for a in range(naxis, 0, -1):
                        shape.append(int(get("NAXIS%d" % a, "1") or 1))
                    items = int(np.prod(shape)) if shape else 0
                    dlen = items * bps
                    if naxis == 0:
                        shape = None
                data_off = off + nblocks * 2880
                self.hdus.append(dict(name=name, kind=xt, off=data_off, dlen=dlen,
                                      shape=shape, bps=bps, ttypes=ttypes,
                                      naxis1=int(get("NAXIS1", "0") or 0) if xt == "BINTABLE" else None))
                off = data_off
                if dlen:
                    off += (dlen + 2879) // 2880 * 2880
        except (EOFError, IOError):
            pass

    def hdu(self, name):
        for h in self.hdus:
            if h["name"].upper() == name.upper():
                return h
        return None

    def col(self, hdu_name, colname):
        h = self.hdu(hdu_name)
        t = h["ttypes"].get(colname)
        if t is None:
            raise KeyError("no col %s in %s (%s)" % (colname, hdu_name, list(h["ttypes"])))
        colnum, tform, tbcol = t
        code = tform[0]
        dt = {"B": "u1", "I": ">i2", "J": ">i4", "K": ">i8", "E": ">f4", "D": ">f8", "L": ">i4"}.get(code, ">f4")
        nrows = h["shape"]
        naxis1 = h.get("naxis1") or np.dtype(dt).itemsize
        itemsize = np.dtype(dt).itemsize
        if naxis1 == itemsize:
            off = h["off"] + (tbcol - 1)
            b = self._read_bytes(off, nrows * itemsize)
            return np.frombuffer(b, dtype=dt, count=nrows)
        # 多列表：读整个表数据区，按行宽步进取列字节
        b = self._read_bytes(h["off"], nrows * naxis1)
        arr = np.frombuffer(b, dtype=np.uint8).reshape(nrows, naxis1)
        colb = arr[:, tbcol - 1: tbcol - 1 + itemsize].tobytes()
        return np.frombuffer(colb, dtype=dt, count=nrows)

    def image_row(self, name, row):
        h = self.hdu(name)
        shape, bps = h["shape"], h["bps"]
        nrow, ncol = shape
        off = h["off"] + row * ncol * bps
        b = self._read_bytes(off, ncol * bps)
        dt = {4: ">f4", 8: ">f8"}.get(bps)
        return np.frombuffer(b, dtype=dt, count=ncol)

    def image_all(self, name):
        h = self.hdu(name)
        shape, bps = h["shape"], h["bps"]
        items = int(np.prod(shape))
        b = self._read_bytes(h["off"], items * bps)
        dt = {4: ">f4", 8: ">f8"}.get(bps)
        return np.frombuffer(b, dtype=dt, count=items).reshape(shape)


if __name__ == "__main__":
    BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
    local = os.path.join(BASE, "_desi_spec", "coadd-main-bright-7110.fits")
    d = DesiCoadd(local)
    for i, h in enumerate(d.hdus):
        print(i, h["name"], h["kind"], "off", h["off"], "shape", h["shape"])
    tid = d.col("FIBERMAP", "TARGETID")
    print("TARGETID[0:6]", tid[:6], "dtype", tid.dtype)
    # 只对照前 8 行
    from astropy.io import fits
    with fits.open(local, memmap=True) as hdul:
        t = hdul["FIBERMAP"].data
        print("astropy TARGETID[0:6]", t["TARGETID"][:6])
        print("match:", np.array_equal(tid, t["TARGETID"]))
        w = d.image_all("B_WAVELENGTH")
        f = d.image_row("B_FLUX", 0)
        wref = np.asarray(hdul["B_WAVELENGTH"].data)
        fref = np.asarray(hdul["B_FLUX"].data)[0]
        print("wave len", len(w), "match:", np.allclose(w, wref))
        print("flux match:", np.allclose(f, fref, equal_nan=True))
