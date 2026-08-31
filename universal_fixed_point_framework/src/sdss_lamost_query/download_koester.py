"""
尝试下载 Koester 白矮星模型大气网格
多个下载源尝试
"""
import os
import urllib.request
import ssl

# 禁用 SSL 验证（某些镜像可能需要）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

MODEL_DIR = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\data\koester_models"
os.makedirs(MODEL_DIR, exist_ok=True)

# 可能的下载源
URLS = [
    # 基尔大学官方
    "https://www.astro.physik.uni-kiel.de/kds/koester_models/da/da_model_grid.fits",
    "http://www.astro.physik.uni-kiel.de/~kds/koester_models/da/da_model_grid.fits",
    # 可能的替代路径
    "https://www.astro.physik.uni-kiel.de/kds/koester_models/da_grid.tar.gz",
    # VizieR 上的 Koester 模型
    "https://cdsarc.cds.unistra.fr/ftp/cats/V/130/",
    # 其他可能的镜像
    "https://archive.stsci.edu/hlsps/koester-wd/",
]

def try_download(url, filepath):
    try:
        print(f"尝试: {url}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=20, context=ctx)
        data = response.read()
        print(f"  成功! 大小: {len(data)} 字节")
        with open(filepath, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"  失败: {e}")
        return False

print("="*60)
print("尝试下载 Koester 白矮星模型大气")
print("="*60)
print()

# 先尝试列出目录内容
for url in URLS[:3]:
    try:
        print(f"探测目录: {url}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=15, context=ctx)
        content = response.read().decode('utf-8', errors='ignore')
        print(f"  状态: {response.status}")
        print(f"  内容前 1000 字符:")
        print(content[:1000])
        print()
    except Exception as e:
        print(f"  失败: {e}")
        print()

# 尝试下载具体文件
print("\n尝试下载模型文件...")
for i, url in enumerate(URLS):
    ext = url.split('.')[-1] if '.' in url.split('/')[-1] else 'dat'
    filepath = os.path.join(MODEL_DIR, f"koester_model_{i}.{ext}")
    if try_download(url, filepath):
        print(f"\n下载成功! 文件保存在: {filepath}")
        break
else:
    print("\n所有下载源均失败。")
    print("建议:")
    print("1. 手动从 https://www.astro.physik.uni-kiel.de/kds/koester_models/ 下载")
    print("2. 或使用 astropy 的模型大气接口")
    print("3. 继续使用当前的 Bergeron+ 1992 近似模型")
