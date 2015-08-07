import unittest
import mite


class miteTests(unittest.TestCase):

    def test_get(self):
        identifier = 'test.test1'
        data = {'test': {'test0': '0', 'test1': 'ok'}}
        self.assertEqual(mite.get(identifier, [data]), 'ok')

    def test_get_scopes(self):
        identifier = 'test.test1'
        data0 = {'test': {'test0': '0', 'test2': 'ok'}}
        data1 = {'test': {'test0': '0', 'test1': 'ok'}}
        self.assertEqual(mite.get(identifier, [data0, data1]), 'ok')


    def test_compile_empty(self):
        self.assertEqual(mite.compile(), [])

    def test_compile_unbalanced_right(self):
        template = '{{}'
        fragments = mite.compile(template)
        self.assertEqual(fragments, [(mite.FRAG_TEXT, '{{}')])

    def test_compile_unbalanced_right_space(self):
        template = '{{ }'
        fragments = mite.compile(template)
        self.assertEqual(fragments, [(mite.FRAG_TEXT, '{{ }')])

    def test_compile_fragments_var(self):
        template = '{{  test0 }}'
        fragments = mite.compile(template)
        self.assertEqual(fragments, [(mite.FRAG_VAR, 'test0')])

    def test_compile_fragments_var_text(self):
        template = '{{{  test0 }}'
        fragments = mite.compile(template)
        self.assertEqual(fragments, [(mite.FRAG_TEXT, '{'),
                                     (mite.FRAG_VAR, 'test0')])


    def test_render_empty(self):
        rendered = mite.render()
        self.assertEqual(rendered, '')

    def test_render_unbalanced_left(self):
        template = '{{}'
        rendered = mite.render(template)
        self.assertEqual(rendered, '{{}')

    def test_render_unbalanced_left(self):
        template = '{{var}}'
        data = {'var': 'ok'}
        rendered = mite.render(template, data)
        self.assertEqual(rendered, 'ok')

    def test_render_unpacking_args(self):
        template = 'ok {{var}}'
        data = {'var': 'ok'}
        args = {'template': template,
                'data': data}
        rendered = mite.render(**args)
        self.assertEqual(rendered, 'ok ok')

    def test_render_scopes(self):
        template = 'Hello, {{test.test1}}!'
        data0 = {'test': {'test0': '0', 'test2': 'ok'}}
        data1 = {'test': {'test0': '0', 'test1': 'ok'}}
        scopes = [data0, data1]
        self.assertEqual(mite.render(template, scopes=scopes), 'Hello, ok!')

    def test_render_fragments_scopes(self):
        template = 'Hello, {{test.test1}}!'
        data0 = {'test': {'test0': '0', 'test2': 'ok'}}
        data1 = {'test': {'test0': '0', 'test1': 'ok'}}
        scopes = [data0, data1]
        fragments = mite.compile(template)
        rendered = mite.render(fragments=fragments, scopes=scopes)
        self.assertEqual(rendered, 'Hello, ok!')


if __name__ == '__main__':
    unittest.main(verbosity=2)
