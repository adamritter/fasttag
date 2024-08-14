import time
import dominate
from lxml import etree
import sys
sys.path.append("build/lib.macosx-14.5-arm64-cpython-312")
import fasttag
from fasttag import *
import fasthtml.common
import html
import fast_html
import jinja2


def latency(f):
    start = time.time()
    f()
    return time.time() - start
def latency1000000(f): return latency(lambda: [f() for _ in range(1000000)])
def latency1000(f): return latency(lambda: [f() for _ in range(1000)])

def lxml_text_div():
    div = etree.Element("div")
    div.text = "Hello & world <3"
    return etree.tostring(div)

fasttag.set_indent(-1)

template = jinja2.Template("<div>{{ text }} {{ text2 }}</div>", autoescape=True)
def assert_equal(a, b): assert a == b, (a, b)

assert_equal(fast_html.render(fast_html.div([html.escape("Hello &"), html.escape(" world <3")])), "<div>Hello &amp; world &lt;3</div>")
assert_equal("".join(["<div>", html.escape("Hello &"), html.escape(" world <3"), "</div>"]), "<div>Hello &amp; world &lt;3</div>")
assert_equal(fasttag.Div("Hello &", "world <3").bytes(), b"<div>Hello &amp;world &lt;3</div>")
assert_equal(str(dominate.tags.div("Hello &", "world <3")), "<div>Hello &amp;world &lt;3</div>")
assert_equal(fasthtml.common.to_xml(fasthtml.common.Div("Hello &", "world <3")), "<div>\nHello &amp;\nworld &lt;3\n</div>\n")
assert_equal(lxml_text_div(), b'<div>Hello &amp; world &lt;3</div>')
assert_equal(template.render(text="Hello &", text2="world <3"), "<div>Hello &amp; world &lt;3</div>")

b200 = "q" * 195
print("         fasttag200 latency: ", latency1000000(lambda: fasttag.Div(b200).bytes()), "us")

print("         fasttag latency: ", latency1000000(lambda: fasttag.Div("Hello &", "world <3").bytes()), "us")
print("join+html.escape latency: ", latency1000000(lambda: "".join(["<div>", html.escape("Hello &"), html.escape(" world <3"), "</div>"])), "us")
print("        dominate latency: ", latency1000000(lambda: str(dominate.tags.div("Hello &", "world <3"))), "us")
print("        fasthtml latency: ", latency1000000(lambda: fasthtml.common.to_xml(fasthtml.common.Div("Hello &", "world <3"))), "us")
print("            lxml latency:", latency1000000(lambda: lxml_text_div()), "us")
print("         jinja2 latency: ", latency1000000(lambda: template.render(text="Hello &", text2="world <3")), "us")


