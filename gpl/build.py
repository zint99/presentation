#!/usr/bin/env python3
"""Build offline HTML slides, speaker manuscript and source index (stdlib only)."""
from pathlib import Path
from html import escape
from content import REV, ROOT, SOURCES, SLIDES
from diagrams import figure

HERE=Path(__file__).resolve().parent

def source_link(key):
    label,path=SOURCES[key]
    url=path if path.startswith('https:') else ROOT+path
    return f'<a href="{escape(url)}" target="_blank" rel="noopener noreferrer">{escape(label)} ↗</a>'

def page_head(title,extra=''):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light"><meta name="description" content="OpenROAD GPL 中文深度演示：线长、静电密度、Nesterov、时序与拥塞反馈。56 页图解，四个数值实验与逐页讲解稿。">
<title>{title}</title><link rel="stylesheet" href="style.css">{extra}</head>'''

parts=[page_head('GPL · 从连接到空间'),'''<body class="deck">
<header class="topbar"><a class="brand" href="../">GPL<span> / OPENROAD</span></a><span id="chapter-label">序章</span>
<nav aria-label="演示工具"><button id="overview" title="O 打开目录">目录 <kbd>O</kbd></button><button id="show-notes" title="N 显示当前页备注">备注 <kbd>N</kbd></button><a href="notes.html" target="_blank" rel="noopener">讲解稿 ↗</a><a href="gpl-deep-dive.pdf" download>PDF ↓</a><button id="fullscreen" title="F 全屏">全屏 <kbd>F</kbd></button></nav></header>
<noscript><p class="nojs">JavaScript 未启用：以下显示全部幻灯片，交互图例为默认状态；可阅读讲解稿。</p></noscript>
<main id="slides" aria-label="GPL 演示文稿">''']
notes=[page_head('GPL · 逐页讲解稿'),'<body class="manuscript"><header><a href="index.html">← 返回演示</a> · <a href="gpl-deep-dive.pdf">下载 PDF</a> · <a href="source-index.html">源码索引</a><h1>GPL · 逐页讲解稿</h1><p>56 页中文演示 · 建议完整分享 90–120 分钟。每页包括重点、讲解与固定版本来源。</p><p>源码：zint99/OpenROAD @ '+REV+'</p></header><main>']
for i,s in enumerate(SLIDES,1):
    refs=' · '.join(source_link(k) for k in s['refs'])
    theme=' dark' if s.get('theme')=='dark' else ''
    lab=f' data-lab="{s["lab"]}"' if s.get('lab') else ''
    parts.append(f'''<section id="slide-{i}" class="slide{theme}" data-chapter="{escape(s['ch'])}" aria-labelledby="title-{i}">
<div class="slide-heading"><p class="eyebrow">{escape(s['subtitle'])}</p><h{'1' if i==1 else '2'} id="title-{i}">{escape(s['title'])}</h{'1' if i==1 else '2'}></div>
<div class="slide-content"><div class="copy">{s['body']}</div><figure id="figure-{i}"{lab}>{figure(s['diagram'],i,s['title'])}</figure></div>
<p class="takeaway">{escape(s['takeaway'])}</p><footer class="sources"><span>来源：</span>{refs}<b class="print-page">{i:02d} / 56</b></footer>
<template class="speaker-note">{escape(s['notes'])}</template></section>''')
    notes.append(f'''<article id="note-{i}"><p class="eyebrow">{i:02d} / 56 · {escape(s['ch'])}</p><h2><a href="index.html#slide-{i}">{escape(s['title'])}</a></h2><blockquote>{escape(s['takeaway'])}</blockquote><p>{escape(s['notes'])}</p><div class="sources">{refs}</div></article>''')
parts.append('''</main><footer class="bottombar"><div id="progress"></div><span class="key-hint">← → 翻页 · O 目录 · N 备注 · F 全屏</span><span id="slide-status" class="sr-only" aria-live="polite"></span><nav aria-label="翻页"><button id="previous" aria-label="上一页">←</button><span id="count">01 / 56</span><button id="next" aria-label="下一页">→</button></nav></footer>
<dialog id="toc-dialog" aria-labelledby="toc-title"><header><div><p class="eyebrow">GPL / READING MAP</p><h2 id="toc-title">从任意章节开始</h2></div><button id="close-toc" aria-label="关闭目录">关闭 ×</button></header><div id="toc"></div></dialog>
<aside id="notes" hidden aria-label="当前页讲者备注"><header><b id="notes-title">讲者备注</b><button id="close-notes" aria-label="关闭备注">×</button></header><p id="note-text"></p><small>备注显示在当前窗口，投屏时也会可见。可另开<a href="notes.html" target="_blank" rel="noopener">完整讲解稿</a>。</small></aside>
<script src="numerics.js"></script><script src="deck.js"></script></body></html>''')
notes.append('</main><footer>原理图均为自行绘制；回归图的数据来源随页标明。</footer></body></html>')
(HERE/'index.html').write_text('\n'.join(parts))
(HERE/'notes.html').write_text('\n'.join(notes))
index=[page_head('GPL · 固定版本源码索引'),'<body class="manuscript"><header><a href="index.html">← 返回演示</a><h1>GPL · 源码与资料索引</h1><p>所有实现入口均固定到 '+REV+'。</p></header><main><table><tr><th>主题</th><th>位置 / 链接</th></tr>']
for key,(label,path) in SOURCES.items():index.append(f'<tr><td>{escape(label)}</td><td>{source_link(key)}<br><code>{escape(path)}</code></td></tr>')
index.append('</table></main></body></html>')
(HERE/'source-index.html').write_text('\n'.join(index))
print(f'Built {len(SLIDES)} slides, manuscript, and {len(SOURCES)} source references.')
