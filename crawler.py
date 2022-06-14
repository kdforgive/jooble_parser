from parser import parse_main_page, parse_pages_amount, parse_subpage
import requests
from requests_html import HTMLSession
import json
from bs4 import BeautifulSoup
from typing import Union


headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
}

# filter parameters:
    # date
        # none
        # date=8,2,3
    # salary
        # none
        # withSalary=true
        # salaryMin=
        # salaryMax=777&salaryMin=666
    # experience
        # none
        # workExp=1,2
    # location
        # none
        # near by ??
        # loc=2,3
    # employment_type
        # jt=1,2,3,6
# search parameters
    # city
        # rgns=Київ
    # job
        # ukw=python програмист
    # page
        # p=

BASE_URL = 'https://ua.jooble.org/SearchResult?date={date}&jt={employment_type}&loc={location}&p={page}&rgns={city}' \
           '&salaryMax={salary_max}&salaryMin={salary_min}&ukw={job}&withSalary={salary}&workExp={experience}'


def generate_url(date: int = None, employment_type: int = 0, location: int = 0, page: int = None, city: str = None,
                 salary_max: int = None, salary_min: int = None, job: str = None, salary: int = None,
                 experience: int = None, url_template: str = BASE_URL) -> str:
    return url_template.format(date=date, employment_type=employment_type, location=location, page=page, city=city,
                               salary_max=salary_max, salary_min=salary_min,  job=job, salary=salary,
                               experience=experience)


def crawl_main_page(page_number: int = 1):
    main_page_url = generate_url(date=2, city='Київ', job='python программист', page=page_number)
    resp = requests.get(main_page_url, headers)
    return resp.text


def crawl_subpage(url: str):
    session = HTMLSession()
    resp = session.get(url=url)
    return resp.text


def handler():
    pages_amount = None
    current_page = 1
    while True:
        first_page_raw = crawl_main_page(current_page)
        if pages_amount is None:
            pages_amount = parse_pages_amount(first_page_raw)
        main_page_items_gen = parse_main_page(first_page_raw)
        for item in main_page_items_gen:
            item_subpage_raw = crawl_subpage(item.get('job_url'))
            updated_item = parse_subpage(item_subpage_raw, item)
            yield updated_item
        if current_page >= pages_amount:
            break
        current_page += 1


def write_item_to_json(item: dict, file_name: str = 'data.json') -> None:
    with open(file_name, 'r', encoding="UTF-8") as r_file:
        data = json.load(r_file)
    data.append(item)
    with open(file_name, 'w', encoding='UTF-8') as w_file:
        json.dump(data, w_file, indent=4, ensure_ascii=False)


def main():
    counter = 1
    for item in handler():
        write_item_to_json(item)
        print(f'item #{counter}')
        counter += 1


if __name__ == '__main__':
    main()
