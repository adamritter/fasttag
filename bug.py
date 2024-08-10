from fasttag import *

a=0

hello = html_from_str("hello")
for i in range(1, 10000):
    a += len(str((hello + hello)))
    