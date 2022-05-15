from bs4 import BeautifulSoup
import bs4
from typing import Generator, Union, Optional, List

soup_class_dict = {'job_name': '_3862j6',
                   'job_url': '_15V35X',
                   'salary_tag': 'jNebTl',
                   'short_description': '_9jGwm1',
                   'full_description_raw': '_1yTVFy'}


def soup_find_exception_checker(line: Union[str, bs4.element.ResultSet, bs4.element.Tag]):  # typing ?
    if isinstance(line, bs4.element.ResultSet):
        # list index error
        return ' '.join(line[1].text.split()) if line else 'empty field or wrong value'
    elif isinstance(line, bs4.element.Tag):
        return line.text.strip()
    return 'empty field or wrong value'


def count_pages_amount():
    pass


def parse_pages_amount():
    pass


def parse_main_page(page: str) -> Generator[dict, None, None]:
    soup = BeautifulSoup(page, 'lxml')
    jobs_items = soup.find_all('article', class_='FxQpvm yKsady')

    for job_item in jobs_items:
        job_name = soup_find_exception_checker(job_item.find('span', class_=soup_class_dict['job_name']).find('span'))
        job_url = soup_find_exception_checker(job_item.find('div', class_=soup_class_dict['job_url']).find('a').get('href'))
        salary_tag = soup_find_exception_checker(job_item.find('p', class_=soup_class_dict['salary_tag']))
        short_description = soup_find_exception_checker(job_item.find('div', class_=soup_class_dict['short_description']))
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


def create_item_main_page():
    pass


def parse_subpage(page: str, item: dict):
    soup = BeautifulSoup(page, 'lxml')
    full_description = soup_find_exception_checker(soup.find_all('div', class_=soup_class_dict['full_description_raw']))
    return subpage_update_item(item, full_description)


def subpage_update_item(item: dict, full_description: str) -> dict:
    pass
