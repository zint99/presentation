# SimPL 论文演示

21 页中文静态演示，基于 Kim、Lee、Markov 的 CACM 2013 论文。无需安装依赖、构建或外部 CDN，可直接打开 `index.html`，也可作为 GitHub Pages 子目录使用。

## 使用

- 左右方向键、PageUp / PageDown、空格：翻页。
- Home / End：首尾页。
- O：目录。N：当前窗口讲者备注。F：全屏。
- 移动设备可水平滑动，或使用底部按钮。
- `#slide-5` 等链接直接定位页码。
- 浏览器打印会输出全部 21 页，可保存成 PDF。
- 备注显示在当前窗口，投屏时也会可见。

## 内容与来源

Myung-Chul Kim, Dong-Jin Lee, Igor L. Markov. *SimPL: An Algorithm for Placing VLSI Circuits*. Communications of the ACM, 56(6), pp.105–113, June 2013. https://doi.org/10.1145/2461256.2461279

所有几何图形为原理重绘。几何插值动画使用线性插值，不运行 SimPL，不代表实测迭代结果。实验数值取自论文表 1 和图 10。每页底部标明来源，详细解释位于讲者备注。

新增四组逐步公式推导：二次能量到矩阵、双单元手算、B2B 与 HPWL 的等值关系、锚点对矩阵的更新。推导支持上一步、下一步和重置，打印会展开全部步骤。

前瞻合法化动画分为 8 个预设阶段，支持步进、播放、暂停与重置。另一个双单元示例会实时精确求解 2×2 系统并显示残差，统一权重 λ 仅为教学参数，并非完整 SimPL 实现。翻页、打开目录或备注、切换后台时自动停止播放。

## 托管

保留目录结构即可，入口为 `simpl/index.html`。若仓库已将 `master` 根目录配置为 GitHub Pages，合并后通常从 `/presentation/simpl/` 访问。本更改不修改 Pages 配置或添加部署工作流。

## 数值验证

在仓库根目录执行 `node simpl/test-numerics.cjs`，无需第三方依赖。验证双单元解析解、残差、锚点极限趋势、B2B 等值关系以及旧权重不再等值的反例。浏览器视觉与交互回归仍需在真实浏览器完成。
