# mite

**mite**, pronounced /maɪt/, is a *minimal template engine* written for fun in
pure python. It looks for `{{variable}}` tags, which get replaced when the
template is rendered.

### Examples

---

##### Basic usage
 
```python
>>> import mite
>>> data = {'var': 'world'}
>>> mite.render("<p>Hello {{var}}!</p>", data)
'<p>Hello world!</p>'
```

---

##### Render precompiled template

```python
>>> import mite
>>> compiled = mite.compile("<p>Hello {{var}}!</p>")
>>> mite.render(fragments=compiled, data={'var': 'world'})
'<p>Hello world!</p>'
>>> mite.render(fragments=compiled, data={'var': 'omg D:'})
'<p>Hello omg D:!</p>'
```
