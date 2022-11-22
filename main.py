import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_years_suffix(years):
    if 11 <= years <= 19:
        return "лет"

    if years % 10 == 1:
        return "год"

    if 2 <= years % 10 <= 4:
        return "года"

    return "лет"


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('wine_template.html')

    year_of_foundation = 1920
    years_exist = datetime.datetime.now().year - year_of_foundation
    suffix = get_years_suffix(years_exist)

    rendered_page = template.render(
        years_exist=f'{years_exist} {suffix}'
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
