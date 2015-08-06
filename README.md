# mite

**mite**, pronounced /maɪt/, is a *minimal template engine* written for fun.

### Examples

**mite** looks for `{{variable}}` tags, which get replaced when the template is rendered.
 
```python
>>> import mite
>>> data = {'var': 'world'}
>>> mite.render("<p>Hello {{var}}!</p>", data)
'<p>Hello world!</p>'
```
