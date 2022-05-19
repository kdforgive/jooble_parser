from bs4 import BeautifulSoup
import bs4
from typing import Generator, Union, Optional, List

soup_class_dict = {'job_name': '_3862j6',
                   'job_url': '_15V35X',
                   'salary_tag': 'jNebTl',
                   'short_description': '_9jGwm1',
                   'full_description_raw': '_1yTVFy',
                   'vacancy_amount': '_22VJWN'}


def soup_find_exception_checker(tag_element, tag, element, method, find_all=None):
    if find_all == 'find_all':
        souper = tag_element.find_all(tag, element)
        if souper is not None:
            return ' '.join(souper[1].text.split())

    souper = tag_element.find(tag, element)
    if souper is not None:
        if method == 'text':
            return souper.text
        elif method == 'get':
            return souper.get('href')
    else:
        return ''


def count_pages_amount(vacancy_amount: int, items_per_page: int = 20):
    pages_amount = vacancy_amount // items_per_page + 1 \
        if vacancy_amount % items_per_page != 0 \
        else vacancy_amount // items_per_page
    return pages_amount


def parse_pages_amount(page):
    soup = BeautifulSoup(page, 'lxml')
    vacancy_amount_raw = soup_find_exception_checker(soup, 'div', {'class': soup_class_dict['vacancy_amount']}, 'text')
    vacancy_amount = ''
    for char in vacancy_amount_raw:
        if char.isdigit():
            vacancy_amount += char
    return count_pages_amount(int(vacancy_amount))


def parse_main_page(page: str) -> Generator[dict, None, None]:
    soup = BeautifulSoup(page, 'lxml')
    jobs_items = soup.find_all('article', class_='FxQpvm yKsady')

    for job_item in jobs_items:
        job_name = soup_find_exception_checker(job_item, 'span', {'class': soup_class_dict['job_name']}, 'text')
        job_url = soup_find_exception_checker(job_item, 'a', {'rel': soup_class_dict['job_url']}, 'get')
        salary_tag = soup_find_exception_checker(job_item, 'p', {'class': soup_class_dict['salary_tag']}, 'text')
        short_description = soup_find_exception_checker(job_item, 'div', {'class': soup_class_dict['short_description']}, 'text')
        yield create_item_main_page(job_name, job_url, salary_tag, short_description)


def parse_salary(raw_salary: str) -> Optional[float]:
    if not isinstance(raw_salary, str):
        return
    stripped_salary = raw_salary.strip('$ € грн $/год. .')
    splitted_salary = stripped_salary.split('-')
    replaced_salary = splitted_salary[0].replace(' ', '')
    if replaced_salary[0].isdigit():
        return float(replaced_salary)
    print('wrong salary data')
    return


def create_item_main_page(job_name: str, job_url: str, salary: str, short_description: str):
    if not isinstance(job_url, str) or not job_url:
        return {}
    item = create_empty_item()
    item['job_url'] = job_url
    item['job_name'] = job_name if isinstance(job_url, str) else ''
    item['short_description'] = short_description if isinstance(short_description, str) else ''
    item['salary'] = parse_salary(salary) if parse_salary(salary) is not None else ''
    return item


def parse_subpage(page: str, item: dict):
    soup = BeautifulSoup(page, 'lxml')
    full_description = soup_find_exception_checker(soup, 'div', {'class': soup_class_dict['full_description_raw']}, 'text', 'find_all')
    return subpage_update_item(item, full_description)


def subpage_update_item(item: dict, full_description: str) -> dict:
    item['description'] = full_description
    return item


def create_empty_item():
    return {
        'main_job_name': '',
        'job_url': '',
        'salary': '',
        'short_description': '',
        'description': ''
    }
