import time
import dominate
from lxml import etree
import sys
sys.path.append("build/lib.macosx-14.5-arm64-cpython-312")
import fasttag
from fasttag import *
import fasthtml.common
import html


def latency(f):
    start = time.time()
    f()
    return time.time() - start
def latency1000000(f): return latency(lambda: [f() for _ in range(1000000)])
def latency1000(f): return latency(lambda: [f() for _ in range(1000)])

def lxml_text_div():
    div = etree.Element("div")
    div.text = "Text Text"
    return etree.tostring(div)

print("            join latency: ", latency1000000(lambda: "".join(["<div>", "Text", "Text", "</div>"])), "us")
print("         fasttag latency: ", latency1000000(lambda: fasttag.Div("Text", "Text")), "us")
print("join+html.escape latency: ", latency1000000(lambda: "".join(["<div>", html.escape("Text"), html.escape("Text"), "</div>"])), "us")
print("        dominate latency: ", latency1000000(lambda: dominate.tags.div("Text", "Text")), "us")
print("        fasthtml latency: ", latency1000000(lambda: fasthtml.common.Div("Text", "Text")), "us")
print("            lxml latency:", latency1000000(lambda: lxml_text_div()), "us")
