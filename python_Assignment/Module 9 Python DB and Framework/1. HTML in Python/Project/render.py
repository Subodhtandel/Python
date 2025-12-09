import os
from django.template import Engine, Context

print("Current working directory:", os.getcwd())
print("Looking for:", os.path.abspath("templates/hello.html"))
print("Template exists:", os.path.isfile("templates/hello.html"))

engine = Engine(dirs=["templates"])
template = engine.get_template("hello.html")
context = Context({"name": "World"})
html = template.render(context)

print(html)
