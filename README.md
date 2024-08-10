# FastTag

FastTag is a fast HTML generation module written in C for Python. It allows for efficient and easy generation of HTML tags with support for attributes and nested content.

It's almost as fast as string join, and it's built as a mostly drop in replacement for FastHTML's tag library (but 20x faster).

## Installation

You can install the module using pip:

```bash
pip install fasttag
```


## Usage:

```python
from fasttag import *
Div( # HTML Tags are exported in fasttag, but fasttag.tag("div", ...) can be used as well.
    # Label("First Name") returns the HTML as a bytes (which is not escaped, just indented), but all passed strings in the element children and attribute values are escaped
    Div(Label("First Name"), ": Joe"),
    Div(Label("Last Name"), ": Blow"),
    Div(Label("Email"), ": joe@blow.com")
    # if a keyword starts with _, the first _ is ignored and the rest is used as an argument unchanged.
    Button("Click To Edit", hx_get="/contact/1/edit", _class="btn primary"),   
    # If the keyword argument doesn't start with _, underscores are converted to hypens (-) in the attibute name
    hx_target="this", hx_swap="outerHTML")
```

=>

```HTML
<div hx-target="this" hx-swap="outerHTML">
<div>
    <label>First Name</label>
    : Joe
</div>
<div>
    <label>Last Name</label>
    : Blow
</div>
<div>
    <label>Email</label>
    : joe@blow.com
</div>
<button hx-get="/contact/1/edit" class="btn primary">Click To Edit</button>
</div>
```

Keyword argument values can be string, boolean or numeric. Boolean values will appear as attributes without values if True, and not appear if False.
Numeric values are quoted.

```python
    Input(type="checkbox", id="scales", name="scales", checked=True, disabled=False)
    # => HTML('<input type="checkbox" id="scales" name="scales" checked>')
```

The HTML is represented as UTF-8. The bytes can be extracted / converted to str with:

```python
  HTML('<div>Example HTML</div>').bytes() # => b'<div>Example HTML</div>'
  str(HTML('<div>Example HTML</div>')) # => '<div>Example HTML</div>'
```

Text node can be created with Text (although it's automatically created for strings inside tags):

```python
Text('This is an <example> text ') # => HTML('This is an &lt;example> text')
```

The DOCTYPE constant can be used to prepend DOCTYPE html:
```python
DOCTYPE + Html(Head(Title("Hello"), Body("Hello, world")))
```

=>
```html
<!DOCTYPE html>
<html>
  <head>
    <title>Hello</title>
    <body>Hello, world</body>
  </head>
</html>
```

### Changing indentation

Indentation can be set with fasttag.set_indent.
Default value is 2, but it can set to any non-negative number, or -1 which achieves no indentation and no newline between children.
It improves performance, memory usage and output size for large data.
1 space is still added between text children siblings even with -1 indentation.

```python
from fasttag import *
set_indent(-1)
Div("hello", Span("world"))
# => HTML('<div>hello<span>world</span></div>')
```

## Using with FastHTML:
FastTag was built to be mostly mirror FastHTML API. One important missing feature is automatically concatenating tuples.

To use it, import fasttag after fasthtml.common:

```python
from fasthtml.common import *
from fasttag import *
```

Also when returning data inside a handler, use ```.bytes()``` to convert it into ```bytes``` object.

Right now  ``to_xml()`` inside ```FastCore``` needs a modification: https://github.com/fastai/fastcore/pull/597

It's a one line change in to_xml() inside xml.py:

```python
def to_xml(elm, lvl=0):
    "Convert `ft` element tree into an XML string"
    if elm is None: return ''
    if isinstance(elm, tuple): return '\n'.join(to_xml(o) for o in elm)
    if hasattr(elm, '__ft__'): elm = elm.__ft__()
    if isinstance(elm, bytes): return elm.decode('utf-8')  # This line needs to be inserted
    sp = ' ' * lvl
    if not isinstance(elm, list): return f'{_escape(elm)}\n'
```


## Benchmark:

```
              fasttag latency:  0.16us      1x
     join+html.escape latency:  0.45us      3x
             dominate latency:  2.92us     18x
             fasthtml latency:  3.23us     20x
                 lxml latency:  1.66us     10x
join without escaping latency:  0.12us   0.75x
```

