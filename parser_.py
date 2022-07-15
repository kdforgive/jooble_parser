from bs4 import BeautifulSoup
from typing import Generator, Optional


class Item:
    """fields for item representation,
     method for (create_empty_item) dict construct"""
    def __init__(self):
        self.job_name = ''
        self.job_url = ''
        self.salary = ''
        self.short_description = ''
        self.description = ''

    def add_items_to_dict(self):
        return {
            'job_name': self.job_name,
            'job_url': self.job_url,
            'salary': self.salary,
            'short_description': self.short_description,
            'description': self.description,
        }


class SoupFieldIds:
    """create class SoupFieldsIds, class_attr = keys"""
    job_name = '_3862j6'
    job_url = 'noopener nofollow'
    salary_tag = 'jNebTl'
    short_description = '_9jGwm1'
    full_description_raw = '_1yTVFy'
    vacancy_amount = '_22VJWN'


class ParserJooble:

    @staticmethod
    def soup_find_exception_checker(tag_element, tag, element, method, find_all=None):
        if find_all == 'find_all':
            souper = tag_element.find_all(tag, element)
            if souper is not None:
                # return ' '.join(souper[1].text.split())
                return souper
        souper = tag_element.find(tag, element)
        if souper is not None:
            if method == 'text':
                return souper.text
            elif method == 'get':
                return souper.get('href')
        else:
            return ''

    @staticmethod
    def count_pages_amount(vacancy_amount: int, items_per_page: int = 20):
        pages_amount = vacancy_amount // items_per_page + 1 \
            if vacancy_amount % items_per_page != 0 \
            else vacancy_amount // items_per_page
        return pages_amount

    def parse_pages_amount(self, page):
        soup = BeautifulSoup(page, 'lxml')
        # SoupFieldIds.vacancy_amount
        vacancy_amount_raw = self.soup_find_exception_checker(soup, 'div',
                                                              {'class': SoupFieldIds.vacancy_amount}, 'text')
        vacancy_amount = ''
        for char in vacancy_amount_raw:
            if char.isdigit():
                vacancy_amount += char
        return self.count_pages_amount(int(vacancy_amount))

    def parse_main_page(self, page: str) -> Generator[dict, None, None]:
        soup = BeautifulSoup(page, 'lxml')
        jobs_items = soup.find_all('article', class_='FxQpvm yKsady')
        for job_item in jobs_items:
            job_name = self.soup_find_exception_checker(job_item, 'span', {'class': SoupFieldIds.job_name}, 'text')
            job_url = self.soup_find_exception_checker(job_item, 'a', {'rel': SoupFieldIds.job_url}, 'get')
            salary_tag = self.soup_find_exception_checker(job_item, 'p', {'class': SoupFieldIds.salary_tag}, 'text')
            short_description = self.soup_find_exception_checker(job_item, 'div',
                                                                 {'class': SoupFieldIds.short_description}, 'text')
            yield self.create_item_main_page(job_name, job_url, salary_tag, short_description)

    def parse_salary(self, raw_salary: str) -> Optional[float]:
        if not isinstance(raw_salary, str):
            return
        stripped_salary = raw_salary.strip('$ € грн $/год. .')
        return stripped_salary
        # splitted_salary = stripped_salary.split('-')
        # replaced_salary = splitted_salary[0].replace(' ', '')
        # if replaced_salary[0].isdigit():
        #     return float(replaced_salary)
        # print('wrong salary data')
        # return

    def create_item_main_page(self, job_name: str, job_url: str, salary: str, short_description: str) -> dict:
        if not isinstance(job_url, str) or not job_url:
            return {}
        item = Item()  # Item() - create instance
        item.job_url = job_url
        item.job_name = job_name if isinstance(job_url, str) else ''
        item.short_description = short_description if isinstance(short_description, str) else ''
        item.salary = self.parse_salary(salary) if self.parse_salary(salary) is not None else ''
        return item.add_items_to_dict()  # item.to_dict - method or @property to create dictionary from this item

    def parse_subpage(self, page: str, item: dict):
        soup = BeautifulSoup(page, 'lxml')
        # to see captcha request on subpage
        print(soup.text)
        full_description = self.soup_find_exception_checker(soup, 'div', {'class': SoupFieldIds.full_description_raw},
                                                            'text', 'find_all')
        return self.subpage_update_item(item, full_description)

    @staticmethod
    def subpage_update_item(item: dict, full_description: str):
        item['description'] = full_description
        return item
