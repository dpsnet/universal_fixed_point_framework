# -*- coding: utf-8 -*-
"""从 HEAD 恢复论文工作区文件（二进制安全），并备份当前工作区版本。"""
import hashlib, io, os, shutil, subprocess, time

GIT = r"D:\apps\Git\cmd\git.exe"
REPO = r"E:\workspace\hyper-resolution"
REL = "universal_fixed_point_framework/paper/paper_SM_endogenous_derivation.md"
ABS = os.path.join(REPO, REL)
TS = time.strftime("%Y%m%d_%H%M%S")
BAK = os.path.join(os.environ["TEMP"], "paper_work_backup_%s.md" % TS)

# 1. 备份
shutil.copyfile(ABS, BAK)
print("BACKUP ->", BAK)
print("WORK bytes=%d md5=%s" % (os.path.getsize(ABS), hashlib.md5(open(ABS,'rb').read()).hexdigest()))

# 2. 取 HEAD blob 原始字节
blob = subprocess.run([GIT, "-C", REPO, "cat-file", "blob", "HEAD:" + REL],
                      capture_output=True).stdout
print("HEAD blob bytes=%d md5=%s" % (len(blob), hashlib.md5(blob).hexdigest()))

# 3. 写回
with open(ABS, "wb") as f:
    f.write(blob)

# 4. 校验：与 git hash-object 一致
ho = subprocess.run([GIT, "-C", REPO, "hash-object", REL],
                    capture_output=True, text=True).stdout.strip()
blobhash = subprocess.run([GIT, "-C", REPO, "rev-parse", "HEAD:" + REL],
                          capture_output=True, text=True).stdout.strip()
print("hash-object=", ho)
print("HEAD blob    =", blobhash)
print("MATCH=", ho == blobhash)
t = blob.decode("utf-8")
print("lines=", t.count("\n") + 1)
print("has_origin_narrative=", "框架起源——从脉冲神经网络" in t)
print("has_branchA=", "分支 A（活跃步）" in t)
print("has_jobs_retract=", "v1.3 撤回 7096 口径" in t)
