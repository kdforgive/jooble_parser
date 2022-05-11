from bs4 import BeautifulSoup
from typing import Generator, Union, Optional, List


def count_pages_amount():
    pass


def parse_pages_amount():
    pass


def parse_main_page(page: str) -> Generator[dict, None, None]:
    soup = BeautifulSoup(page, 'lxml')
    jobs_items = soup.find_all('article', class_='FxQpvm yKsady')

    for job_item in jobs_items:
        job_name = job_item.find('span', class_='_3862j6').find('span').text.strip()
        job_url = job_item.find('div', class_='_15V35X').find('a').get('href')
        salary_tag = job_item.find('p', class_='jNebTl')
        salary = None
        if salary_tag is not None:
            salary = salary_tag.text.strip()
        short_description = job_item.find('div', class_='_9jGwm1').text.strip()
        yield create_item_main_page(job_name, job_url, salary, short_description)


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
