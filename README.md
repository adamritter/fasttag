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

Values in attributes and children are converted to string automatically. The only exception is
tuples in children, which are concatenated:

```python
Div(a=[1,2,3], [4,5,6])
# => <div a='[1, 2, 3]'>[4, 5, 6]</div>
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

Tag attribute can be used to get the tag
```python
Div("hello").tag # => "div"
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

## HTML for custom objects:

Objects can implement the ```.__html__()``` method to return their HTML representation.

```python
class HTML_Test:
    def __html__(self):
        return "hello"

Div(HTML_Test()) # => <div>hello</div>
```

## Using with FastHTML:
FastTag was built to mostly mirror FastHTML API.

To use it, just import fasttag after fasthtml.common:

```python
from fasthtml.common import *
from fasttag import *
```

Also when returning data inside a handler, use ```.bytes()``` to convert it into ```bytes``` object.

```.__html__()``` returns the HTML as string, and ```.__ft()__``` returns the object itself (identity method) for compatibility with FastHTML.


## Benchmark:

```
              fasttag latency:  0.17us      1x
     join+html.escape latency:  0.53us      3x
             dominate latency:  3.89us     23x
             fasthtml latency:  4.99us     29x
                 lxml latency:  1.69us     10x
               jinja2 latency:  6.83us     40x
```


## TODO:
Some missing features:
- Large table benchmarks with headers
- Comformance test vs FastHTML
- svg namespace
- parsing: attrs should get attributes
- parsing: children should extract children from text