"""Original SVG teaching figures; only real/logchart use extracted golden data."""
from html import escape
from pathlib import Path
import json
import math

TEAL='#087e83'; ORANGE='#cb613c'; INK='#1d3639'; MUTED='#627976'
PALE='#d7e9e3'; LINE='#c7d4cd'; BLUE='#426eaa'; GOLD='#b39142'
DATA=json.loads((Path(__file__).parent/'data/simple01.json').read_text())

def text(x,y,value,size=18,color=INK,anchor='start',weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(value))}</text>'

def rect(x,y,w,h,fill=PALE,stroke='none',rx=3,opacity=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" opacity="{opacity}"/>'

def line(x1,y1,x2,y2,color=LINE,width=2,dash=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>'

def arrow(x1,y1,x2,y2,color=TEAL,width=2.5):
    a=math.atan2(y2-y1,x2-x1); l=10
    p1=(x2-l*math.cos(a-.45),y2-l*math.sin(a-.45));p2=(x2-l*math.cos(a+.45),y2-l*math.sin(a+.45))
    return line(x1,y1,x2,y2,color,width)+f'<polygon points="{x2},{y2} {p1[0]},{p1[1]} {p2[0]},{p2[1]}" fill="{color}"/>'

def dot(x,y,r=6,color=TEAL):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'

def box(x,y,w,h,title,sub='',color=TEAL):
    return rect(x,y,w,h,'#edf2ea',LINE,6)+rect(x,y,4,h,color)+text(x+18,y+32,title,21,color,weight=650)+(text(x+18,y+60,sub,15,MUTED) if sub else '')

def grid(x,y,w,h,n=8,m=6):
    s=rect(x,y,w,h,'#f6f5ee',LINE)
    for i in range(1,n):s+=line(x+w*i/n,y,x+w*i/n,y+h,LINE,1)
    for i in range(1,m):s+=line(x,y+h*i/m,x+w,y+h*i/m,LINE,1)
    return s

def path(points,color=TEAL,width=3):
    return f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in points)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"/>'

def caption(value):return text(340,413,value,15,MUTED,'middle')

def chips(x,y,n=25,spread=True,color=TEAL):
    s=''
    for i in range(n):
        xx=x+(i%5)*(39 if spread else 12)+((i*7)%13)
        yy=y+(i//5)*(31 if spread else 11)+((i*11)%9)
        s+=rect(xx,yy,28+(i%3)*4,18,color,'#ffffff',2,.75)
    return s

def flow(labels,colors=None):
    s=''; n=len(labels); w=550 if n<4 else 560
    if n<=4:
        for i,(a,b) in enumerate(labels):
            y=25+i*88;s+=box(80,y,520,70,a,b,(colors or [TEAL]*n)[i])
            if i<n-1:s+=arrow(340,y+71,340,y+85)
    else:
        for i,(a,b) in enumerate(labels):
            col=i%2;row=i//2;x=30+col*330;y=35+row*120
            s+=box(x,y,290,88,a,b,(colors or [TEAL]*n)[i])
            if i%2==0:s+=arrow(x+293,y+43,x+323,y+43)
    return s

def figure(name,idx,title):
    s=''; note='原理示意 · 非实测运行'
    if name=='real':
        sc=10.6; x0=173;y0=45
        s+=rect(x0,y0,30.97*sc,30.8*sc,'#173b40','#6ba89e')
        for c in DATA['cells']:
            s+=rect(x0+c['x']*sc,y0+(30.8-c['y']-c['h'])*sc,c['w']*sc,c['h']*sc,'#66c4b7','#173b40',0,.82)
        s+=text(165,27,'GCD / 294 CELLS / NANGATE45',17,'#b8d7ca')
        s+=line(510,45,510,371,'#9bc5ba')+text(529,213,'30.8 μm',16,'#b8d7ca')
        note='已有回归布局重绘 · simple01.defok · 尚未 DPL'
    elif name=='roadmap':
        ys=[60,147,234,321];labs=[('01','直觉与建模','01—07',TEAL),('02','线长 / 密度 / Nesterov','08—34',TEAL),('03','时序 / 可布线性','35—44',ORANGE),('04','源码 / 诊断 / 练习','45—56',BLUE)]
        for y,(num,a,b,c) in zip(ys,labs):
            s+=text(40,y+18,num,38,c)+line(104,y-5,104,y+47,c,3)+text(130,y+12,a,25)+text(130,y+41,b,17,MUTED)
    elif name=='pipeline':
        labs=[('Floorplan','宏块 / 引脚 / rows'),('GPL','整体分布'),('DPL + CTS','合法化 / 时钟树'),('GRT + DRT','全局 / 详细布线')]
        for i,(a,b) in enumerate(labs):
            y=20+i*92;s+=box(80,y,385,73,a,b,TEAL if i==1 else MUTED)
            if i<3:s+=arrow(274,y+74,274,y+89)
        s+=path([(468,332),(602,332),(602,149),(477,149)],ORANGE,2.5)+arrow(515,149,477,149,ORANGE)+text(513,245,'反馈',22,ORANGE)
    elif name=='geometry':
        s+=grid(35,40,600,320,10,8)+rect(430,65,175,110,INK)+text(518,115,'FIXED',22,'#fff','middle')
        s+=rect(175,195,158,76,TEAL)+dot(254,233,5,'white')+text(237,294,'中心 (xᵢ,yᵢ)',17)
        s+=dot(316,210,7,ORANGE)+arrow(258,231,310,213,'#fff',2)+text(322,199,'pin',17,ORANGE)
        s+=dot(48,110,7,ORANGE)+path([(48,110),(120,110),(316,210),(477,175)],ORANGE,2)
        s+=text(42,95,'I/O',16,ORANGE)+text(73,345,'net 连接 pins',18,MUTED)
    elif name=='forces':
        s+=rect(22,40,282,303,'#edf1e8',LINE)+rect(369,40,282,303,'#edf1e8',LINE)
        s+=chips(115,148,25,False)+chips(400,100,25,True)
        s+=arrow(302,185,364,185,ORANGE,4)+text(163,376,'线长优先 → 聚集',21,TEAL,'middle')+text(510,376,'加入密度 → 展开',21,ORANGE,'middle')
        for x,y in [(70,98),(247,105),(67,304),(262,309)]:s+=arrow(x,y,163,202,TEAL,2)
    elif name=='objective':
        s+=text(65,76,'Wγ',70,TEAL)+text(220,73,'+',53,MUTED)+text(303,76,'λD',70,ORANGE)
        s+=box(45,120,260,100,'网表连接','WA · net weights',TEAL)+box(359,120,260,100,'空间资源','bins · Poisson',ORANGE)
        s+=arrow(175,226,285,282,TEAL)+arrow(480,226,380,282,ORANGE)+box(205,290,270,80,'下一次位移','力 + 预条件 + 步长',INK)
    elif name in ('mainflow','iteration'):
        labs=[('模型 / 起点','geometry + connectivity'),('WA 线长力','pin → net → cell'),('密度电场','scatter → solve → gather'),('试探 / 步长','Nesterov + backtracking'),('物理反馈','timing / routability'),('收敛 / 写回','逐个 region 检查')]
        s+=flow(labs,[INK,TEAL,ORANGE,TEAL,ORANGE,INK])
        for y in [140,260]:
            s+=path([(505,y-14),(505,y),(18,y),(18,y+59),(27,y+59)],MUTED,1.6)+arrow(18,y+59,27,y+59,MUTED,1.6)
        s+=text(340,390,'未收敛：带着更新后的模型回到求力步骤',17,MUTED,'middle')
    elif name=='b2b':
        xs=[90,240,370,570]; s+=line(75,295,605,295,MUTED)
        for i,x in enumerate(xs):s+=dot(x,295,9,TEAL)+text(x,330,['min','pin 1','pin 2','max'][i],19,INK,'middle')
        for a,b,h in [(90,240,90),(90,370,140),(90,570,200),(240,570,130),(370,570,80)]:
            s+=f'<path d="M{a},285 Q{(a+b)/2},{285-h*2} {b},285" stroke="{TEAL}" fill="none" stroke-width="2.5"/>'
        s+=line(240,267,370,267,ORANGE,2,'5 5')+text(305,251,'不连接内部–内部',16,ORANGE,'middle')
        s+=text(340,43,'一个方向：只保留与极值端点相连的边',21,INK,'middle')
    elif name=='quadratic':
        for x,lab,c in [(60,'0',INK),(245,'10/3',TEAL),(435,'20/3',TEAL),(620,'10',INK)]:
            s+=dot(x,105,10,c)+text(x,145,lab,22,c,'middle')
        for a,b in [(72,233),(257,423),(447,608)]:s+=line(a,105,b,105,TEAL,3)
        s+=box(70,205,240,118,'矩阵 A','[ 2   −1 ; −1    2 ]',TEAL)+box(370,205,230,118,'右端 b','[ 0 ; 10 ]',ORANGE)
        s+=text(340,366,'Ax = b   →   ∇E = 0',28,INK,'middle')
    elif name=='hpwl':
        x0=76;y0=338;k=61
        s+=arrow(x0,y0,622,y0,MUTED)+arrow(x0,y0,x0,35,MUTED)
        s+=rect(x0+k,y0-4*k,6*k,3*k,'#d7e9e360',TEAL,0)
        for x,y in [(1,1),(3,4),(7,2)]:
            s+=dot(x0+x*k,y0-y*k,8,TEAL)+text(x0+x*k+13,y0-y*k-13,f'({x},{y})',20)
        s+=text(320,365,'Δx = 6',23,TEAL,'middle')+text(32,213,'3',26,ORANGE,'middle')
        s+=text(571,68,'HPWL = 9',22,INK,'middle')
    elif name in ('wa','walab','wagrad'):
        xs=[90,240,590]
        s+=line(65,212,620,212,MUTED)
        for x,v in zip(xs,[0,3,10]):s+=dot(x,212,9,TEAL)+text(x,246,v,22,INK,'middle')
        s+=text(65,55,'μ− 偏向左端',24,TEAL)+text(425,55,'μ+ 偏向右端',24,ORANGE)
        for i,(x,v) in enumerate(zip(xs,[.81,.18,.01])):s+=rect(x-20,185-v*100,40,v*100,TEAL)
        for i,(x,v) in enumerate(zip(xs,[.006,.029,.965])):s+=rect(x-20,270,40,v*92,ORANGE)
        s+=text(340,385,'归一化权重随 γ 改变 · γ = 2',18,MUTED,'middle')
        if name=='wagrad':
            s+=arrow(94,213,158,213,BLUE,4)+arrow(585,213,528,213,BLUE,4)
            note='箭头为负梯度方向 · 图上权重为近似展示'
    elif name=='coef':
        s+=arrow(85,342,620,342,MUTED)+arrow(85,342,85,38,MUTED)
        pts=[]
        for i in range(101):
            ov=1.2*i/100;c=.1 if ov>1 else 10 if ov<.1 else 10**(1-(ov-.1)*20/9)
            pts.append((100+ov*410,323-(math.log10(c)+1)*125))
        s+=path(pts,TEAL,4)
        for val,lab in [(0,'0.1'),(1,'1'),(2,'10')]:s+=text(72,328-val*125,lab,17,MUTED,'end')
        for ov in [0,.1,.5,1,1.2]:s+=text(100+ov*410,370,ov,16,MUTED,'middle')
        s+=text(345,30,'wlCoeff / base（对数轴）',21,TEAL,'middle')+text(587,395,'overflow',17,MUTED,'end')
        note='按 updateWireLengthCoef 的分段公式重绘'
    elif name=='bins':
        s+=grid(55,45,560,300,8,5)
        for j in range(5):
            for i in range(8):
                v=(math.sin(i*.8)+math.cos(j*.9)+2)/4
                s+=rect(56+i*70,46+j*60,68,58,ORANGE if v>.7 else TEAL,opacity=.1+.65*v)
        s+=rect(265,165,70,60,'none',INK)+text(301,202,'tAb',22,'white','middle')
        s+=text(334,382,'深色＝较高占用 · 每格分别计算容量',20,MUTED,'middle')
    elif name=='scatter':
        s+=grid(100,42,400,300,2,2)+rect(232,142,198,139,TEAL,TEAL,0,.35)
        for x,y,lab in [(264,175,'68×50'),(361,175,'130×50'),(263,239,'68×89'),(363,239,'130×89')]:s+=text(x,y,lab,18,INK,'middle')
        s+=line(300,40,300,345,INK,2)+line(98,192,503,192,INK,2)
        s+=text(525,167,'Rᵢ',26,TEAL)+arrow(521,178,434,202,TEAL)
        s+=text(305,383,'Σ overlap = 198 × 139',26,TEAL,'middle')
    elif name=='smoothing':
        s+=grid(30,35,280,300,4,4)+grid(370,35,280,300,4,4)
        s+=rect(141,173,55,29,TEAL)+rect(453,119,108,108,TEAL,TEAL,0,.26)+rect(480,158,55,29,'none',TEAL)
        s+=arrow(314,185,364,185,ORANGE,3)+text(170,377,'小支撑 / 大权重',21,TEAL,'middle')+text(510,377,'大支撑 / 小权重',21,TEAL,'middle')
    elif name=='fillers':
        s+=grid(50,38,560,300,8,5)
        for i in range(44):
            x=68+(i*79)%511;y=57+(i*53)%255
            s+=rect(x,y,24,15,TEAL if i%3==0 else '#d8c991',TEAL if i%3==0 else GOLD,1)
        s+=dot(85,377,7,TEAL)+text(103,383,'真实实例',20)+dot(326,377,7,GOLD)+text(345,383,'虚拟 filler：无 net',20)
    elif name=='obstacles':
        s+=grid(50,40,565,290,8,5)+rect(142,80,235,166,INK,opacity=.78)+rect(276,159,234,126,INK,opacity=.78)
        s+=rect(276,159,101,87,ORANGE,opacity=.85)+text(323,208,'∩',40,'white','middle')
        s+=text(330,367,'A ∪ B = A + B − A ∩ B',29,INK,'middle')
        note='交叠区域只计一次 · 固定背景按实现进行密度缩放'
    elif name=='densitylab':
        vals=[80,20,65,35]
        for i,v in enumerate(vals):
            x=55+i*150;s+=rect(x,65,115,250,'#e2e9df',LINE)+rect(x,315-v*2.5,115,v*2.5,TEAL)
            s+=line(x-5,165,x+120,165,ORANGE,3,'6 4')+text(x+57,345,str(v),24,INK,'middle')
        s+=text(340,35,'容量 = 60 / bin',22,ORANGE,'middle')+text(340,387,'总超额面积 = 25 → overflow = 0.125',23,INK,'middle')
    elif name=='field':
        for j in range(9):
            for i in range(13):
                x=52+i*45;y=42+j*35;dx=x-310;dy=y-182;r=math.hypot(dx,dy)+1
                v=math.exp(-r*r/14000);s+=rect(x-20,y-15,42,32,ORANGE,opacity=.06+.65*v)
                length=7+22*v;s+=arrow(x,y,x+length*dx/r,y+length*dy/r,TEAL,1.6)
        s+=text(340,385,'中心较密 → 周围电场引导疏散',23,INK,'middle')
    elif name=='fft':
        for col,lab in [(0,'ρ 空间域'),(1,'ρ̂ 频域'),(2,'ψ / E 空间域')]:
            x0=25+col*226;s+=text(x0+95,47,lab,21,INK,'middle')
            for j in range(7):
                for i in range(6):
                    if col==0:v=math.exp(-((i-2)**2+(j-3)**2)/5)
                    elif col==1:v=1/(1+i+j)
                    else:v=(math.cos(i*.55)*math.cos(j*.5)+1)/2
                    s+=rect(x0+i*31,78+j*30,28,27,TEAL if col!=0 else ORANGE,opacity=.08+.8*v)
            if col<2:s+=arrow(x0+186,181,x0+219,181,INK)
        s+=box(48,318,584,70,'非零频率：除以 kx² + ky²','(0,0) 模式清零；方向尺度与逆变换归一化相配',ORANGE)
    elif name=='gather':
        s+=grid(60,35,390,300,5,4)
        for j in range(4):
            for i in range(5):s+=arrow(85+i*78,73+j*75,111+i*78,53+j*75,TEAL,2)
        s+=rect(190,131,178,118,ORANGE,ORANGE,0,.25)+arrow(277,190,371,106,ORANGE,5)
        s+=text(490,151,'Σ aᵢb Eᵦ',24,ORANGE)+text(490,183,'面积加权',20)+text(490,213,'合成密度力',20)
        s+=text(256,372,'一个 cell 覆盖多个不同的电场采样点',19,MUTED,'middle')
    elif name in ('twoheatmaps','channel'):
        for col in range(2):
            x=27+col*340;s+=grid(x,43,285,295,6,6)+rect(x+77,43,124,122,INK)+rect(x+77,220,124,118,INK)
            s+=text(x+140,378,'密度占用' if col==0 else '布线需求',23,TEAL if col==0 else ORANGE,'middle')
            if col==0:s+=chips(x+7,172,4,True)
            else:
                s+=rect(x+8,169,270,45,ORANGE,opacity=.15)
                for j in range(7):s+=path([(x+7,60+j*38),(x+68,171+j*6),(x+214,171+j*6),(x+275,60+j*38)],ORANGE,2)
        note='同一通道，两个指标 · 几何与连线均为教学示意'
    elif name=='precondition':
        for y,a,n in [(110,1,3),(260,5,12)]:
            s+=rect(45,y-35,50*a**.5,40*a**.5,TEAL)+text(205,y-10,f'面积 {a} / pins {n}',21)
            s+=arrow(205,y+20,385+a*22,y+20,ORANGE,4)+arrow(485,y+20,595,y+20,TEAL,4)
        s+=text(365,52,'原始合力',23,ORANGE,'middle')+text(548,52,'预条件后',23,TEAL,'middle')+text(427,189,'÷ Pᵢ',30,INK,'middle')
    elif name=='balance':
        s+=text(70,70,'原始力的 L1 总量',25)
        for y,w,lab,c in [(118,430,'‖FW‖₁',TEAL),(204,185,'‖FD‖₁',ORANGE)]:
            s+=rect(80,y,w,37,c)+text(80,y+66,lab,22,c)
        s+=box(80,310,520,78,'按比例设定 λ₀','先匹配量级，再用 c₀ 调整初始偏好',INK)
    elif name=='penalty':
        s+=box(48,50,259,90,'ΔHPWL < 0','密度压力可更积极增长',TEAL)+box(366,50,269,90,'ΔHPWL ≥ 0','按变化量调节 φ',ORANGE)
        s+=arrow(178,145,287,223,TEAL)+arrow(496,145,389,223,ORANGE)+box(205,231,270,95,'λ ← φ × λ','重新平衡两种力',INK)
        s+=path([(475,281),(620,281),(620,368),(58,368),(58,165)],MUTED,2)+arrow(58,165,58,146,MUTED)
    elif name=='nesterov':
        # Last displacement is exactly 0.6 * (x_next - x_current).
        pts=[(70,335),(210,275),(375,200),(558,119)]
        labs=['xₖ','yₖ','xₖ₊₁','yₖ₊₁']
        s+=arrow(*pts[1],*pts[2],TEAL,5)+arrow(*pts[2],*pts[3],ORANGE,5)+line(*pts[0],*pts[2],MUTED,2,'6 5')
        for (x,y),lab in zip(pts,labs):s+=dot(x,y,9,INK)+text(x,y+40,lab,27,INK,'middle')
        s+=text(231,207,'αd(yₖ)',26,TEAL)+text(403,68,'β(xₖ₊₁−xₖ)',24,ORANGE)
        s+=text(340,375,'求力位置与基础迭代点不同',23,INK,'middle')
    elif name=='states':
        for col,a in enumerate(['PREV','CUR','NEXT']):
            x=26+col*226;s+=text(x+91,45,a,23,TEAL,'middle')
            for row,lab in enumerate(['SLP coordinates','WL / density force','sum direction']):s+=box(x,76+row*85,191,65,lab,'',TEAL if row==0 else MUTED)
        s+=arrow(565,351,340,351,ORANGE,4)+arrow(329,351,111,351,ORANGE,4)+text(340,389,'接受后轮换；试探期间先保持旧状态',19,MUTED,'middle')
    elif name=='optlab':
        s+=optimizer_figure(0)
    elif name=='backtracking':
        s+=box(48,46,265,90,'候选步长 α','产生 next 坐标',TEAL)+box(368,46,265,90,'重算力 dnext','估计新步长 α̂',ORANGE)+arrow(317,93,361,93)
        s+=box(185,204,310,90,'步长检查','接受 / 缩小后重试 / 异常',INK)+arrow(499,143,425,197,ORANGE)
        s+=path([(183,250),(71,250),(71,153)],TEAL,3)+arrow(71,153,71,141,TEAL)+text(107,287,'重试',21,TEAL)
        s+=arrow(340,298,340,360,TEAL)+text(340,388,'轮换状态进入下一轮',22,TEAL,'middle')
    elif name=='snapshot':
        for x,y,t,st,c in [(30,45,'位置','基础点 + 外推点',TEAL),(363,45,'数值状态','力 / λ / α / 动量',ORANGE),(30,173,'模型状态','尺寸 / filler / 权重',ORANGE),(363,173,'同步边界','DB / host / device',BLUE)]:s+=box(x,y,283,92,t,st,c)
        s+=line(172,270,172,325,TEAL)+line(500,270,500,325,BLUE)+line(172,325,500,325,INK)+arrow(339,325,339,361,INK)+text(340,392,'恢复一个自洽的优化状态',26,INK,'middle')
    elif name=='logchart':
        rows=DATA['iterations']
        for y0,key,c,low,high,lab in [(46,'overflow',ORANGE,0,1,'密度 overflow'),(232,'hpwl',TEAL,1700,2700,'HPWL (μm)')]:
            s+=text(72,y0-12,lab,20,c)+line(72,y0+125,618,y0+125,MUTED)+line(72,y0,72,y0+125,MUTED)
            for val in [low,high]:s+=text(62,y0+125-(val-low)/(high-low)*125+5,f'{val:g}',16,MUTED,'end')
            pts=[(72+r['iter']/235*540,y0+125-(r[key]-low)/(high-low)*125) for r in rows]
            s+=path(pts,c,3.3)
            for x,y in pts:s+=dot(x,y,2.7,c)
            s+=text(618,y0+148,'235',16,MUTED,'end')+text(72,y0+148,'0',16,MUTED)
        note='来自固定提交 simple01.ok · 25 个日志采样点 · 横轴为迭代'
    elif name=='timing':
        s+=flow([('当前位置 → 估计 RC','确定早期连线延迟'),('STA / resizer → slack','找出较关键的 nets'),('更新 net 权重','改变 WA 线长力'),('继续 Nesterov','位置变化后再次评估')],[TEAL,BLUE,ORANGE,TEAL])
    elif name=='weights':
        s+=arrow(85,340,617,340,MUTED)+arrow(85,340,85,44,MUTED)
        pts=[(104,73),(347,198),(590,323)];s+=path(pts,ORANGE,4)
        for (x,y),lab,w in zip(pts,['−100','−50','0'],[5,3,1]):
            s+=dot(x,y,8,ORANGE)+text(x,371,lab,20,INK,'middle')+text(x+17,y-14,f'ω = {w}',22,ORANGE)
        s+=text(90,27,'net weight',20,ORANGE)+text(586,398,'slack / ps',18,MUTED,'end')
    elif name=='mutation':
        s+=rect(54,115,65,50,TEAL)+rect(213,115,65,50,TEAL)+arrow(122,139,207,139,TEAL)+text(165,75,'反馈前',24,INK,'middle')
        s+=rect(373,114,95,66,TEAL)+rect(520,124,32,35,ORANGE)+rect(594,115,65,50,TEAL)+arrow(470,140,515,140,ORANGE)+arrow(555,140,588,140,ORANGE)+text(513,75,'保留 resize / buffer',22,INK,'middle')
        s+=arrow(329,211,329,257,ORANGE)+box(50,267,579,104,'重建一致性','connectivity → pin offsets → area → filler → forces',INK)
    elif name=='timinglimits':
        s+=flow([('Placement estimate','位置 + 估计寄生'),('CTS / GRT','时钟、路由资源与拓扑逐步具体化'),('DRT / extracted RC','真实绕路、via 与寄生模型'),('统一阶段评价','WNS / TNS / area / violations')],[TEAL,BLUE,ORANGE,INK])
    elif name=='rudy':
        for k in range(2):
            x=40+340*k;s+=grid(x,75,260,245,5,5)+dot(x+24,284,7,TEAL)+dot(x+231,109,7,TEAL)
            if k==0:
                s+=rect(x+24,109,207,175,ORANGE,ORANGE,0,.18)+text(x+130,202,'分摊 bbox 需求',18,ORANGE,'middle')
            else:s+=rect(x+65,134,112,116,INK)+path([(x+24,284),(x+207,284),(x+207,109),(x+231,109)],ORANGE,4)
            s+=text(x+130,47,'RUDY' if k==0 else 'GRT',27,TEAL,'middle')
        s+=text(340,374,'快速几何代理                       带资源与绕路信息',19,MUTED,'middle')
    elif name=='tail':
        for i in range(55):
            v=2.3*math.exp(-i/15)+.1;x=45+i*10.8
            s+=rect(x,326-v*95,8,v*95,ORANGE if i<6 else TEAL,opacity=1 if i<6 else .55)
        s+=line(42,326,640,326,MUTED)+text(50,55,'最高拥塞尾部',23,ORANGE)+arrow(148,65,75,106,ORANGE)
        s+=text(340,370,'从高到低排序 → 取多个尾部区间均值',23,INK,'middle')
    elif name in ('inflation','inflationlab'):
        s+=grid(64,42,550,300,10,6)+rect(235,131,190,114,ORANGE,ORANGE,0,.17)+rect(258,146,145,87,TEAL)+line(330,73,330,301,MUTED,1,'5 4')+line(176,190,493,190,MUTED,1,'5 4')
        s+=text(330,374,'真实 cell       →       较大的优化模型',24,INK,'middle')
        note='实心：真实尺寸 · 橙框：虚拟尺寸 · 中心不因膨胀自动移动'
    elif name=='routeloop':
        s+=flow([('达到评估条件','overflow + 移动稳定性'),('拥塞估计 / 最佳记录','RUDY 或 GRT'),('面积膨胀 / 空间预算','尺寸 + filler + target density'),('快照恢复 / 继续优化','目标达到 / 预算耗尽 / 不改善退出')],[TEAL,ORANGE,ORANGE,INK])
    elif name=='architecture':
        s+=box(55,24,570,72,'OpenDB → PlacerBase','实例 / 连接 / 几何 / 区域',INK)+arrow(340,98,340,119,INK)
        s+=box(55,122,570,72,'NesterovBaseCommon','GCell / GPin / GNet + 全局线长',TEAL)
        for x,lab in [(55,'Region 0'),(350,'Region 1')]:
            s+=arrow(x+130,198,x+130,225,TEAL)+box(x,228,275,87,lab,'bins / filler / λ / state',ORANGE)
        s+=rect(55,342,570,40,INK)+text(340,370,'NesterovPlace：协调主循环与反馈',23,'white','middle')
    elif name=='regions':
        s+=grid(40,45,580,294,10,6)+rect(375,79,210,195,'#c8d4e3',BLUE,4,.7)+chips(75,132,12)+chips(402,105,12,False,BLUE)
        s+=path([(115,161),(263,246),(442,143)],ORANGE,3)+dot(115,161,5,ORANGE)+dot(442,143,5,ORANGE)
        s+=text(185,81,'top-level',22,TEAL,'middle')+text(480,304,'region / group',20,BLUE,'middle')
        s+=text(340,378,'线长跨域耦合；密度分区管理',24,INK,'middle')
    elif name=='gpu':
        s+=box(35,35,260,92,'HOST','DB / timing / snapshots',INK)+box(375,35,270,92,'DEVICE','coordinates / pins / bins',TEAL)
        s+=arrow(300,67,369,67,ORANGE)+arrow(369,100,300,100,ORANGE)
        s+=rect(373,154,272,206,'#e0ece5',TEAL)+text(510,192,'驻留迭代',24,TEAL,'middle')
        for i,v in enumerate(['WA + scatter','Poisson + gather','Nesterov vectors']):s+=text(510,232+i*44,v,21,INK,'middle')
        s+=text(50,205,'明确同步点：',22,ORANGE)+text(50,247,'拓扑 / 权重 / 面积改变',18)+text(50,284,'快照 / 显示 / 写回',18)
    elif name=='incremental':
        for k in range(2):
            x=34+k*340;s+=grid(x,55,274,258,5,5)
            for i in range(15):s+=rect(x+17+(i%4)*62,80+(i//4)*48,40,26,INK if k==0 else TEAL)
            s+=rect(x+125,265,38,26,ORANGE)+text(x+139,361,'阶段 1：临时锁' if k==0 else '必要时阶段 2：继续优化',20,INK,'middle')
        s+=arrow(310,184,367,184,ORANGE,4)
    elif name=='diagnosis':
        s+=flow([('症状：最终位置 / 指标异常','记录出现异常的首轮'),('对齐事件边界','TD / RD / backtracking / revert'),('追踪状态产生点','坐标、面积、连接、同步'),('最小化并验证','小设计 + 单一机制 + 后续 QoR')],[ORANGE,INK,TEAL,BLUE])
    elif name=='qor':
        for i,(a,b) in enumerate([('GPL','HPWL / overflow'),('DPL','位移 / 合法性'),('GRT','资源 / 拥塞'),('DRT','违例 / WNS / TNS')]):
            y=30+i*90;s+=text(38,y+36,f'0{i+1}',32,TEAL)+box(107,y,509,70,a,b,TEAL if i<2 else ORANGE)
    elif name=='exercises':
        for i,(a,b,c) in enumerate([('一条 net','pin → WA → cell force',TEAL),('一个 bin','overlap → density → field',ORANGE),('一次更新','force → α / β → coordinates',BLUE)]):
            s+=box(50,40+i*112,575,91,a,b,c)
    elif name=='reading':
        s+=flow([('01 解释力','WA / scatter / FFT / gather'),('02 解释步','precondition / step / Nesterov'),('03 解释改变','timing / inflation / callbacks'),('04 解释一致性','region / snapshots / backend')],[TEAL,TEAL,ORANGE,BLUE])
    elif name=='questions':
        for i,(x,y,c) in enumerate([(135,107,TEAL),(340,107,ORANGE),(545,107,BLUE),(238,282,ORANGE),(443,282,TEAL)]):
            s+=dot(x,y,64,c)+text(x,y+18,f'Q{i+1}',43,'white','middle')
    elif name=='notation':
        for x,y,a,b,c in [(95,103,'γ','平滑尺度',TEAL),(340,103,'λ','密度强度',ORANGE),(584,103,'ψ','电势',ORANGE),(95,280,'α','步长',BLUE),(340,280,'β','动量',BLUE),(584,280,'ω','net 权重',TEAL)]:
            s+=text(x,y,a,64,c,'middle')+text(x,y+45,b,21,INK,'middle')
    elif name=='provenance':
        s+=box(60,37,560,94,'固定提交','源码 / tests / diagrams 的共同坐标',TEAL)+box(60,164,560,94,'原理与实数证据分开标识','教学公式 ≠ GPL 仿真；golden ≠ 本次测量',ORANGE)+box(60,291,560,94,'所有资源可离线阅读','SVG / HTML / PDF / 逐页讲解稿',INK)
    elif name=='final':
        s+=dot(330,209,115,'#24494b')
        for x,y,a,b,c in [(154,83,'连接','WA', '#73c9bc'),(515,95,'空间','Poisson','#e6a07c'),(335,362,'反馈','TD / RD','#b7cabc')]:
            s+=dot(x,y,58,c)+text(x,y-3,a,25,INK,'middle')+text(x,y+25,b,17,INK,'middle')
        s+=text(330,203,'Nesterov',29,'#fff','middle')+text(330,239,'一轮轮移动',21,'#b8d7ca','middle')
    else:raise ValueError(name)
    if name not in ('real','final'):s+=caption(note)
    else:s+=text(340,420,note if name=='real' else '从模型到实现 · 回到一整轮数据流',15,'#b8d7ca','middle')
    return f'<svg class="visual" viewBox="0 0 680 435" role="img" aria-labelledby="fig-title-{idx}"><title id="fig-title-{idx}">{escape(title)}</title>{s}</svg>'

def optimizer_figure(k):
    s=''
    cx=326;cy=237
    for r in [50,100,150,220,290]:
        s+=f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r/math.sqrt(12)}" fill="none" stroke="{LINE}"/>'
    s+=line(26,cy,654,cy,LINE)+line(cx,40,cx,365,LINE)
    s+=dot(cx,cy,5,INK)+text(cx-12,cy+27,'最优点',17,INK,'end')
    s+=dot(cx+8*34,cy-4*34,7,ORANGE)+text(595,81,'起点 (8,4)',18,INK,'end')
    s+=text(50,387,'青：GD    橙：Nesterov    等高线：f(x,y)',19,MUTED)
    return s
