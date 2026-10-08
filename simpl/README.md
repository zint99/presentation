# SimPL 论文演示

15 页中文静态演示，基于 Kim、Lee、Markov 的 CACM 2013 论文。无需安装依赖、构建或外部 CDN，可直接打开 `index.html`，也可作为 GitHub Pages 子目录使用。

## 使用

- 左右方向键、PageUp / PageDown、空格：翻页。
- Home / End：首尾页。
- O：目录。N：当前窗口讲者备注。F：全屏。
- 移动设备可水平滑动，或使用底部按钮。
- `#slide-5` 等链接直接定位页码。
- 浏览器打印会输出全部 15 页，可保存成 PDF。
- 备注显示在当前窗口，投屏时也会可见。

## 内容与来源

Myung-Chul Kim, Dong-Jin Lee, Igor L. Markov. *SimPL: An Algorithm for Placing VLSI Circuits*. Communications of the ACM, 56(6), pp.105–113, June 2013. https://doi.org/10.1145/2461256.2461279

所有几何图形为原理重绘。第 5 页动画使用线性插值，不运行 SimPL，不代表实测迭代结果。实验数值取自论文表 1 和图 10。每页底部标明来源，详细解释位于讲者备注。

## 托管

保留目录结构即可，入口为 `simpl/index.html`。若仓库已将 `master` 根目录配置为 GitHub Pages，合并后通常从 `/presentation/simpl/` 访问。本更改不修改 Pages 配置或添加部署工作流。
