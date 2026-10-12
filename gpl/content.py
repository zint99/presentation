"""Editorial source of the GPL presentation. Rebuild with python3 build.py."""

REV = '977813f3b02e35692b7b5ab3cca36e4e6fa380bb'
ROOT = f'https://github.com/zint99/OpenROAD/blob/{REV}/src/gpl/'
SOURCES = {
    'overview': ('GPL 模块说明', 'README.md'),
    'pb': ('PlacerBase · 数据建模', 'src/placerBase.cpp'),
    'ip': ('InitialPlace · B2B 建模', 'src/initialPlace.cpp#L278'),
    'solver': ('BiCGSTAB 求解器', 'src/solver.cpp#L17'),
    'wa': ('WA 线长与力', 'src/nesterovBase.cpp#L1445'),
    'waderiv': ('WA 导数与符号', 'src/nesterovBase.cpp#L1611'),
    'coef': ('平滑系数调度', 'src/nesterovPlace.cpp#L1355'),
    'scatter': ('面积散射与 overflow', 'src/nesterovBase.cpp#L982'),
    'smooth': ('密度尺寸与缩放', 'src/nesterovBase.cpp#L3476'),
    'filler': ('Filler 初始化', 'src/nesterovBase.cpp#L2357'),
    'fixed': ('固定面积并集与缩放', 'src/nesterovBase.cpp#L869'),
    'fft': ('CPU DCT Poisson 求解', 'src/fft.cpp#L110'),
    'gather': ('密度力回采样', 'src/nesterovBase.cpp#L3602'),
    'grad': ('力合成与预条件', 'src/nesterovBase.cpp#L3915'),
    'lambda': ('密度罚系数初始化', 'src/nesterovBase.cpp#L3830'),
    'phi': ('罚系数迭代调度', 'src/nesterovBase.cpp#L4251'),
    'step': ('步长估计与检查', 'src/nesterovBase.cpp#L3860'),
    'coord': ('Nesterov 坐标更新', 'src/nesterovBase.cpp#L4426'),
    'loop': ('Nesterov 主循环', 'src/nesterovPlace.cpp#L1136'),
    'backtrack': ('Backtracking', 'src/nesterovPlace.cpp#L999'),
    'overflow': ('迭代 overflow 分母', 'src/nesterovBase.cpp#L4299'),
    'converge': ('区域收敛判定', 'src/nesterovBase.cpp#L4550'),
    'revert': ('发散快照与恢复', 'src/nesterovPlace.cpp#L644'),
    'timing': ('TimingBase · net 重加权', 'src/timingBase.cpp#L125'),
    'tdloop': ('时序反馈编排', 'src/nesterovPlace.cpp#L375'),
    'clock': ('Virtual CTS', 'src/clockBase.cpp'),
    'route': ('RouteBase · 拥塞反馈', 'src/routeBase.cpp#L862'),
    'inflate': ('Tile 膨胀比例', 'src/routeBase.cpp#L628'),
    'cellinflate': ('单元膨胀与 filler 预算', 'src/routeBase.cpp#L943'),
    'rc': ('拥塞尾部统计', 'src/routeBase.cpp#L1163'),
    'routeloop': ('拥塞重启与快照', 'src/nesterovPlace.cpp#L734'),
    'model': ('GCell / GPin / GNet', 'src/nesterovBase.h'),
    'gpu': ('GPU 迭代上下文', 'src/gpu/nesterovDeviceContext.h'),
    'incremental': ('增量布局两阶段', 'src/replace.cpp#L138'),
    'golden': ('simple01.ok · 已有 golden', 'test/simple01.ok'),
    'def': ('simple01.defok · 已有布局', 'test/simple01.defok'),
    'tests': ('GPL 回归测试', 'test'),
    'eplace': ('ePlace · Lu et al., TODAES 2015', 'https://doi.org/10.1145/2699873'),
    'replace': ('RePlAce · Cheng et al., TCAD 2019', 'https://vlsicad.ucsd.edu/Publications/Journals/j126.pdf'),
}

SLIDES = []
def add(ch, title, subtitle, body, diagram, takeaway, notes, refs, **kw):
    SLIDES.append(dict(ch=ch,title=title,subtitle=subtitle,body=body,diagram=diagram,
                       takeaway=takeaway,notes=notes,refs=refs.split(),**kw))

add('序章', 'GPL：从连接到空间', 'OPENROAD GLOBAL PLACEMENT · 概念 / 数学 / 源码',
    '<p class="hero-copy">把数十万单元的位置，<br>写成一个可以迭代求解的问题。</p><p>中文深度导读 · 56 页<br>建议：入门 25 分钟 / 完整分享 90–120 分钟</p><p class="small">源码基线：zint99/OpenROAD · 977813f3b02e<br>图例：青色＝单元 / 线长；橙色＝密度 / 拥塞</p>',
    'real', '理解三个动作：拉近连接、疏散密度、引入物理反馈。',
    'GPL 是 Global Placement，全局布局。本演示以当前工作区对应的公开提交为基线，并非对所有 OpenROAD 版本的描述。右图由 simple01.defok 和同目录 LEF 的真实单元尺寸重绘，展示已有回归基准的 GPL 输出，不是本次新运行截图；它尚未经过详细布局。其余未特别标注的几何图均为原理示意。先把网表变成空间问题，再讲数学，最后落到源码。讲解重点放在线长、密度、优化循环及反馈，不展开命令注册和选项管理。', 'def overview', theme='dark')

add('序章', '两条阅读路径，同一条算法主线', 'READING MAP · 按重要性分配时间',
    '<div class="rows"><p><b>快速入门 · 25 分钟</b><br>01–07 → 10 → 15、18、20–21 → 28、32、34 → 35、39、42 → 50、56</p><p><b>算法深读 · 90–120 分钟</b><br>顺序阅读 08–44；重点推导 WA、Poisson 与 Nesterov，并操作四个实验。</p><p><b>开发者延伸</b><br>45–55：数据边界、源码导航、诊断与回归设计。</p></div>',
    'roadmap', '核心算法占 28 页；时序与拥塞反馈占 10 页。',
    '全篇分成三个问题：优化什么，怎么优化，如何让结果适合真实芯片。第 8–34 页加第 6 页提供 28 页核心算法内容；第 35–44 页用 10 页讲物理反馈。新人可以跳过详细导数和数据同步，先看每页底部的一句话。讲者应根据听众选择快速路径或完整路径，不必在一次入门分享中读完所有源码附录。四个交互实验都采用明确的教学模型，不能当作 OpenROAD 仿真器或性能证据。', 'overview')

add('01 / 建立直觉', 'GPL 决定整体分布，DPL 完成合法落位', 'CONTEXT · 在物理设计流程中定位',
    '<p>输入：网表、单元尺寸、core / rows、固定对象、I/O 与区域约束。</p><p>输出：可移动实例的坐标，以及布局质量指标。</p><p>时序驱动可保留 resizer 修改，因此部分运行也会改变网表和单元面积。</p>',
    'pipeline', '全局布局允许暂时重叠；最终还需要合法化与布线验证。',
    '网表描述逻辑连接，但不决定物理距离。Floorplan、宏布局和引脚放置给 GPL 一个带约束的空间。GPL 用连续坐标找到整体分布，不能替代 DPL 的行、站点、方向和无重叠检查；也没有生成最终金属走线。典型流程中 DPL 后还会经历 CTS、全局布线、详细布线以及进一步优化。图中的时序和布线反馈箭头表示 GPL 可在内部借助其他模块评估位置，不表示已经完成最终实现。', 'overview tdloop')

add('01 / 建立直觉', '优化变量是单元中心，连接端点是 pin', 'GEOMETRY · 四类对象',
    '<p><b>Movable cell</b>：中心坐标 (xᵢ, yᵢ) 可变。</p><p><b>Fixed macro / blockage</b>：占空间但不参与移动。</p><p><b>Pin</b>：位置 = cell 中心 + 变换后的 offset；I/O 可提供固定端点。</p><p><b>Net</b>：连接多个 pin 的超边，不能只看 cell 中心距离。</p>',
    'geometry', '尺寸、坐标、pin offset 和可移动状态，共同决定正确的力。',
    'OpenDB 实例位置与 GPL 内部中心坐标不是同一约定，写回时要处理中心到数据库几何位置的转换。Pin offset 与实例方向相关。宏块是否可移动取决于流程和实例状态，并非见到宏块就固定。本页和后面的核心推导采用 I/O 固定、标准单元可移动的基本模式；当前分支还有并行 I/O 放置扩展，但它不属于这里推导的基准情形。图中菱形表示 pin，小圆点表示中心，避免把两者混同。', 'pb model')

add('01 / 建立直觉', '只追求短线长，会把电路拉成一团', 'TWO FORCES · 两种相反的趋势',
    '<p class="accent-text">线长力：连接越近越好。</p><p class="orange-text">密度力：为每个单元分配足够空间。</p><p>均匀不是目的本身：还要兼顾关键路径、宏块通道和可布线性。</p>',
    'forces', '布局的难点，是在连接结构和空间容量之间持续寻找平衡。',
    '用一组相连的单元解释两种力。左侧布局线长很短，却存在严重重叠；右侧分布缓解拥挤，但拉长部分连接。数学上必须把空间需求放进优化过程，不能在最后简单地把重叠单元随便挪开，否则合法化会摧毁线长和时序。箭头只表达吸引与排斥的方向，不是实际梯度数值。密度场与网表连接图相互作用，最终分布不需要严格视觉均匀。', 'wa gather')

add('01 / 建立直觉', '把位置优化写成两个主要代价', 'OBJECTIVE · 固定一轮权重时的模型',
    '<div class="equation">min<sub>z ∈ Ω</sub>　W<sub>γ</sub>(z; ω) + λ D(z)</div><p>z：所有可移动中心；Ω：允许移动的区域。</p><p>W<sub>γ</sub>：平滑线长，ω 是 net 权重。</p><p>D：静电密度能量；λ 平衡线长与疏散强度。</p>',
    'objective', 'γ、λ、net 权重与虚拟面积会变化：整个运行不是固定目标的单次下降。',
    '这是一轮内理解核心算法的数学表达，不是源码中直接求值的完整闭式目标。约束区域既有显式的边界投影，也有通过障碍密度表达的可用空间。时序反馈修改 net 权重，拥塞反馈修改虚拟占用；每轮还会调整平滑系数和密度罚系数。因此不能因为某一步 HPWL 或抽象目标上升就判定求解失败，也不能套用固定凸函数的 Nesterov 收敛保证。优化器实际主要依靠力、步长和 overflow 来推进。', 'grad loop')

add('01 / 建立直觉', '完整算法是一条内循环，外加两种反馈', 'ALGORITHM · 先记住这张图',
    '<p><b>起点</b>：建立布局模型；可选 B2B 初始布局。</p><p><b>高频循环</b>：算线长力与密度场 → 更新位置 → 检查步长。</p><p><b>低频反馈</b>：在合适阶段评估时序和拥塞，再修改模型继续迭代。</p>',
    'mainflow', 'Initial placement 提供起点；Nesterov placement 负责主要优化。',
    '不要把 initial placement 的线性系统求解，与后续 Nesterov 的非线性优化混为一谈。前者可跳过；后者才是主要的密度与线长联合优化。一次 Nesterov 外层迭代内部可能有多次步长试探，所以迭代次数不等于梯度调用次数。时序与拥塞评估相对昂贵，使用 overflow 等条件选择触发点。全部区域满足收敛条件后写回数据库，再由后续模块检验物理可实现性。', 'loop ip')

add('02 / 连接与线长', '初始布局：用 B2B 弹簧得到有结构的起点', 'INITIAL PLACEMENT · 可选的线性求解',
    '<p>每个方向分别找 net 的极值 pin，把边界端点与其他端点连接。</p><div class="equation compact">wᵢⱼ ∝ 1 / max(|xᵢ − xⱼ|, ε)</div><p>固定端点进入右端向量；可移动端点进入稀疏矩阵。</p><p>更新 pin 极值和权重，再解 x / y 两个系统。</p>',
    'b2b', '稀疏 B2B 模型降低连接复杂度，但此时还没有解决重叠。',
    '当前 createSparseMatrix 的 net 基础权重为 netWeightScale/(pin_count−1)，再除以方向距离的下界截断值。图示只表达边界到边界的连接拓扑，不宣称这里的二次目标严格等于 HPWL。极值 pin 和权重依赖当前位置，外层需要重建。过高 fanout 的 net 在初始阶段被跳过，避免建模代价过高；这不是说后续平滑线长一定忽略同一条 net。日志用 conjugate gradient 泛称，实际 solver.cpp 使用 Eigen BiCGSTAB。', 'ip solver')

add('02 / 连接与线长', '两单元手算：固定端点如何确定位置', 'WORKED EXAMPLE · 等权弹簧的一维切片',
    '<div class="equation compact">E = ½[x₁² + (x₁−x₂)² + (x₂−10)²]</div><p>对 x₁、x₂ 求导并令其为零：</p><div class="equation compact">2x₁ − x₂ = 0<br>−x₁ + 2x₂ = 10</div><p><b>x₁ = 10/3，x₂ = 20/3。</b> 两条方程残差均为 0。</p>',
    'quadratic', '有锚点的连接决定相对位置；没有面积约束，单元仍可能重叠。',
    '这是解释稀疏线性系统的教学算例，权重固定为 1，不是完整的 OpenROAD B2B 迭代。矩阵对角线累加相邻弹簧权重，非对角线为负权重，固定端点贡献右端项。固定在 0 和 10 的端点让解唯一；若只保留 x₁ 与 x₂ 的连接，整体平移不改变能量，会出现零模态。这个例子让新人理解为什么固定 pin、初始化和数值退化处理重要，但不必深入求解器的全部实现。', 'ip solver')

add('02 / 连接与线长', 'HPWL：用包围盒估计一条 net 的线长', 'METRIC · HALF-PERIMETER WIRELENGTH',
    '<div class="equation compact">HPWLₑ = (x<sub>max</sub>−x<sub>min</sub>)<br>　　　 + (y<sub>max</sub>−y<sub>min</sub>)</div><p>示例 pin：(1,1)、(3,4)、(7,2)。</p><p>宽 6 + 高 3 = <b>9 个长度单位</b>。</p><p>不含绕障、层分配、via 与详细布线拓扑。</p>',
    'hpwl', 'HPWL 适合快速比较，但单独优化它会遇到不可导与梯度稀疏。',
    'HPWL 是包含所有端点的最小轴对齐包围盒的半周长。固定极值 pin 时，内部 pin 的小幅移动不会改变 HPWL，所以其导数大部分时候为零；极值身份切换又带来折点。真实路由必须满足层方向、障碍和线宽间距等条件，HPWL 只是早期代理指标。图中虚线矩形不是实际布线。还要区分总 HPWL 的报告口径与带时序权重的优化目标，二者并不一定使用相同加权方式。', 'wa overview')

add('02 / 连接与线长', 'WA：把 max / min 换成平滑的加权平均', 'WEIGHTED AVERAGE · 一个方向的公式',
    '<div class="equation compact">μ⁺ = Σ xᵢe<sup>xᵢ/γ</sup> / Σ e<sup>xᵢ/γ</sup><br>μ⁻ = Σ xᵢe<sup>−xᵢ/γ</sup> / Σ e<sup>−xᵢ/γ</sup><br>W<sub>γ,x</sub> = μ⁺ − μ⁻</div><p>γ 大：更平滑，极值选择更柔和。</p><p>γ → 0⁺：μ⁺ → max x，μ⁻ → min x。</p>',
    'wa', 'WA 不是 log-sum-exp；这里使用的是指数加权的坐标平均。',
    '每条 net 分别计算 x 和 y 方向的 weighted-average 线长，再按 net 权重组合。γ 是具有长度含义的平滑尺度；源码使用其倒数形式 wlCoeff，因此读代码时不要把参数变化方向反过来。固定一组坐标时，两个加权平均都落在最小和最大坐标之间，WA 不超过该方向跨度，γ 变小时趋近跨度。它不是精确实际线长，也不同于常见的 log-sum-exp 近似。后面的交互会把这两个量并排显示。', 'wa')

add('02 / 连接与线长', '对 WA 求导，得到每个 pin 的拉力', 'DERIVATION · 先归一化，再使用乘积法则',
    '<div class="equation compact">pᵢ⁺ = e<sup>xᵢ/γ</sup> / Σe<sup>xⱼ/γ</sup><br>∂μ⁺/∂xᵢ = pᵢ⁺[1 + (xᵢ−μ⁺)/γ]<br>∂μ⁻/∂xᵢ = pᵢ⁻[1 − (xᵢ−μ⁻)/γ]</div><p>数学梯度：∂W/∂xᵢ = ∂μ⁺/∂xᵢ − ∂μ⁻/∂xᵢ。</p><p>源码返回 <b>min 导数 − max 导数</b>，即负梯度方向。</p>',
    'wagrad', '从 pin 汇总到 cell，并乘 net 权重；固定 pin 参与算力，但不被移动。',
    '推导的关键是 pᵢ 本身也随坐标变化，不能把指数权重当作常数。利用 softmax 导数可得到图左的两个公式。OpenROAD 的 getWireLengthGradientPinWA 最后返回 gradientMin−gradientMax，因此它名为 gradient，实际已带下降方向的符号。一个 cell 的所有 pin 贡献相加，再乘各自 net 的 timing/custom 权重。对于 pin offset 固定的平移变量，pin 对 cell 中心的导数为 1。不要仅凭变量名再次加负号。', 'waderiv')

add('02 / 连接与线长', '实验 ①：调 γ，观察近似值和力如何变化', 'INTERACTIVE · 精确计算教学公式',
    '<p>固定一维 pin：<b>0、3、10</b>。</p><p>拖动 γ，比较 HPWL = 10 与 WA；箭头显示各 pin 的负梯度。</p><p>小 γ 更接近跨度；大 γ 更平滑，但不等于更强的力。</p><div class="control"><label for="gamma">γ 平滑尺度</label><input id="gamma" type="range" min="0.2" max="10" step="0.1" value="2"><output id="gamma-value">2.0</output></div><div id="wa-result" class="readout"></div>',
    'walab', '实验实时求值与求导；不是完整 GPL，也不是实测布局曲线。',
    '先把 γ 设为 10，看正负极值分布相互重叠，WA 显著小于跨度；再设为 0.2，权重集中在两端。中间 pin 的力随位置和尺度变化，不必始终等于零。箭头共同使用固定的显示缩放，读数保留真实教学公式数值。实现使用平移后的指数避免上溢，并用中心差分校验解析导数。可以让听众预测整体平移 100 个单位后，WA 与各 pin 的力是否改变：理论上保持不变。', 'wa waderiv', lab='wa')

add('02 / 连接与线长', '稳定指数计算，并随 overflow 收紧近似', 'NUMERICS · 平移不变性与连续化',
    '<p>用 e<sup>(xᵢ−x<sub>max</sub>)/γ</sup> 和 e<sup>(x<sub>min</sub>−xᵢ)/γ</sup>，把指数约束为非正。</p><p>减去共同常数不改变归一化加权平均。</p><p>源码随 overflow 下降增大 wlCoeff，即减小等效 γ，让线长模型更接近 HPWL。</p>',
    'coef', '从平滑到尖锐：早期便于移动，后期提高线长代理的分辨率。',
    '源码对 max 侧减去 net 最大坐标，对 min 侧使用最小坐标减 pin 坐标，避免很大的正指数；还会截断极小贡献。图画的是 updateWireLengthCoef 的实际分段因子：overflow 大于 1 时为 0.1，小于 0.1 时为 10，中间按指数变化，再乘 baseWireLengthCoef。纵轴是相对 base 的倍数，不是 γ 本身。overflow 是跨 region 的平均 scaled overflow，和日志里常见的 unscaled 数值不能无条件互换。', 'wa coef')

add('03 / 空间与密度', '把连续版图切成 bins，才能计算局部容量', 'DENSITY GRID · 面积而非实例数量',
    '<p>每个 bin 有面积 A<sub>b</sub> 和目标密度 t<sub>b</sub>。</p><div class="equation compact">容量 C<sub>b</sub> = t<sub>b</sub>A<sub>b</sub></div><p>一个大单元跨越多个 bin，按重叠面积分摊占用。</p><p>网格太粗会掩盖热点；太细会增加计算量与数值敏感性。</p>',
    'bins', '要衡量“这个地方被占了多少面积”，不能只数中心点。',
    '先用无宏块、无障碍的标准单元情形理解容量。密度 0.7 表示该 bin 的目标面积占用为 bin 面积的 70%，不是要求全芯片每个地方实际占用刚好一样。目标密度与 floorplan utilization 也不是同一个量：前者是布局模型的分布目标，后者通常是设计面积相对于可用面积的总体比例。障碍、宏块与 padding 等有效面积会改变实际可行范围。本页的网格仅用于教学，实际 bin 数由设计与算法设置决定。', 'scatter filler')

add('03 / 空间与密度', 'Scatter：一个 cell 的面积分摊到邻近 bins', 'GEOMETRY → GRID · 从矩形到密度',
    '<div class="equation compact">aᵢb = overlap(Rᵢ, B<sub>b</sub>) × sᵢ</div><p>Rᵢ 是密度矩形；sᵢ 是面积缩放系数。</p><p>遍历与 Rᵢ 相交的 bin，累加实际重叠面积。</p><p>位置移动时，多个 bin 的占用连续交换。</p>',
    'scatter', '同一个几何重叠算子，既用于密度散射，也用于电场回采样。',
    '图中矩形跨四个 bin，横向和纵向各分为两个重叠长度，四个面积乘积之和等于矩形总面积。密度平滑后需要乘 densityScale，避免凭空增加总电荷。源码在标准单元、宏块和 filler 上使用不同的面积路径；本页公式直接对应标准单元与 filler 的基础散射。跨 bin 求和时要注意整数 DBU 面积的转换和边界截断，不能只根据中心所在的 bin 赋全部面积。', 'scatter gather')

add('03 / 空间与密度', '密度平滑：扩大支撑范围，但守恒总面积', 'SMOOTHING · 避免小 cell 在网格内“失去方向”',
    '<div class="equation compact">d<sub>x</sub> = max(w, √2·b<sub>x</sub>)<br>d<sub>y</sub> = max(h, √2·b<sub>y</sub>)<br>s = wh / (d<sub>x</sub>d<sub>y</sub>)</div><p>矩形变宽，单位面积贡献相应变小。</p><p><b>s·d<sub>x</sub>d<sub>y</sub> = wh</b>：总“电荷”保持一致。</p>',
    'smoothing', '密度平滑守恒面积；拥塞膨胀会增加虚拟面积，二者不同。',
    '这里 w、h 是进入密度模型前的 GCell 模型尺寸，已经可能包含 padding 或其他有效尺寸调整，不一定等于原始库 master 尺寸。小 cell 若完全落入一个 bin，轻微移动不改变该 bin 占用，反馈不够敏感。扩大密度矩形至至少约 √2 个 bin 宽高，让移动更容易改变相邻 bin 的重叠，再用 densityScale 保持积分面积。源码还包含整数尺寸截断，所以守恒式是理想实数模型，实际有 DBU 舍入。', 'smooth')

add('03 / 空间与密度', 'Filler：用虚拟电荷表示未被真实单元占用的空间', 'VIRTUAL CELLS · 不写进逻辑网表',
    '<div class="equation compact">A<sub>filler</sub> ≈ t·A<sub>free</sub> − A<sub>inst</sub></div><p>无 net 连接，只响应密度力。</p><p>填补目标容量与实例面积的差额，让密度场有合理的平衡状态。</p><p>它们不是后续制造流程中插入的物理 filler cells。</p>',
    'fillers', 'Filler 参与密度场；报告真实拥挤程度时，overflow 分子排除 filler。',
    '公式采用标准单元的简化情形。当前代码的 A_inst 来自 getNesterovInstsArea，包含标准单元有效面积以及乘 targetDensity 的 movable macro 面积。若目标密度过低，计算出的 filler 面积为负，当前分支会警告并上调到可行的 uniform density，而非无条件接受设置。Filler 的尺寸与数量受实现约束和舍入影响。拥塞膨胀消耗额外虚拟面积时，还会削减 filler；所以 filler 是算法的空间预算，不是待布线的逻辑器件。', 'filler scatter')

add('03 / 空间与密度', '固定宏块与障碍：没有自由空间，就不能分配容量', 'CAPACITY · 几何并集比简单求和更重要',
    '<p>固定对象变成不可放置面积，进入 bin 的占用背景。</p><p>重叠的宏块 / blockage 必须按几何并集统计，避免重复扣减。</p><p>当前实现对固定背景使用 target density 缩放，并区分 scaled / unscaled 路径。</p>',
    'obstacles', '宏块移动状态、几何可用区域和密度归一化必须一起理解。',
    '不要把每个固定宏块都理解为单位密度的普通可移动电荷。当前实现以 per-bin 几何并集构造 unscaled 不可用面积，并乘目标密度；另一条 scaled 路径还有平滑与上界处理。这样在理想情形下，完全被固定对象覆盖的 bin 自身不应产生虚假的超容量。移动宏块则有自己的 targetDensity 面积缩放。图示强调两个障碍重叠区域只算一次，避免将相同空间重复记账而人为制造 overflow。', 'fixed scatter')

add('03 / 空间与密度', '实验 ②：同一组占用，目标密度改变 overflow', 'INTERACTIVE · 四个面积均为 100 的 bins',
    '<p>实例占用：<b>[80, 20, 65, 35]</b>，总面积 200；无宏块、无 filler、无障碍。</p><div class="equation compact">O = Σ max(0, a<sub>b</sub>−100t) / 200</div><div class="control"><label for="target">目标密度 t</label><input id="target" type="range" min="0.5" max="0.9" step="0.05" value="0.6"><output id="target-value">0.60</output></div><div id="density-result" class="readout"></div><p class="small">这是标准单元简化算例；真实代码还有宏块与归一化保护。</p>',
    'densitylab', 't = 0.60 时：超额面积 20 + 0 + 5 + 0 = 25，overflow = 0.125。',
    '密度场的分子包含 instance、filler 和 non-place area；overflow 的分子不包括 filler。教学实验故意固定布局，仅改变 t，说明 overflow 降低不一定意味着单元移动或拥塞改善。实际运行中 target density 还影响 filler 与整个优化过程，不能用本实验预测最终结果。源码每轮的 overflow 分母取 max(A_inst, (iter/maxIter)·A_nonplace·0.05)，用于宏块占优的设计；初始化则直接使用 A_inst。跨区域平均也不是按面积加权，诊断要看各 region。', 'scatter overflow', lab='density')

add('03 / 空间与密度', '静电类比：让密集区域产生向外的力', 'POISSON · 密度 → 电势 → 电场',
    '<div class="equation compact">−∇²ψ = ρ − ρ̄<br>D ∝ ½∫ (ρ−ρ̄)ψ dA<br>E = −∇ψ</div><p>ρ：归一化密度；ρ̄：空间平均。</p><p>ψ：电势；D：静电能量；E：电场。</p><p>高密区域对远处也有影响，不只推动相邻 bin。</p>',
    'field', '电场来自整个密度分布；并非把每个热点独立地推向最近空格。',
    '这组方程采用标准静电能量的归一化表达，常数可吸收到 λ，离散尺度由具体实现处理；源码主要使用离散电场力，不会每步拿这个积分做目标值 line search。减去平均值使右端总量为零，满足 Neumann Poisson 问题的兼容条件；源码通过去掉零频分量实现相应处理。均匀分布不产生驱动移动的非零频电场。图中的箭头依据解析高斯热点的教学场形绘制，不是 OpenROAD FFT 输出。密度能量下降与每个 bin 的 overflow 单调下降也不是同一保证。', 'fft gather')

add('03 / 空间与密度', '在频域求 Poisson：微分变成乘法', 'SPECTRAL SOLVE · CPU 使用 DCT / 混合正弦余弦逆变换',
    '<div class="equation compact">ψ̂<sub>uv</sub> = ρ̂<sub>uv</sub> / (k<sub>u</sub>²+k<sub>v</sub>²)<br>ψ̂<sub>00</sub> = 0</div><p>① 密度网格做 DCT。<br>② 每个非零频率除以波数平方。<br>③ 逆变换得到电势与两个电场分量。</p><p class="small">规则网格上的变换通常为 O(B log B)，B 是 bin 数。</p>',
    'fft', '零频必须单独处理；非方形 bin 的两个方向尺度也不能混用。',
    '离散余弦基函数与法向零导数的边界条件相配。CPU 后端在 fft.cpp 中调用 Ooura ddct2d，电场分量的逆变换分别使用 ddsct2d 与 ddcst2d。实现有配套归一化以及 x/y bin 尺寸的频率缩放，因此不能把图上的概念公式直接替换成任意 FFT 库调用。u=v=0 时分母为零，这个模式代表常量电势与平均密度，不驱动移动，源码显式将电势和电场频率系数置零。B log B 是变换成本，不是整个 GPL 的复杂度。', 'fft')

add('03 / 空间与密度', 'Gather：把 bin 电场积分回每个 cell', 'GRID → GEOMETRY · 密度力的最后一公里',
    '<div class="equation compact">F<sub>D,i</sub> ≈ Σ<sub>b</sub> aᵢb E<sub>b</sub></div><p>用相交面积乘该 bin 的电场，再对覆盖区域求和。</p><p>大单元往往得到更大的原始密度力。</p><p>因此后面还需要预条件，统一不同单元的移动尺度。</p>',
    'gather', 'Scatter → Poisson → Gather，是密度计算最值得记住的数据流。',
    'getDensityGradient 重新遍历密度矩形覆盖的 bins，累加 overlapArea·densityScale·electroField。它返回的是推动单元沿电场方向移动的密度力，而不是要求更新时额外取负号的数学梯度。Filler 没有 wirelength force，所以其移动来自密度项。这里用标准单元解释基本算子，宏块在散射中的额外 targetDensity 缩放需要与实现一并核对。每轮计算成本包括重叠枚举，不只是 FFT；一个跨很多 bin 的大对象与小 cell 的代价不同。', 'gather scatter')

add('03 / 空间与密度', '密度低，不代表导线能穿过去', 'TWO HEATMAPS · Placement overflow ≠ Routing congestion',
    '<p><b>密度图</b>：实例模型面积 / 可放置容量。</p><p><b>拥塞图</b>：连线需求 / 可用 routing 资源。</p><p>两块宏之间的狭窄通道，可能几乎没有 cell，却承载大量跨区连接。</p>',
    'twoheatmaps', '判断可布线性需要连线与容量信息；只看单元面积不够。',
    '这是一张关键的概念分界页。密度 overflow 用来评估布局空间超容，routing overflow 通常描述边或轨道的需求超容量，它们单位、归一化和统计范围不同。右图中的热点来自大量连线经过狭缝，而左图相同位置可能是低密区。即使已经做到 cell 无重叠，仍可能遇到 pin access、宏块遮挡、层资源不足和 via 拥塞。后面的 routability loop 就是把这些额外信息反馈进空间分配。', 'scatter route')

add('04 / 数值优化', '预条件：把“力大”与“移动过猛”分开', 'PRECONDITIONING · 源码中的下降方向',
    '<div class="equation compact">dᵢ = (F<sub>W,i</sub> + λF<sub>D,i</sub>) / Pᵢ<br>Pᵢ ≈ max(P<sub>min</sub>, n<sub>pin,i</sub> + λAᵢ)</div><p>F<sub>W</sub> 与 F<sub>D</sub> 已经指向下降方向。</p><p>pin 多、面积大的单元，分母更大。</p><p>这是对角尺度修正，不是精确求 Hessian 逆矩阵。</p>',
    'precondition', '代码按 z ← z + αd 更新；别把“gradient”变量再取一次负号。',
    '当前标准单元 CPU 路径先把 net 力汇总，再将线长力与 λ 倍密度力相加，最后除以预条件。getWireLengthPreconditioner 返回 pin 数，getDensityPreconditioner 返回 GCell 模型面积，分母还有 minPreconditioner 下界。此表达不包括本分支并行 I/O 的特殊自由度和镜像约束。预条件让不同大小与连通度的对象拥有更合理的更新尺度，但并不消除所有病态问题，步长仍需估计和检查。', 'grad waderiv')

add('04 / 数值优化', 'λ 的起点：先匹配两种力的量级', 'DENSITY PENALTY · 不是直接使用一个固定常数',
    '<div class="equation compact">λ₀ = c₀ · ‖F<sub>W</sub>‖₁ / ‖F<sub>D</sub>‖₁</div><p>先计算全体相关 cell 的原始力绝对值之和。</p><p>c₀ 控制初始的相对密度强度。</p><p>当密度力总量为零时，源码使用回退值，避免直接除零。</p>',
    'balance', 'λ 的绝对数值依赖尺度；离开坐标单位、面积和力，单看数字没有意义。',
    'updateDensityPenaltyFromRatio 的公式使用 wireLengthGradSum / densityGradSum，再乘初始化因子。这里的范数写成 1 范数，指每个 cell 的 x/y 原始力绝对值相加。由于 DBU、bin 尺寸、面积和模型归一化都影响力，日志里的很小罚系数并不表示密度作用很弱。初始化还要用前后位置构造首个步长估计，对无有效线长梯度等退化情况做恢复。修改初始系数后应看力比例和收敛曲线，而不是只看是否更快达到 overflow。', 'lambda grad')

add('04 / 数值优化', 'λ 随迭代变化，把拥挤布局逐步展开', 'PENALTY SCHEDULE · 用 HPWL 变化控制增长',
    '<div class="equation compact">λ<sub>k+1</sub> = φ<sub>k</sub> λ<sub>k</sub><br>Δ = (HPWL<sub>k</sub>−HPWL<sub>k−1</sub>)/H<sub>ref</sub></div><p>HPWL 改善时，允许更积极增加密度压力。</p><p>HPWL 变差时，增长因子按 Δ 调整，并设下界。</p><p>实际 φ 还受动态调节与恢复逻辑影响。</p>',
    'penalty', '线长允许适度增长，以换取较低的空间冲突。',
    'getPhiCoef 在 Δ 小于 0 时返回 maxPhiCoef；否则返回 max(minPhiCoef, maxPhiCoef·maxPhiCoef^(−Δ))。然后 densityPenalty 乘这个因子。这里的 phiCoef 与电势 ψ 是不同概念，不能因名字相近混淆。整个算法不要求 HPWL 每步下降：初始布局集中时，展开通常会增加线长。具体版本还有动态调整 phi 参数的逻辑，因此图示重点是反馈关系，不能解读为所有运行都有固定指数增长曲线。', 'phi loop')

add('04 / 数值优化', 'Nesterov：在外推位置计算下一步', 'ACCELERATED UPDATE · 两套坐标',
    '<div class="equation compact">u<sub>k+1</sub> = y<sub>k</sub> + α<sub>k</sub>d(y<sub>k</sub>)<br>x<sub>k+1</sub> = ΠΩ(u<sub>k+1</sub>)<br>y<sub>k+1</sub> = ΠΩ[u<sub>k+1</sub> + β<sub>k</sub>(u<sub>k+1</sub>−x<sub>k</sub>)]</div><p>x：基础点；y：外推点；u：未裁剪试探点。</p><p>a<sub>k+1</sub> = (1 + √(1+4a<sub>k</sub>²))/2<br>β<sub>k</sub> = (a<sub>k</sub>−1)/a<sub>k+1</sub>；ΠΩ 表示边界处理。</p>',
    'nesterov', '沿当前方向移动，再利用历史位移外推；边界处理限制可行范围。',
    '图示没有触碰边界，此时 u_(k+1)=x_(k+1)，先在 y_k 计算 d，再沿 x_(k+1)−x_k 外推。公式专门保留未裁剪试探点 u，对应当前 CPU 路径先算 nextCoordi 与 nextSLPCoordi、再分别裁剪的顺序。标准 cell 按密度矩形限制在区域边界内；临时锁住的对象跳过更新，并行 I/O 有单独的边界投影。障碍与站点合法性不是这里的一次坐标裁剪就能完全解决的。经典凸优化收敛率不能直接移植到动态权重的非凸布局问题。', 'coord loop')

add('04 / 数值优化', '读代码时，分清 Cur / SLP / Next 的身份', 'STATE MAP · 数学变量到 C++ 状态',
    '<table><tr><th>数学角色</th><th>主要源码字段</th></tr><tr><td>x<sub>k</sub></td><td>curCoordi_</td></tr><tr><td>y<sub>k</sub></td><td>curSLPCoordi_</td></tr><tr><td>d(y<sub>k</sub>)</td><td>curSLPSumGrads_</td></tr><tr><td>x<sub>k+1</sub> / y<sub>k+1</sub></td><td>nextCoordi_ / nextSLPCoordi_</td></tr></table><p>试探点计算新场和新力后，接受迭代，再轮换缓冲区。</p>',
    'states', '几何、pin 位置、密度场和梯度，必须对应同一轮坐标。',
    'SLP 坐标对应 Nesterov 外推序列，是核心梯度评估点。prev/cur/next 成套出现，是为了估计步长、试探下一点和避免重复分配。updateNextIter 使用 swap 轮换状态，因此调试时要先确认采样位置在交换之前还是之后。GCell 的 density center、GPin 的坐标和 bins 也必须更新到同一状态；只改一份坐标数组可能让 wirelength 与 density 在不同布局上计算。这个一致性原则在 GPU 设备驻留路径上尤其重要。', 'coord grad phi')

add('04 / 数值优化', '实验 ③：加速从何而来，又为何会越过最优点', 'INTERACTIVE · 二维二次函数，不运行 GPL',
    '<div class="equation compact">f(x,y) = ½(x² + 12y²)</div><p>同一起点 (8,4)、同一步长 α = 1/12。</p><p>比较普通梯度下降与 Nesterov；每次点击执行一轮。</p><div class="lab-buttons"><button id="opt-step">前进一步</button><button id="opt-reset">重置</button></div><div id="opt-result" class="readout"></div><p class="small">凸二次示例仅演示动量，不包含 GPL 的密度、预条件与反馈。</p>',
    'optlab', '加速常能更快穿过平缓方向，但它不是每步单调下降的保证。',
    '函数两个方向曲率相差 12 倍，所以梯度下降步长受陡峭的 y 方向限制，x 方向推进较慢。实验使用固定稳定步长，显示真实计算得到的路径与 f 值，最多 40 步。Nesterov 的外推能加快平缓方向的推进，也可能跨过最优点并振荡。它不是布局性能对比，更不意味着实际 GPL 必然比另一求解器快某个倍数。让听众在第 10、15、20 步观察当前位置与历史轨迹，区分“加速”和“单调”。', 'coord loop', lab='optimizer')

add('04 / 数值优化', '步长来自局部变化，而不是一次设定后不再改变', 'BACKTRACKING · 用坐标差 / 力差估计尺度',
    '<div class="equation compact">α̂ ≈ ‖y<sub>new</sub>−y<sub>old</sub>‖₂<br>　　 / ‖d<sub>new</sub>−d<sub>old</sub>‖₂</div><p>试探新坐标 → 重算场和力 → 比较新旧步长。</p><p>力变化很大：局部更陡，需要较小步长。</p><p>零分母、NaN、Inf 和试探上限都需要保护。</p>',
    'backtracking', '这里不是基于目标值的标准 Armijo line search。',
    'getStepLength 返回 coordinateDistance / gradientDistance，采用局部 Lipschitz 尺度的倒数估计。nesterovUpdateStepLength 比较 newStepLength 与 0.95·stepLength；新值较小时继续试探，过小值有 0.01 的下界处理，非法值触发发散。多 region 的聚合退出逻辑还要参考 doBackTracking，不能把一个 region 的布尔返回值直接读成全局收敛。因为合成力包含预条件且模型会变化，公式是工程估计，不是精确全局 Lipschitz 常数。', 'step backtrack')

add('04 / 数值优化', '把一轮循环展开：昂贵工作发生在哪里', 'ONE ITERATION · 数据依赖优先于函数名字',
    '<ol><li>计算动量系数，生成试探坐标。</li><li>更新 pin / bin，完成 WA 与 Poisson。</li><li>合成力，估计步长；必要时重试。</li><li>接受状态，更新 overflow、λ 与平滑系数。</li><li>触发时序 / 拥塞反馈，检查收敛与异常。</li></ol>',
    'iteration', '优化运行时间时，先统计每轮算了几次场、多少次反馈与重启。',
    '这里按算法依赖组织源码阅读，而不是逐个列举 API。原始坐标改变会影响 pin 位置、net 包围盒、指数和、bin 重叠与电场，必须按顺序刷新。Backtracking 的每一次重试都可能重复这些热点工作。Timing repair 可能改变拓扑与面积；routability inflation 可能要求恢复早期位置并再次展开。因此只比较 Nesterov 外层迭代次数会遗漏主要成本。正确的 profile 应区分 wirelength、scatter、FFT、gather、时序、拥塞以及数据同步。', 'loop backtrack')

add('04 / 数值优化', '快照与回退：保存的是一致状态，而非一张坐标表', 'ROBUSTNESS · 处理模型变化和发散',
    '<p>快照可能涉及坐标、梯度、罚系数、动量与线长平滑系数。</p><p>低 overflow 附近出现退化时，检查已保存的较好解。</p><p>拥塞反馈还需要管理虚拟尺寸、filler 与目标密度。</p><p>NaN / Inf 是异常信号；达到迭代上限也不等于成功收敛。</p>',
    'snapshot', '恢复后如果状态来自不同轮次，再好的坐标也无法保证下一步正确。',
    '发散快照与 routability snapshot 是不同目的的机制，不应混用。前者试图在已接近低 overflow 后发生恶化时恢复可用解，后者为面积膨胀后的重新展开提供起点。当前代码还支持增量阶段的可恢复发散窗口，但常规运行仍需明确报告失败。调试时重点检查恢复前后哪一份状态更新了、是否重算梯度、是否重新估计步长，以及 GPU host/device 镜像是否新鲜。不能简单地把某条发散消息理解为一定是密度过高。', 'revert routeloop')

add('04 / 数值优化', '真实回归曲线：展开使 HPWL 上升，overflow 下降', 'EVIDENCE · simple01.ok 的已有 golden 数据',
    '<div class="metrics"><p><b>0.8655 → 0.0990</b><br>密度 overflow</p><p><b>1829.304 → 2594.019 μm</b><br>迭代日志中的 HPWL</p><p><b>235</b> 次迭代<br>本例目标 overflow = 0.1</p></div><p class="small">最终 DB 报告 HPWL = 2597.56 μm，口径不同；未在本次重新运行。</p>',
    'logchart', '收敛判据主要看各 region 的 overflow；仍需检查后续合法化与布线质量。',
    '数据逐行提取自固定提交的 test/simple01.ok，不是本次测量。simple01.tcl 使用 skip_initial_place，并设置 init_density_penalty 为 0.01；不能用此曲线评价所有设计的初始布局策略。曲线分别绘制 HPWL 和 overflow，避免双轴造成视觉误导。最后一次迭代 HPWL 与 Final HPWL 的差别来自内部模型与最终数据库评估口径，不能合并为同一数值。当前 checkConvergence 对每个 region 判断 unscaled overflow，主循环要求全部区域完成。', 'golden converge')

add('05 / 时序反馈', '时序驱动：让关键连接更有“拉力”', 'TIMING LOOP · 布局位置改变关键性',
    '<p>位置 → 估计寄生 → STA / resizer → net slack。</p><p>选出较关键的 nets，增加它们在线长目标中的权重。</p><p>后续优化缩短关键连接，再评估新的关键路径。</p><p>反馈在 overflow 阶段条件下触发，不是每轮完整跑 STA。</p>',
    'timing', '关键路径是动态的：布局改变延迟，延迟又改变布局优先级。',
    'TimingBase 调用 resizer 获取 slack，当前模型将较差 slack 对应的 net 赋予较高 timing weight。它不是直接对完整电路路径延迟求解析梯度，而是通过加权线长作为代理进行反馈。wirelength force 因 net 权重增大而增强，这可能牺牲部分非关键线长，并在关键区域形成新的密度压力。物理 RC、约束完整性与 clock 模型决定反馈是否有意义。时序条件触发代码与权重公式分布在 NesterovPlace 和 TimingBase 两处。', 'timing tdloop')

add('05 / 时序反馈', '从 slack 到 net 权重：线性映射的可解释例子', 'REWEIGHTING · 在选中的关键 net 集合内',
    '<div class="equation compact">ω(s) = 1 + (ω<sub>max</sub>−1)<br>　　　 · (s<sub>max</sub>−s)/(s<sub>max</sub>−s<sub>min</sub>)</div><p>例：s<sub>min</sub> = −100 ps，s<sub>max</sub> = 0，ω<sub>max</sub> = 5。</p><p>slack −100 / −50 / 0 ps<br>对应权重 <b>5 / 3 / 1</b>。</p>',
    'weights', '未获得有效 slack 或未进入加权范围的 net 保持基础权重。',
    '先重置 timing weight 为 1，再对有多个 pin 且存在 slack 的 net，根据关键集合的 slack 范围映射。s_max 是选中集合的边界，不必等于 0；图中的 0 是教学设定。源码只对 net_slack 小于 slack_max 的 net 尝试加权，相同 slack 等退化情形不能照公式直接除零。Timing weight 还可能与 custom weight 合成 total weight。加权后的目标不同于报告的原始 HPWL，因此 HPWL 上升但时序改善完全可能。', 'timing')

add('05 / 时序反馈', 'Resizer 不只提供分数，也可能改变优化对象', 'MODEL MUTATION · 拓扑和面积会变',
    '<p>换 cell master → 面积和 pin offset 改变。</p><p>插入 / 删除实例与 net → 索引和连接关系改变。</p><p>虚拟分析可回滚修改；保留修改时，GPL 必须同步更新内部对象与面积预算。</p>',
    'mutation', '一次 timing feedback 后，旧的指针、梯度与 filler 预算可能都已失效。',
    'run_journal_restore 决定是否恢复 resizer journal；NesterovPlace 依据 overflow 与 keepResizeBelowOverflow 条件选择行为。默认值是本分支版本细节，演示不把某种配置假设成必然行为。保留修改需要 db callbacks 更新 GCell/GPin/GNet，并修复引用与布局状态。面积改变后 density、filler、预条件也要保持一致。实验性 repair_timing 在当前文档中仍被标为 experimental，不应因为存在入口就推定已经适合所有生产流程。', 'timing tdloop model')

add('05 / 时序反馈', '时序结果的可信度，取决于评估模型', 'CORRELATION · 从 placement 到 routed timing',
    '<p>早期位置估计不了所有绕线、拥塞、层选择与 via。</p><p>实际 CTS 尚未完成，时钟延迟模型会改变关键路径。</p><p>当前分支的 Virtual CTS 可临时注入时钟插入延迟，结束前移除。</p><p>最终比较必须跟踪到同一后续阶段的 WNS / TNS。</p>',
    'timinglimits', '改善 placement slack 是中间信号；布线后结果才验证代理是否有效。',
    'WNS 是最差负裕量，TNS 是负裕量总和；如果报告使用不同约束、corner、寄生或 endpoint 集合，就不能直接比较。Virtual CTS 是建模扩展，不是真实插入和布线时钟树，也不能替代 CTS。该能力与 GPU、增量恢复等一样，需要按固定源码版本理解。设计缺失库、RC 或约束时，先修评估基础，再讨论 net 权重是否合适。避免通过单独调大关键 net 权重去掩盖模型不一致。', 'clock tdloop overview')

add('06 / 拥塞反馈', 'RUDY 快速估需求，GRT 提供更具体的路由反馈', 'ROUTABILITY · 两种估计路径',
    '<table><tr><th>RUDY</th><th>GRT</th></tr><tr><td>按 net 包围盒分摊需求</td><td>使用全局布线资源与结果</td></tr><tr><td>适合快速反复评估</td><td>包含更具体的绕路与容量信息</td></tr><tr><td>几何代理，有盲区</td><td>成本较高，仍非详细布线</td></tr></table><p>当前 GPL 默认走 RUDY，可选择 GRT。</p>',
    'rudy', '反馈越真实通常越昂贵；两种估计都需要后续详细布线验证。',
    '对包围盒宽 w、高 h 的 net，可用 (w+h)/(wh) 理解 RUDY 的基础需求密度直觉，但实际 OpenROAD RUDY 还有线宽、tile 重叠、单位和退化 box 处理，不应将此式当作完整实现。GRT 用路由边的 usage/capacity 来估拥塞，并考虑可用层与邻边信息。无论使用哪条路径，反馈都不是 detailed router 的 pin access 和全部 DRC 的完全模型。图中的线只说明 bbox 上的需求分摊与绕障路径的区别。', 'route overview')

add('06 / 拥塞反馈', '宏块通道：短线长方案可能把问题集中到一条缝', 'CASE STUDY · 原理示意，不是实测结果',
    '<p>紧凑聚类使大量跨组连接争用中间通道。</p><p>适当分散单元，可让连线从更多位置通过。</p><p>若通道容量先天不足，仍需修改 floorplan 或宏块位置。</p>',
    'channel', '算法可以重新分配需求，却无法凭空创造 routing capacity。',
    '用左右两组单元与中间两块宏解释拥塞的几何来源。箭头代表希望改善的布局方向，不表示算法保证找到这样的结果。缩小同组内距离可能同时增加跨组连线的重叠，因此 HPWL 与拥塞不是严格同向的。单元膨胀可以增加局部留白并改变连接分布，但固定宏块把通道彻底堵住时，单靠 cell spreading 的自由度不够。应将这种结构问题与数值不收敛、密度参数不合适区分。', 'route inflate')

add('06 / 拥塞反馈', 'RC metric 关注最拥塞的尾部，而非全芯片平均', 'TAIL METRIC · 热点不能被大片空白稀释',
    '<p>把拥塞值排序，分别取最高 <b>0.5%、1%、2%、5%</b> 的平均。</p><div class="equation compact">RC = Σ kⱼ·RC<sub>top-j</sub> / Σ kⱼ</div><p>GRT 路径还比较水平 / 垂直方向的尾部值。</p><p class="small">此处 RC 指 routing congestion，和电学 R、C 参数不是同一概念。</p>',
    'tail', '评价指标决定优化重点；全局均值可能掩盖少量致命热点。',
    '当前 updateRudyAverage 与 getGrtRC 分别统计拥塞尾部；GRT 在各百分位使用水平和垂直统计中较大者再加权。具体参与统计的 tile/edge 过滤、容量为零时的处理、层范围以及百分位取整，都属于指标定义的一部分。RC 接近目标不等价于没有任何局部违例。不能直接比较不同估计器、不同资源设置或不同统计口径的 RC。图中排序条形是教学数据，只用来说明尾部均值为何对热点敏感。', 'rc route')

add('06 / 拥塞反馈', '膨胀：让拥塞区域的 cell 在模型里“更占地方”', 'INFLATION · 从 routing 信息到 density 力',
    '<div class="equation compact">r = min(r<sub>max</sub>, (c/c₀)<sup>p</sup>)，c ≥ c₀<br>w′ ≈ w√r，h′ ≈ h√r</div><p>c：tile 拥塞；c₀：膨胀阈值；r：面积倍率。</p><p>真实 master 尺寸不因这种膨胀而改变。</p><p>新增虚拟面积先消耗 filler / 空间预算。</p>',
    'inflation', '拥塞膨胀增加模型面积；密度平滑只是重新分布同一面积。',
    'updateTileInflationRatio 用相对阈值的幂函数并设上限。RouteBase 仅对符合条件的标准单元执行面积膨胀，依据 cell 的 density center 所在 tile 取比例，并对新宽高四舍五入到整数 DBU。膨胀后调用面积预算与 filler 处理，再让密度力把单元推开。这里不等价于 resizer 的真实 upsizing，后者会换 master 并改变电学属性。受舍入影响，实际面积倍率不一定精确等于 r。', 'inflate cellinflate')

add('06 / 拥塞反馈', '实验 ④：拥塞比例如何转化为面积压力', 'INTERACTIVE · 使用当前分支的膨胀公式',
    '<p>c₀ = 0.95，p = 2，r<sub>max</sub> = 3。<br>教学 cell 尺寸：100 × 60 DBU。</p><div class="control"><label for="congestion">tile 拥塞 c</label><input id="congestion" type="range" min="0.7" max="2" step="0.05" value="1.2"><output id="congestion-value">1.20</output></div><div id="inflation-result" class="readout"></div><p class="small">只计算一次膨胀；单元中心保持不变，不模拟后续重新布局。</p>',
    'inflationlab', '面积倍率为 r，边长倍率为 √r；不要把两者都乘 r。',
    '先设 c 小于 0.95，观察没有膨胀。超过阈值后面积逐渐增加，接近 c≈1.645 时达到 r=3 的上限。实验同时显示理论面积倍率与整数尺寸四舍五入后的实际倍率，对应源码的 round 行为。图中实心矩形是原始尺寸，橙色轮廓是模型尺寸；虚线为同一中心。这个实验不包含多轮累计预算、不同 cell 所在 tile 的变化、filler 削减以及快照恢复，所以无法用它预测某个设计最终拥塞下降多少。', 'inflate cellinflate', lab='inflation')

add('06 / 拥塞反馈', '膨胀之后必须重新展开，必要时恢复较好的状态', 'ROUTABILITY LOOP · 成本与收益的闭环',
    '<p>达到合适阶段 → 估拥塞 → 更新最佳记录。</p><p>若仍需优化：膨胀、调整 filler / 密度，恢复布局快照继续 Nesterov。</p><p>达到目标、预算受限或连续不改善时，结束或回退。</p><p>当前分支还检查移动是否稳定，避免在高速迁移时采集失真的拥塞反馈。</p>',
    'routeloop', '位置快照与最佳拥塞的尺寸 / 权重记录，是两套相关但不同的状态。',
    'NesterovPlace 管理早期位置快照与迭代重启；RouteBase 保存较好拥塞对应的尺寸、target density、filler 和 net 权重。不能简单描述为“恢复最低 RC 的完整坐标解”。当前分支还有 weightCongestedNets：在 RUDY 路径且相关设置启用时，依据热点需求贡献增加部分 net 的线长权重，试图收缩其需求包围盒。移动稳定性门控、累计膨胀预算、无改善退出同样是此版本的增强。读该路径需跟踪两个类的返回值与恢复操作，不能只看 setSize。', 'route routeloop')

add('07 / 源码与实践', '源码只需要先认清四个核心责任', 'ARCHITECTURE · 围绕算法数据组织阅读',
    '<p><b>PlacerBase</b>：从 OpenDB 提取几何、连接和区域。</p><p><b>NesterovBaseCommon</b>：全局 GCell / GPin / GNet 与线长计算。</p><p><b>NesterovBase</b>：每个 region 的 bins、filler、密度与迭代状态。</p><p><b>NesterovPlace</b>：协调迭代、时序、拥塞、收敛和写回。</p>',
    'architecture', '按“谁拥有数据、谁改变状态、谁发起重算”读代码。',
    '这些层次不是简单的数据库对象复制。PlacerBase 负责从数据库建立适合布局的结构，Nesterov 模型进一步包含虚拟尺寸、filler、聚类对象与数值状态。Common 层让跨区域 net 在统一连接图里计算线长，各 region 则独立持有密度网格和求解状态。Replace 提供更上层编排，但本演示不展开入口注册和参数传递，因为它们不是理解算法的主要障碍。找问题时先确定错误在哪一层产生，再追踪下游使用者。', 'pb model loop')

add('07 / 源码与实践', '多 region：线长全局耦合，密度在各自区域求解', 'REGIONS · 不能用总平均遮住局部失败',
    '<p>跨区 net 仍连接不同区域的 pins，线长力需要共同计算。</p><p>每个 region 有自己的 bins、filler、λ 和 overflow。</p><p>主循环协调全部 region；全部满足条件才能正常结束。</p><p>宏块、边界与非矩形可用空间需要正确建模。</p>',
    'regions', '某个小 region 的容量错误，可能影响整个设计的收敛。',
    'NesterovBase 对应 placement domain，通常包括 top-level 与 power domain/group。region 不等于一个与外界完全断开的独立网表；跨域连接仍要产生全局线长梯度。主循环对各 region 求 overflow 平均用于某些调度，真正结束则要逐个检查。调试区域相关问题时，核对成员归属、固定背景、可用面积、约束边界与 bin 索引，而不是只提高总迭代数。图用两个矩形区域作示意，实际可用几何还要通过障碍等结构表达。', 'pb loop converge')

add('07 / 源码与实践', 'CPU / GPU：数学算子相同，数据新鲜度成为重点', 'BRANCH EXTENSION · GPU 后端按本分支理解',
    '<p>热点：WA / HPWL、面积 scatter、FFT、密度 gather、向量更新。</p><p>设备驻留减少逐轮 host/device 往返。</p><p>时序修改、可视化、快照和最终写回需要明确同步边界。</p><p>验证质量、数值容差与可重复性；不能只看 kernel 时间。</p>',
    'gpu', '这份演示不提供 GPU 加速比：没有本次端到端测量证据。',
    '当前工作区包含策略接口和设备驻留 Nesterov 上下文，这些是指定 fork 的实现，不能推定上游所有版本都具备。CPU 路径始终可用，GPU 需要相应构建与运行环境。更新 topology 或 cell 面积后，device net weights、pin maps、density 参数和坐标都可能需要刷新。并行规约的加法次序影响浮点结果，应依据实际后端设置一致性要求。性能实验需要包括数据准备、迭代次数变化、反馈调用与传输成本，并同时评估最终 QoR。', 'gpu grad fft')

add('07 / 源码与实践', '增量布局：先处理新增对象，再决定是否继续松动', 'BRANCH EXTENSION · 已放置不等于始终固定',
    '<p>当前两阶段路径：先锁住已有 PLACED 实例，放置未放置对象。</p><p>阶段一后解除临时锁；若发散或未达到目标，则继续第二阶段。</p><p>第二阶段可加强密度罚项；永久 fixed 对象仍按固定语义处理。</p><p>全已放置等情形有不同分支，不能套用同一流程。</p>',
    'incremental', '“增量”描述重用已有布局的策略，不承诺所有旧单元零位移。',
    '本页严格按 doIncrementalPlace 的当前两阶段代码描述：首次建立模型时临时锁住 PLACED 实例，阶段一有迭代预算并允许特定发散转入阶段二；随后解除临时锁。只有阶段一发散或未达到目标时才显式继续第二阶段，避免误讲成无条件重跑全局优化。阶段二没有相同的发散回退窗口。若需要定位增量问题，要核对 placement status、锁语义、filler 重新分布和 penalty guard，而不是把所有不移动对象都当成数据库 FIXED。', 'incremental')

add('07 / 源码与实践', '读日志：先定位机制，再调整参数', 'DIAGNOSIS · 症状不是根因',
    '<table><tr><th>观察</th><th>优先检查</th></tr><tr><td>overflow 长期不降</td><td>可用面积、region、锁、密度力与 λ</td></tr><tr><td>HPWL 突然跳变</td><td>TD 修改、RD 重启、快照、权重</td></tr><tr><td>步长 NaN / Inf</td><td>零力差、非法面积 / 坐标、尺度</td></tr><tr><td>低密度但 routing 失败</td><td>宏通道、pin access、资源与拥塞</td></tr></table>',
    'diagnosis', '把异常追到产生错误状态的那一步，再看输出和日志。',
    '例如最终位置异常，应该从坐标更新、锁、DB callbacks 或快照恢复追起，而不是只改 DEF 写出。overflow 变差可能是模型面积增加后的正常短期反应，也可能是重复计入障碍或区域成员错误。比较事件前后的 HPWL、overflow、penalty、area 与触发次数，比孤立地看一行日志更有效。先缩小到普通模式、单 region 和小设计，再逐步加 TD、RD、GPU 等维度，能更快找出导致分歧的机制。表格给的是检查顺序，不是唯一根因。', 'loop revert overflow')

add('07 / 源码与实践', '评价一次改动：让早期收益走到后续流程', 'EXPERIMENT DESIGN · 控制变量与一致口径',
    '<p>固定输入网表、floorplan、库 / RC / SDC、seed、线程与版本。</p><p>每次只改变一个因素：普通 GPL → TD → RD → 组合。</p><p>记录 GPL 曲线与时间，也跟踪 DPL 位移、GRT 拥塞、DRT 违例和 routed WNS / TNS。</p>',
    'qor', '更低 HPWL、更快收敛、更好 routed timing，是三个需要分别验证的结论。',
    '建立基线时保留输入快照与工具提交，防止比较过程中库、floorplan 或 resizer 设置悄悄变化。性能应报告硬件、线程、GPU 设置、重复次数和端到端时间；质量必须在相同后续阶段比较。TD 可能改变实例数和真实面积，RD 改变模型面积，二者不要合并成同一个面积指标。对于多目标权衡，报告 HPWL、拥塞、时序、面积与运行时间的共同变化，不用某一个指标宣称全面改善。没有测量就不给出加速或 QoR 百分比。', 'overview tests')

add('07 / 源码与实践', '三个练习，让新人从“听懂”走向“能定位”', 'HANDS-ON · 用现有回归建立最小闭环',
    '<ol><li><b>读曲线：</b>从 simple01.ok 找一次 HPWL 上升与 overflow 下降，解释为什么合理。</li><li><b>跟踪一次力：</b>从一个 GPin 的 WA 导数追到 GCell 更新，确认符号和预条件。</li><li><b>跟踪一次膨胀：</b>记录尺寸、filler、overflow 和快照在 RD 前后的变化。</li></ol><p class="small">有构建环境时，从 src/gpl/test 的小用例开始；测试输出放入独立结果目录。</p>',
    'exercises', '每个练习都应有可检查的答案或数据，而不只是“成功跑完”。',
    '当前环境没有现成的 build/src/openroad，因此本次演示使用仓库已有 golden，而未声称重新跑通 OpenROAD。练习一无需编译；练习二可结合断点和小设计；练习三建议先确认 baseline 再单独启用 RD。运行现有 Tcl 用例需遵守 OpenROAD test helpers 的工作目录与依赖约定，不要直接复制一个裸命令并假设所有路径都能解析。若后续为 GPL 添加回归，项目要求在 CMake 与 Bazel 两处登记；这里不把测试基础设施当作算法章节展开。', 'tests golden')

add('07 / 源码与实践', '源码阅读顺序：每次只回答一个问题', 'SOURCE MAP · 所有链接固定到同一提交',
    '<table><tr><th>问题</th><th>入口</th></tr><tr><td>起点如何得到？</td><td>initialPlace.cpp → solver.cpp</td></tr><tr><td>线长力来自哪里？</td><td>updateWireLengthForceWA_native</td></tr><tr><td>空间力来自哪里？</td><td>BinGrid → FFT → getDensityGradient</td></tr><tr><td>位置如何更新？</td><td>doNesterovPlace → nesterovUpdateCoordinates</td></tr><tr><td>物理反馈如何介入？</td><td>TimingBase / RouteBase</td></tr></table>',
    'reading', '先建立公式与状态的对应关系，再读异常路径和后端优化。',
    '建议第一次阅读只看普通标准单元 CPU 路径，画出坐标、pin、bin 和力的依赖。第二次加入 fixed macros 与 region；第三次加入 TD 和 RD，因为这时优化对象本身会变化。最后再追 GPU 的缓存与同步、incremental 的临时锁和恢复路径。每页脚注给出实际源码入口，而不是只链接仓库首页。当前代码会继续演化，使用本演示的 commit 链接可避免打开 master 后行号和行为变化。', 'ip wa scatter fft loop timing route')

add('附录 / 自测', '用五个问题检查是否真的理解了 GPL', 'REVIEW · 答案在讲解稿中',
    '<ol><li>为什么 HPWL 上升时，布局可能正在改善？</li><li>为何 filler 参与密度，却不计入 overflow 分子？</li><li>密度平滑和拥塞膨胀分别守恒什么？</li><li>源码为什么用“加梯度”更新坐标？</li><li>为什么低 overflow 不能保证布线成功？</li></ol>',
    'questions', '能用“公式 + 图 + 源码位置”解释这些问题，就已经掌握主要框架。',
    '答案一：展开减少重叠需要更长连接，目标包含密度和物理反馈，HPWL 不是唯一目标。答案二：filler 用来平衡目标容量与真实实例面积，并不代表真实布局冲突。答案三：密度平滑扩大支撑但用缩放保持模型面积；RD 膨胀故意增加虚拟面积，真实 master 不变。答案四：wirelength 的实现返回 min 导数减 max 导数，已是负梯度，density 返回电场力。答案五：routing 容量、拓扑、障碍、层和 pin access 与 cell 面积容量不同。', 'waderiv smooth scatter inflate')

add('附录 / 记号', '把几组容易混淆的名词放在一起', 'NOTATION · 数学含义优先',
    '<table><tr><th>记号 / 概念</th><th>含义</th></tr><tr><td>γ / wlCoeff</td><td>线长平滑尺度 / 其倒数形式</td></tr><tr><td>λ / densityPenalty</td><td>密度项的相对强度</td></tr><tr><td>ψ / phiCoef</td><td>电势 / λ 更新倍率，两者不同</td></tr><tr><td>α / β</td><td>步长 / Nesterov 动量倍率</td></tr><tr><td>bin / routing tile</td><td>放置密度网格 / 布线评估网格</td></tr><tr><td>scaled / unscaled</td><td>实现中的面积与 overflow 路径，不等于有 / 无目标密度</td></tr></table>',
    'notation', 'overflow 是比例，HPWL 是长度，area 是面积；比较前先核对单位与归一化。',
    '尤其要注意 unscaled 这个名字：当前 scatterDensityAreaInPlace 在宏块面积上仍乘 targetDensity，不代表这里完全没有任何缩放。固定背景同样有专门处理。DBU 是数据库长度单位，面积相应为 DBU²，输出微米和平方微米需要不同转换。目标密度、overall utilization、放置 overflow 和 routing congestion 是四个不同指标；把它们全部叫“密度”会让讨论失去精确性。符号表是阅读辅助，不替代具体源码中的条件分支。', 'scatter overflow coef phi')

add('附录 / 资料', '源码基线、证据和延伸阅读', 'PROVENANCE · 可追溯比版本名更可靠',
    '<p><b>实现基线</b><br>zint99/OpenROAD<br><code>977813f3b02e35692b7b5ab3cca36e4e6fa380bb</code></p><p><b>算法背景</b><br>Lu et al. · ePlace · TODAES 2015<br>Cheng et al. · RePlAce · TCAD 2019</p><p><b>实数证据</b><br>simple01.ok / simple01.defok / nangate45.lef</p><p class="small">交互例子是教学公式；未提供新的 OpenROAD 性能测量。</p>',
    'provenance', '论文解释思想，固定版本源码解释当前行为；两者不能逐项画等号。',
    'ePlace 介绍基于静电场和 Nesterov 的分析式布局框架；RePlAce 讨论质量与可布线性改进。本演示主要依据当前源码重新推导并绘制原理图，不复刻论文图表，也不把论文的全部公式、历史局部密度机制或 benchmark 收益套到现在的 fork。当前分支的 GPU、Virtual CTS、incremental guard 与拥塞门控等增强只按固定提交描述。source-index.html 集中列出所有入口，data 目录保留提取的回归数值与几何，便于复核和更新。', 'eplace replace golden def')

add('收束', '从连接图到位置场，再回到真实芯片', 'GPL · THE COMPLETE MENTAL MODEL',
    '<p class="hero-copy">连接告诉我们靠近谁。<br>密度告诉我们空间在哪里。<br>物理反馈告诉我们哪些位置更有价值。</p><p>Nesterov 把这些信息变成一轮轮可计算的位移。</p><p class="small">下一步：选一条 net、一个 cell、一个 bin，追完一整轮数据流。</p>',
    'final', '理解 GPL 的核心，是理解每次移动背后的信息、尺度和状态。',
    '结束时回到最初的两种力，再加上时序和拥塞这两条反馈。网表不是一堆要随机塞进矩形的方块，而是一个连接图；密度场不是最终合法化，而是连续优化中的空间信号；早期物理评估不是最终真值，但能逐步修正代理目标。掌握这些关系后，初始布局、WA、Poisson、Nesterov、filler、TD、RD 和源码状态就能串成完整过程。提醒听众打开逐页讲解稿和源代码索引，继续沿最小样例验证理解。', 'loop grad timing route', theme='dark')

assert len(SLIDES) == 56
