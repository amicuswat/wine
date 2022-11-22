import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('wine_template.html')

year_of_foundation = 1920
years_exist = datetime.datetime.now().year - year_of_foundation
suffix = "лет"
if 11 <= years_exist <= 19:
    suffix = "лет"
elif years_exist % 10 == 1:
    suffix = "год"
elif 2 <= years_exist % 10 <= 4:
    suffix = "года"

rendered_page = template.render(
    years_exist=f'{years_exist} {suffix}'
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
