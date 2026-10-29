#!/usr/bin/env python3
"""Build an evidence-backed, offline relationship graph from the public skill."""
import argparse
import html
import json
import math
import random
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLORS = {'文档': '#475569', '定位': '#1d4ed8', '依据': '#7e22ce', '验证': '#047857', '实现': '#92400e', '排障': '#be123c', '边界': '#0e7490'}


def build():
    source = json.loads((ROOT / 'maps/network-source.json').read_text())
    files = [ROOT / 'SKILL.md'] + sorted((ROOT / 'references').glob('*.md'))
    docs = {str(p.relative_to(ROOT)): p.read_text() for p in files}
    nodes, edges = [], []

    def proof(name, quote):
        path = 'references/' + name
        text = docs[path]
        if quote not in text:
            raise ValueError(f'Unmatched evidence: {name}: {quote!r}')
        return {'path': path, 'line': text[:text.index(quote)].count('\n') + 1, 'excerpt': quote}

    for path, text in docs.items():
        heading = re.search(r'^# (.+)$', text, re.M)
        if heading is None:
            raise ValueError(f'Missing document title: {path}')
        title = heading.group(1)
        nodes.append({'id': 'doc:' + path, 'label': Path(path).name, 'group': '文档',
                      'summary': title, 'sources': [{'path': path, 'line': text[:heading.start()].count('\n') + 1, 'excerpt': heading.group(0)}]})
    for ident, title, group, name, quote in source['topics']:
        p = proof(name, quote)
        nodes.append({'id': ident, 'label': title, 'group': group, 'summary': quote, 'sources': [p]})
        edges.append({'source': 'doc:' + p['path'], 'target': ident, 'label': '说明', 'kind': 'index', 'evidence': p})
    for a, b, label, name, quote in source['relations']:
        edges.append({'source': a, 'target': b, 'label': label, 'kind': 'semantic', 'evidence': proof(name, quote)})
    # Include every resolvable explicit reference between SKILL.md and reference docs.
    # Repeated links collapse to one edge; all occurrences remain in evidence locations.
    for path, text in docs.items():
        refs = re.finditer(r'`(references/[^`]+\.md)`|\]\(([^)]+\.md)(?:#[^)]*)?\)', text)
        grouped = {}
        for m in refs:
            target = m.group(1) or str((ROOT / path).parent.joinpath(m.group(2)).resolve().relative_to(ROOT))
            if target not in docs or target == path:
                continue
            grouped.setdefault(target, []).append({'path': path, 'line': text[:m.start()].count('\n') + 1, 'excerpt': m.group(0)})
        for target, occurrences in grouped.items():
            edges.append({'source': 'doc:' + path, 'target': 'doc:' + target, 'label': '引用',
                          'kind': 'reference', 'evidence': occurrences[0], 'occurrences': occurrences})
    ids = {n['id'] for n in nodes}
    assert len(ids) == len(nodes)
    for i, e in enumerate(edges):
        assert e['source'] in ids and e['target'] in ids
        e['id'] = 'e' + str(i)
    layout(nodes, edges)
    graph = {'schema_version': 1, 'scope': source['scope'],
             'coverage': 'All resolvable explicit links between SKILL.md and references/*.md, plus curated topic relations backed by exact source excerpts. This is not an exhaustive ontology of UEFI.',
             'nodes': nodes, 'edges': edges}
    return graph


def layout(nodes, edges):
    rng = random.Random(41)
    n = len(nodes)
    pos = {item['id']: [900 + 600 * math.cos(2 * math.pi * i / n) + rng.random(),
                        610 + 470 * math.sin(2 * math.pi * i / n) + rng.random()] for i, item in enumerate(nodes)}
    for step in range(650):
        delta = {k: [0., 0.] for k in pos}
        keys = list(pos)
        for i, a in enumerate(keys):
            for b in keys[i+1:]:
                dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
                dist = max(1., math.hypot(dx, dy))
                force = 25000 / (dist * dist)
                if abs(dx) < 205 and abs(dy) < 66:
                    force += 9
                for axis, diff in enumerate((dx, dy)):
                    val = force * diff / dist
                    delta[a][axis] += val
                    delta[b][axis] -= val
        for e in edges:
            a, b = e['source'], e['target']
            dx, dy = pos[b][0]-pos[a][0], pos[b][1]-pos[a][1]
            dist = max(1., math.hypot(dx, dy))
            force = (dist-235) * .006
            for axis, diff in enumerate((dx,dy)):
                delta[a][axis] += force*diff/dist
                delta[b][axis] -= force*diff/dist
        speed = 2 * (1-step/750)
        for k in pos:
            pos[k][0] = min(1710, max(110, pos[k][0] + max(-10,min(10,delta[k][0]))*speed))
            pos[k][1] = min(1110, max(110, pos[k][1] + max(-10,min(10,delta[k][1]))*speed))
    # Resolve label-box collisions after the spring layout; do not let attractive
    # edges compress labels into each other. Fixed seeded layout stays reproducible.
    keys = list(pos)
    for _ in range(180):
        changed = False
        for i, a in enumerate(keys):
            for b in keys[i+1:]:
                dx, dy = pos[b][0]-pos[a][0], pos[b][1]-pos[a][1]
                ox, oy = 270-abs(dx), 76-abs(dy)
                if ox > 0 and oy > 0:
                    axis = 0 if ox < oy else 1
                    amount = (min(ox, oy)+.1)/2
                    sign = 1 if (dx if axis == 0 else dy) >= 0 else -1
                    pos[a][axis] -= amount*sign
                    pos[b][axis] += amount*sign
                    changed = True
        if not changed:
            break
    offset_x = max(0, 145-min(p[0] for p in pos.values()))
    offset_y = max(0, 135-min(p[1] for p in pos.values()))
    for item in nodes:
        item['x'], item['y'] = (round(pos[item['id']][0]+offset_x, 2), round(pos[item['id']][1]+offset_y, 2))
        item['color'] = COLORS[item['group']]


def static_svg(g):
    by_id = {n['id']: n for n in g['nodes']}
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1840" height="1340" viewBox="0 0 1840 1340" role="img" aria-labelledby="title desc">',
           '<title id="title">UEFI Skill 关系网络</title><desc id="desc">节点包括参考文档和经验主题。线连接文档引用、主题索引和有来源的语义关系；交互版可点选和展开。</desc>',
           '<rect width="1840" height="1340" fill="#f8fafc"/>',
           '<g font-family="Noto Sans CJK SC,Microsoft YaHei,sans-serif">',
           '<text x="48" y="42" fill="#0f172a" font-size="28">UEFI Skill · 全局关系网络</text>',
           f'<text x="48" y="72" fill="#475569" font-size="17">{len(g["nodes"])} 个节点 · {len(g["edges"])} 条关系 · 实线：主题关系 / 虚线：引用与索引 · 点击阅读节点来源</text>']
    for e in g['edges']:
        a,b = by_id[e['source']],by_id[e['target']]
        color = '#475569' if e['kind']=='semantic' else '#7b8ba1'
        dash = '' if e['kind']=='semantic' else ' stroke-dasharray="4 6"'
        out.append(f'<line x1="{a["x"]}" y1="{a["y"]}" x2="{b["x"]}" y2="{b["y"]}" stroke="{color}" stroke-width="2"{dash}><title>{html.escape(a["label"]+" → "+e["label"]+" → "+b["label"])}</title></line>')
    for node in g['nodes']:
        x,y=node['x'],node['y']
        label=node['label']
        # Split long ASCII filenames while keeping conceptual labels intact.
        lines=[label] if len(label)<=22 else [label[:20],label[20:]]
        width=max(130,min(260, max(sum(18 if ord(c)>255 else 9 for c in line) for line in lines)+24))
        height=36 if len(lines)==1 else 56
        out.append(f'<a href="../{html.escape(node["sources"][0]["path"])}"><rect x="{x-width/2}" y="{y-height/2}" width="{width}" height="{height}" rx="9" fill="#ffffff" stroke="{node["color"]}"/>')
        for i,line in enumerate(lines):
            out.append(f'<text x="{x}" y="{y+6-(len(lines)-1)*10+i*20}" text-anchor="middle" fill="{node["color"]}" font-size="18">{html.escape(line)}</text>')
        out.append('</a>')
    for i,(label,color) in enumerate(COLORS.items()):
        x=60+i*245
        out.append(f'<circle cx="{x}" cy="1210" r="7" fill="{color}"/><text x="{x+17}" y="1216" fill="#334155" font-size="18">{label}</text>')
    out.extend(['<text x="48" y="1260" fill="#334155" font-size="18">关系范围：当前公开 skill 的明确引用 + 有原文依据的人工整理关系；不声称穷尽全部 UEFI 知识。</text>',
                '<text x="48" y="1296" fill="#475569" font-size="18">交互版 network.html：点选展开 · 1 / 2 / 全部层级 · 搜索 · 拖动缩放 · 连线依据 · 文档内嵌阅读</text></g></svg>'])
    text='\n'.join(out)
    ET.fromstring(text)
    return text


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    g=build()
    payload=json.dumps(g,ensure_ascii=False,indent=2)+'\n'
    template=(ROOT/'maps/network-template.html').read_text()
    # No fetch/CDN: downloaded HTML works as a standalone file.
    docs={str(p.relative_to(ROOT)):p.read_text() for p in [ROOT/'SKILL.md']+sorted((ROOT/'references').glob('*.md'))}
    page=template.replace('__GRAPH_JSON__',json.dumps(g,ensure_ascii=False).replace('<','\\u003c')).replace('__DOCUMENTS_JSON__',json.dumps(docs,ensure_ascii=False).replace('<','\\u003c'))
    outputs={'maps/network.json':payload,'maps/network.svg':static_svg(g),'maps/network.html':page}
    for path, content in outputs.items():
        target=ROOT/path
        if args.check:
            assert target.read_text()==content, f'Stale generated file: {path}'
        else:
            target.write_text(content)
    print(json.dumps({'nodes':len(g['nodes']),'edges':len(g['edges']), 'kinds':{k:sum(e['kind']==k for e in g['edges']) for k in ['semantic','reference','index']},'sources_verified':True,'generated_files_current':True},ensure_ascii=False))

if __name__=='__main__':
    main()
