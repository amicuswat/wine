import os
import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv


def get_years_suffix(years):
    if 11 <= years <= 19:
        return "лет"

    if years % 10 == 1:
        return "год"

    if 2 <= years % 10 <= 4:
        return "года"

    return "лет"


if __name__ == '__main__':
    load_dotenv()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('wine_template.html')

    foundation_year = 1920
    exist_years = datetime.datetime.now().year - foundation_year
    suffix = get_years_suffix(exist_years)

    excel_wines_df = pandas.read_excel(os.environ['DATA_FILE'])
    excel_wines_df = excel_wines_df.fillna('-')
    excel_wines = excel_wines_df.to_dict('records')

    wines_by_category = collections.defaultdict(list)
    for wine in excel_wines:
        wines_by_category[wine['Категория']].append(wine)

    rendered_page = template.render(
        years_exist=f'{exist_years} {suffix}',
        wines=wines_by_category
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
