# -*- coding: utf-8 -*-
# 拆分 §4 条目 7：104az-154/155/156 拆为独立条目，原 8-11 顺延 +3
import io, re

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md"
with io.open(P, "r", encoding="utf-8") as fp:
    lines = fp.readlines()

# 定位 §4 区域
sec4_start = next(i for i, l in enumerate(lines) if l.startswith("## 4."))
sec4_end = next(i for i, l in enumerate(lines) if l.startswith("## 8."))

# 找条目 7 行（列表项，以 "7. " 开头）
idx7 = None
for i in range(sec4_start, sec4_end):
    if lines[i].startswith("7. （新）m_p/m_e") or lines[i].startswith("7. （新）m\\_p/m\\_e"):
        idx7 = i
        break
if idx7 is None:
    print("条目7未找到"); raise SystemExit

line = lines[idx7]
print("原条目7长度:", len(line))

# 拆分：按 104az-153/154/155/156 分界
# 主体+153: 从行首到 "镜像家族" 结束（154 之前的 "；"）
m154 = line.find("104az-154：")
m155 = line.find("104az-155：")
m156 = line.find("104az-156：")

item7 = line[:m154].rstrip()[:-1]  # 去掉末尾 "；"（若为 "；"）
# 修正：item7 应保留 153 段与加粗闭合符的清理
item7 = re.sub(r"——\*\*104az-153", "——**104az-153", item7)
if not item7.endswith("）**"):
    # 补闭合加粗
    item7 = item7 + "**"

item8 = "8. （新）家族第三实例（104az-154）：353 = 45・8−7（DS 禁闭质量 M(0)，弱实例判定），353/210 = 12/7−1/30（主线 B 线索）；家族矩阵（323/259 无身份）+ δ 家族候选排除（53/10⁵ dev 0.066% 不达）"
item9 = "9. （新）353 双身份 + 禁闭域 42 锚定（104az-155）：353 = (42²+1)/5（42 = 幂基・N_gen・对合域 = 2・3・7）；平方 + 1 家族 {37,65,1765}；★★★ 禁闭域 42 锚定（4.2 = 42/10、Λ_QCD~210 = 5×42、DS M(0) = (42²+1)/5）；κΛ 候选桥 353×8/7×(1−1/240) dev +0.004% 不升格"
item10 = "10. （新）双身份家族（104az-156）：41 = 8・5+1 ≡ (3⁴+1)/2、39 = 8・5−1 ≡ (14²−1)/5、比例恒等 39/65 = 3/5、家族自包含（42²+1∋353、105²+1∋37、32²+1∋41）——双身份家族 {37,41,65,353,39} 5 成员，41/353 有观测锚"

# 原 8-11 编号 +3 → 11-14
renum = {}
for i in range(sec4_start, sec4_end):
    m = re.match(r"^(\d+)\. ", lines[i])
    if m and 8 <= int(m.group(1)) <= 11:
        old = int(m.group(1))
        new = old + 3
        lines[i] = lines[i].replace(f"{old}. ", f"{new}. ", 1)
        renum[old] = new

# 替换条目7并插入新条目
lines[idx7] = item7 + "\n"
for j, it in enumerate([item8, item9, item10]):
    lines.insert(idx7 + 1 + j, it + "\n")

with io.open(P, "w", encoding="utf-8") as fp:
    fp.writelines(lines)

# 验证
new_lines = lines
sec4_end_new = next(i for i, l in enumerate(new_lines) if l.startswith("## 8."))
nums = []
for i in range(sec4_start, sec4_end_new):
    m = re.match(r"^(\d+)\. ", new_lines[i])
    if m:
        nums.append(int(m.group(1)))
print("§4 条目编号序列:", nums)
print("重编号映射:", renum)
print("条目7新长度:", len(item7))
