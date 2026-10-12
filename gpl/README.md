# GPL · 从连接到空间

56 页中文 OpenROAD Global Placement 演示。面向新人与 GPL 开发者，重点是线长模型、静电密度、Nesterov 数值优化、时序和可布线性反馈。核心算法 28 页，时序 / 拥塞反馈 10 页；不展开 Tcl 注册与选项管理。

- [在线演示](https://zint99.github.io/presentation/gpl/)
- [PDF](./gpl-deep-dive.pdf)
- [逐页讲解稿](https://zint99.github.io/presentation/gpl/notes.html)
- [固定版本源码索引](https://zint99.github.io/presentation/gpl/source-index.html)

## 阅读与演示

直接打开 `index.html`，不需构建、服务端、网络或 CDN。所有图形均为本地 SVG，公式为 HTML / Unicode，PDF 已包含完整 56 页。

- 方向键、PageUp / PageDown、空格：翻页；Home / End：首尾页。
- O：目录；N：当前窗口备注；F：全屏；移动端支持水平滑动。
- `#slide-13` 等深链接定位页面；输入框和按钮保留原生键盘行为。
- 备注在当前窗口可见，投屏时建议另开 `notes.html` 阅读讲解稿。
- 浏览器打印输出全部页。打印使用固定示例状态（Nesterov 15 步），结束后恢复交互值。

快速入门约 25 分钟：01–07 → 10 → 15、18、20–21 → 28、32、34 → 35、39、42 → 50、56。完整分享建议 90–120 分钟，也可分两次进行。

## 内容结构

| 页码 | 重点 |
| --- | --- |
| 01–07 | GPL 在流程中的位置、变量、两种力与主循环 |
| 08–14 | B2B 起点、稀疏系统手算、HPWL、WA 与导数、平滑调度 |
| 15–24 | Bin、scatter、面积守恒、filler、障碍、overflow、Poisson / DCT、gather |
| 25–34 | 预条件、λ 初始化和调度、Nesterov 状态、步长、快照、真实 golden 曲线 |
| 35–38 | Slack 到 net 权重、resizer 状态变更、时序相关性 |
| 39–44 | RUDY / GRT、宏块通道、尾部 RC、面积膨胀、预算与恢复 |
| 45–52 | 数据架构、region、GPU、增量模式、诊断、QoR 实验与阅读路径 |
| 53–56 | 自测、记号、证据和完整心智模型 |

## 交互实验与证据边界

1. 第 13 页：一维 WA 精确求值与解析导数；不是完整 GPL。
2. 第 20 页：四个无障碍 bin 的 overflow 手算模型；不模拟真实模型重建。
3. 第 30 页：凸二次函数上的 GD 与 Nesterov；不代表 GPL 性能。
4. 第 43 页：当前分支的一次膨胀公式，含整数尺寸舍入；不运行后续布局。

源码基线固定到 [zint99/OpenROAD `977813f3b02e35692b7b5ab3cca36e4e6fa380bb`](https://github.com/zint99/OpenROAD/commit/977813f3b02e35692b7b5ab3cca36e4e6fa380bb)。GPU、Virtual CTS、增量恢复、移动稳定性与膨胀预算等实现按此 fork 解释，不泛指所有上游版本。

封面从 `src/gpl/test/simple01.defok` 的坐标与同目录 `nangate45.lef` 的 master 尺寸重绘。第 34 页曲线从 `simple01.ok` 提取，25 个迭代采样点。`data/simple01.json` 保存提取后的数值及来源。这些是仓库已有 golden，**本次未重新运行 OpenROAD**。其余图例均为自行绘制的教学示意，无虚构 benchmark 或加速比。

延伸阅读：[ePlace, Lu et al., TODAES 2015](https://doi.org/10.1145/2699873)；[RePlAce, Cheng et al., TCAD 2019](https://vlsicad.ucsd.edu/Publications/Journals/j126.pdf)。主要技术细节以固定源码为准，不将论文历史结果直接套用于当前实现。

## 编辑与验证

- `content.py`：每页正文、逐页讲解、来源、章节。
- `diagrams.py`：原始 SVG 图例；`data/simple01.json`：已有回归数据。
- `style.css` / `deck.js`：演示、移动端、打印、键盘与交互。
- `numerics.js`：纯数值教学模型，浏览器和 Node 测试共用。
- `build.py`：仅用 Python 标准库生成 `index.html`、`notes.html`、`source-index.html`。

在仓库根目录：

```sh
python3 gpl/build.py
node gpl/test-numerics.cjs
python3 gpl/validate.py --pdf --screenshots
```

浏览器验证需要已安装 Playwright Python 包与 Chromium；普通阅读无需这些依赖。验证覆盖 56 页在 1280×720、1440×900、1920×1080、390×844 下的排版、SVG 文本边界、键盘、目录、备注、深链接、滑动、四个实验及 PDF 页面内容边界。截图与报告放在忽略提交的 `.validation/`。

数值测试使用独立有限差分检查 WA 导数，验证平移不变性和极限、密度手算、膨胀阈值 / 上限 / 舍入，以及 GD 的闭式基线和 Nesterov 越过最优点的行为。

## 托管

沿用仓库现有 `master` 根目录 GitHub Pages 配置，入口是 `gpl/index.html`。无需新增发布工作流或第三方资源。
