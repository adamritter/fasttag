import sys, pickle
sys.path.append("build/lib.macosx-14.5-arm64-cpython-312")
import fasttag
from fasttag import *
import fasthtml.common

fasttag.set_indent(-1)
def assert_equal(a, b): assert a == b, (a, b)
assert_equal(tag("div", "text&<>"), HTML('<div>text&amp;&lt;></div>'))
assert_equal(tag("span", "wow", a='Tom & Jerry "the mouse"'), HTML('<span a="Tom &amp; Jerry &quot;the mouse&quot;">wow</span>'))
assert_equal(tag("c", "cc", _class="a b c"), HTML('<c class="a b c">cc</c>'))
assert_equal(tag("b", "bb", hx_target="closest tr"), HTML('<b hx-target="closest tr">bb</b>'))
assert_equal(tag("input", type="text", value="value"), HTML('<input type="text" value="value">'))
assert_equal(Div("value"), HTML('<div>value</div>'))
assert_equal(Input(type="checkbox", checked=True, disabled=False), HTML('<input type="checkbox" checked>'))
fasttag.set_indent(2)
assert_equal(fasttag.Div("value"), HTML("<div>value</div>"))
print(fasttag.Tr(fasttag.Td("hello"), fasttag.Td("world")))
assert_equal(fasttag.Tr(fasttag.Td("hello"), fasttag.Td("world")), HTML("<tr>\n  <td>hello</td>\n  <td>world</td>\n</tr>"))
assert_equal(fasttag.Span("hello", "world"), HTML("<span>\n  hello\n  world\n</span>"))
assert_equal(fasttag.Span("hello\nworld"), HTML("<span>\n  hello\n  world\n</span>"))
assert_equal(Input(type="number", value=10.3, min=-10, max=100), HTML('<input type="number" value="10.3" min="-10" max="100">'))
assert_equal(Div(3.3), HTML('<div>3.3</div>'))
assert_equal(str(HTML("aa") + HTML("BB")), "aaBB")
assert_equal(Div(HTML("aa")), HTML("<div>\n  aa\n</div>"))
assert_equal(Text("This is an <example> of text"), HTML("This is an &lt;example> of text"))
assert_equal(DOCTYPE, HTML("<!DOCTYPE html>\n"))
assert_equal(Div(_="value"), HTML('<div _="value"></div>'))
assert_equal(Div(_="value").__html__(), '<div _="value"></div>')
assert_equal(Div("value").tag, 'div')
assert_equal(Div("hello\nworld"), HTML('<div>\n  hello\n  world\n</div>'))
assert_equal(Pre("hello\nworld"), HTML('<pre>hello\nworld</pre>'))
assert_equal(Div(("hello", ("world", "nested"))), HTML('<div>\nhello\n\nworld\nnested</div>'))
assert_equal(Div(({"a": 2})), HTML("<div>{'a': 2}</div>"))
assert_equal(Div(["a", 2]), HTML("<div>['a', 2]</div>"))
assert_equal(Div(a=[1,2]), HTML('<div a="[1, 2]"></div>'))
assert_equal(Div(a=["'",'"']), HTML('''<div a="[&quot;'&quot;, '&quot;']"></div>'''))
assert_equal(Div(fasthtml.common.Span("hello")), HTML("<div><span>hello</span>\n  </div>"))
assert_equal(Div("value", a="b", ccc="d", and2="tom&jerry").attrs,
             {"a": "b", "ccc": "d", "and2": "tom&jerry"})

class HTML_Test:
    def __html__(self):
        return "hello"

assert_equal(Div(HTML_Test()), HTML("<div>hello</div>"))

a = HTML("<p>hello</p>")
assert_equal(pickle.loads(pickle.dumps(a)), a)


print(
    Div(
        Div(Label("First Name"), ": Joe"),
        Div(Label("Last Name"), ": Blow"),
        Div(Label("Email"), ": joe@blow.com"),
        # if a keyword starts with _, the first _ is ignored and the rest is used as an argument unchanged.
        Button("Click To Edit", hx_get="/contact/1/edit", _class="btn primary"),   
        # If the keyword argument doesn't start with _, underscores are converted to hypens (-) in the attibute name
        hx_target="this", hx_swap="outerHTML")
    )


ss = """<tr id="e8685253296095281136" style="background-color: #d7a748">
  <td>23</td>
  <td>
    <a href="/city/Molino d'Elsa">Molino d'Elsa (IT)</a>
  </td>
  <td>
    <span>
      18.14°C
      <br>
      (19°C / 16°C)
    </span>
  </td>
  <td>1</td>
  <td>0</td>
  <td>
    <a href="#" hx-post="/?city=Molino d'Elsa">update</a>
  </td>
  <td>43.3243</td>
</tr>"""

assert_equal(str(HTML(ss)), ss)
