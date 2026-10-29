#!/usr/bin/env python3
"""Read-only search and neighborhood traversal; no LLM, API, or dependencies."""
import argparse
import json
from pathlib import Path


def neighborhood(graph, node_id, depth, kind='all'):
    ids = {n['id'] for n in graph['nodes']}
    if node_id not in ids:
        raise ValueError(f'Unknown node: {node_id}')
    edges = [e for e in graph['edges'] if kind == 'all' or e['kind'] == kind]
    reached, frontier = {node_id}, {node_id}
    for _ in range(len(ids) if depth == 'all' else int(depth)):
        following = set()
        for e in edges:
            if e['source'] in frontier:
                following.add(e['target'])
            if e['target'] in frontier:
                following.add(e['source'])
        frontier = following - reached
        reached.update(frontier)
        if not frontier:
            break
    return {'nodes': [n for n in graph['nodes'] if n['id'] in reached],
            'edges': [e for e in edges if e['source'] in reached and e['target'] in reached]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_mutually_exclusive_group(required=True)
    commands.add_argument('--search', help='Substring search over ID, label, summary, and source paths')
    commands.add_argument('--node', help='Exact stable node ID')
    parser.add_argument('--depth', choices=['0', '1', '2', 'all'], default='1')
    parser.add_argument('--kind', choices=['all', 'semantic', 'reference', 'index'], default='all')
    args = parser.parse_args()
    graph = json.loads((Path(__file__).resolve().parents[1] / 'maps/network.json').read_text())
    if args.search is not None:
        q = args.search.casefold()
        result = {'matches': [n for n in graph['nodes'] if q in ' '.join([n['id'], n['label'], n['summary']] + [s['path'] for s in n['sources']]).casefold()]}
    else:
        try:
            result = neighborhood(graph, args.node, args.depth, args.kind)
        except ValueError as exc:
            parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
