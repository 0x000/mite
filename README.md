# mite

mite, pronounced /maɪt/, is a minimal template engine system written for fun.

## Example

mite looks for `{{variable}}` fragments, which get replaced when the template is rendered.
 
```python
>>> import mite
>>> env = {'variable': 42}
>>> mite.Compiler("<div>{{variable}}</div>").render(env)
'<div>42</div>'
```
