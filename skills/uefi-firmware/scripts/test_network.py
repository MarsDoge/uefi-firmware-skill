#!/usr/bin/env python3
"""Regression tests for graph provenance, coverage, traversal and packaging."""
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from render_network import ROOT, build
from query_network import neighborhood


class NetworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = build()

    def test_all_public_reference_documents_included(self):
        expected = {'doc:SKILL.md'} | {'doc:' + str(p.relative_to(ROOT)) for p in (ROOT/'references').glob('*.md')}
        actual = {n['id'] for n in self.graph['nodes'] if n['group'] == '文档'}
        self.assertEqual(actual, expected)

    def test_unique_edges_and_valid_endpoints(self):
        ids = {n['id'] for n in self.graph['nodes']}
        edges = self.graph['edges']
        keys = {(e['source'],e['target'],e['label'],e['kind']) for e in edges}
        self.assertEqual(len(keys),len(edges))
        for e in edges:
            self.assertIn(e['source'],ids)
            self.assertIn(e['target'],ids)

    def test_exact_source_evidence_and_lines(self):
        for e in self.graph['edges']:
            for p in e.get('occurrences',[e['evidence']]):
                text = (ROOT/p['path']).read_text()
                self.assertIn(p['excerpt'],text)
                tail = '\n'.join(text.splitlines()[p['line']-1:])
                offset = tail.find(p['excerpt'])
                self.assertGreaterEqual(offset, 0)
                self.assertLessEqual(offset, len(tail.split('\n', 1)[0]))

    def test_label_boxes_do_not_overlap(self):
        nodes = self.graph['nodes']
        for i, a in enumerate(nodes):
            self.assertTrue(130 <= a['x'] <= 1710)
            self.assertTrue(120 <= a['y'] <= 1170)
            for b in nodes[i+1:]:
                self.assertTrue(abs(a['x']-b['x']) >= 260 or abs(a['y']-b['y']) >= 60,
                                (a['id'], b['id']))

    def test_node_source_lines(self):
        for node in self.graph['nodes']:
            for p in node['sources']:
                text = (ROOT/p['path']).read_text()
                self.assertIn(p['excerpt'], '\n'.join(text.splitlines()[p['line']-1:]))
                self.assertIn(p['excerpt'].splitlines()[0], text.splitlines()[p['line']-1])

    def test_unmatched_source_rejected(self):
        original = Path.read_text
        def changed(path,*args,**kwargs):
            value=original(path,*args,**kwargs)
            if path.name=='network-source.json':
                data=json.loads(value)
                data['relations'][0][-1]='NOT A REAL SOURCE EXCERPT'
                return json.dumps(data)
            return value
        with patch.object(Path,'read_text',changed):
            with self.assertRaisesRegex(ValueError,'Unmatched evidence'):
                build()

    def test_semantic_one_hop_boot(self):
        got=neighborhood(self.graph,'boot','1','semantic')
        self.assertEqual({n['id'] for n in got['nodes']},{'boot','variables','policy'})

    def test_monotonic_depth_and_all(self):
        sets=[{n['id'] for n in neighborhood(self.graph,'boot',depth)['nodes']} for depth in ['0','1','2','all']]
        for a,b in zip(sets,sets[1:]):
            self.assertTrue(a<=b)
        self.assertEqual(sets[-1],{n['id'] for n in self.graph['nodes']})

    def test_unknown_node(self):
        with self.assertRaises(ValueError):
            neighborhood(self.graph,'not-a-node','1')

    def test_query_cli(self):
        cmd=[sys.executable,str(ROOT/'scripts/query_network.py')]
        found=json.loads(subprocess.check_output(cmd+['--search','启动项'],text=True))
        self.assertIn('boot',{n['id'] for n in found['matches']})
        result=json.loads(subprocess.check_output(cmd+['--node','boot','--depth','1','--kind','semantic'],text=True))
        self.assertEqual(len(result['nodes']),3)
        bad=subprocess.run(cmd+['--node','not-a-node'],capture_output=True)
        self.assertNotEqual(bad.returncode,0)

    def test_offline_html_contains_data_and_no_remote_assets(self):
        page=(ROOT/'maps/network.html').read_text()
        self.assertNotIn('__GRAPH_JSON__',page)
        self.assertNotIn('__DOCUMENTS_JSON__',page)
        self.assertNotRegex(page,r'<(?:script|link)[^>]+(?:src|href)=["\']https?://')
        self.assertNotIn('fetch(',page)
        self.assertIn('documents-data',page)

    def test_node_text_contrast_on_white(self):
        def luminance(color):
            channels = [int(color[i:i+2], 16)/255 for i in (1, 3, 5)]
            linear = [c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in channels]
            return sum(c*w for c, w in zip(linear, (.2126, .7152, .0722)))
        for n in self.graph['nodes']:
            self.assertGreaterEqual(1.05/(luminance(n['color'])+.05), 4.5, n['id'])
        for color in ('#475569', '#7b8ba1'):
            self.assertGreaterEqual((luminance('#f8fafc')+.05)/(luminance(color)+.05), 3)

    def test_generated_output_fresh(self):
        subprocess.run([sys.executable,str(ROOT/'scripts/render_network.py'),'--check'],check=True)


if __name__=='__main__':
    unittest.main(verbosity=2)
