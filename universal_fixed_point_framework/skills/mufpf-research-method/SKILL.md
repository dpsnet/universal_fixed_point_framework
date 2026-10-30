---
name: mufpf-research-method
description: MUFPF（元通用不动点范畴框架）理论研究的规范化工作流。当需要在本项目 universal_fixed_point_framework 中推进理论推导、登记研究成果（104az-NNN 条目）、执行判据审计（σ_dev/状态阶梯/负控/预注册检验）、数值验证（pyenv 脚本）、Lean 形式化（lake build 零 sorry）、回扫勘误时使用。触发场景：用户说"继续推进/继续/攻此开放项/逐一推进"、"登记/更新登记表/更新记录"、"审计/评判/这个算不算命中/为什么没登记"、"Lean 固化/形式化"等 MUFPF 研究操作。
---

# MUFPF 理论研究规范

## Overview

在 MUFPF 项目（E:\workspace\hyper-resolution\universal_fixed_point_framework）中推进理论研究的标准方法：开放项 → 数值验证 → 判据评判 → 三处登记 → 核验闭环。**三处登记协议为强约束**（用户多次质询后固化："为何 §1 无 104az-190/191"、"只更新 changelog 不更新登记表"）。

## 工作上下文

- 核心文档：`notes\generative_chain_map.md`（§1 生成链全集 / §2 / §3 κΛ 链 / §4 / §6 核磁子链 / §9 changelog / §10 判据协议区 §10.1~§10.28）、`RESEARCH_STATE.md`（头部登记块）、`scripts\`（数值脚本）、`formal_proof\MUFPFormalization`（Lean 项目）。
- 编号体系：104az-NNN 连续编号；编号↔章节映射：200→§10.1、201→§10.2……（每登记一条，下一编号 = 当前最大 +1）。
- 核心目标：纯内生（范畴公设→框架常数→生成链）衍生物理数值，每值可溯源到明确生成链。

## Workflow 1：推进研究项

1. 先 Grep/Read 相关登记现状（开放项、候选、状态），以现状为准，不重复已证伪路径。
2. 写数值脚本到 `scripts\`（命名 v04_openNNN_<topic>.py），用 pyenv 3.11.8 运行，输出重定向到同目录 .out.txt。
3. 按判据评判（Workflow 3），明确诚实边界。
4. 三处登记（Workflow 2）。
5. 核验登记落位（changelog 行 + 正文 §N + RESEARCH_STATE 均出现编号）。

## Workflow 2：三处登记协议（强制）

每条 104az-NNN 成果必须在三处落位：

1. **正文** `generative_chain_map.md`：在 §10.x（判据协议区）或对应正文章节写完整条目——动机、计算（含脚本名与输出）、判定、诚实边界。
2. **changelog**（§9）：`> **104az-NNN（日期，标题）**：<浓缩要点，含关键数值、判据、脚本名、登记位置>。` 单行格式。
3. **RESEARCH_STATE.md** 头部登记块：追加一条要点（编号、核心结论、脚本、登记位置）。

核验：用 Read/Grep 确认三处均含编号；缺一处 = 登记未完成，禁止宣布完成。

## Workflow 3：判据评判（σ_dev 唯一权威）

完整规格见 `references/criteria-protocol.md`。速查：

- **P1 dev/σ**：命中判定用 dev/σ（观测不确定度归一），非 dev%。四档：≤0.5σ 兼容无分辨力 / ≤3σ 候选 / 3–5σ 需解释 / >5σ 真实偏差。表列三件套：dev、σ_dev、不确定度来源。
- **P2 状态五阶梯**：⬜ 未溯源 / 🟡 拟合候选 / 🟢 链内唯一（已计搜索空间）/ 🔵 先验预言已确认 / ✅ 推导（机制+唯一+独立预言）。唯一状态源；**当前证据下无物理常数达 ✅**。
- **P3 负控基线**：每个 ✅/🟢 行必须附（表达式语法、原子集、深度上限、候选总数、命中数、容差），并对 decoy 目标跑假阳性率（≥10 decoy）。
- **预注册检验协议 v1.0**：族定义/值域/容差 3σ 绝对/判定唯一/升级条件 = 协议下未来新量先验命中或负控 ≥10 decoy。**发现顺序 ≠ 证据强度**（事后唯一性不升格）。
- **证据通道 v0.5 四条**：① 代数闭合链（机器证明）② 跨链交叉锁定（弱）③ 预注册预言（强）④ 命中质量数量级分离。
- **等价改写 ≠ 独立确证**：同一整数多身份 = 同一事实的等价改写，不累加置信度。
- **"不是用 σ_dev 评判吗"**：σ_dev 为命中唯一权威（用户裁决）；无观测精度支撑的量（如 Λ_QCD 0.14%）判"链溯源（结构判据）"而非观测确认。

## Workflow 4：数值验证（pyenv）

完整环境见 `references/numerical-env.md`。速查：

- 固定解释器：`D:\pyenv\pyenv-win\versions\3.11.8\python.exe`（numpy 2.4.4 + scipy 1.17.1）；裸 python = 3.14 无 numpy，不可用。
- 输出重定向：`python xxx.py *> "scripts\xxx.out.txt"`；PowerShell 引号内分号陷阱 → 一律落 .py 文件运行。
- 临时脚本用完删除（用户约束）；登记/复算脚本保留在 scripts\。
- 数值结论必须可复现：脚本 + .out.txt 留存。

## Workflow 5：Lean 形式化（零 sorry）

完整环境见 `references/lean-env.md`。速查：

- 每次 lake/lean 前设置三环境变量：`$env:ELAN_HOME="D:\tools\lean\.elan"; $env:ELAN_NO_SELF_UPDATE="1"; $env:PATH="D:\tools\lean\.elan\bin;"+$env:PATH`。
- 单模块构建：`lake build MUFPFormalization.<Module>`（>15s 自动转后台，TaskOutput 接结果）。
- **零 sorry 政策**；新增 sorry 必须三件套（注释原因 + 论文登记缺口 + 更新计数）。
- **先证伪再证明**：难证定理前按 Lean 定义逐字翻译成 Python，≥6 组随机样本残差 1e-8 全 0 才投入证明。
- 离线 mathlib 裁剪规避：`Mathlib.Data.Rat.Basic` 缺失 → 用 `import Mathlib.Tactic + Mathlib.Data.Rat.Defs`（通配）。
- Lean 证明的是框架自整数的算术恒等与有限枚举——不触及"自然界用这组整数"，标题级用语不得宣称"严格性边界闭合"。

## Workflow 6：回扫勘误

- 发现登记不一致（如正文标注与后登记冲突、根集块未同步）→ 立即勘误：修正正文 + changelog 追加勘误条目（如 104az-230b）+ RESEARCH_STATE 补注。
- 勘误留痕：不静默修改历史结论；新编号或同编号 b/c 后缀标注。

## 死路清单（勿重试）

- Bott 塔层无限累加/归纳锁 e（104az-199 证伪）。
- "族内最优命中质量 3.5× 余量"（216 崩溃：50 decoy rank 2/51）。
- T5 通用线性商模板（209 用户裁决撤回）。
- 预言 C 作为唯一性裁决通道（218：代数侧裁决失效，267/400 反解干净）。
- T4 为合格模板正例（214：decoy 击穿）。
- 1124315 恒等式挑战（两次：乘法正确但目标错位）。
- "双口径矛盾未决"（221：分层误会已消）。
- 事后唯一性过滤升格（216：发现顺序 ≠ 证据强度）。

## Resources

- `references/criteria-protocol.md`：判据体系完整规格（P1 四档表、P2 阶梯转移规则、P3 六元组、协议 v1.0、证据通道、负控操作法）。
- `references/registration-format.md`：三处登记格式模板与编号↔章节映射。
- `references/numerical-env.md`：pyenv 环境、脚本惯例、PowerShell 陷阱。
- `references/lean-env.md`：Lean 环境变量、零 sorry、先证伪流程、常见错误修复。
- `scripts/registration_check.py`：核验 104az-NNN 三处登记落位（changelog + 正文 + RESEARCH_STATE）。
