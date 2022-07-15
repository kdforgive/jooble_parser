from parser_ import ParserJooble
# from parser_ import parse_main_page, parse_pages_amount, parse_subpage
import requests
from requests_html import HTMLSession
import json
from typing import Optional

"""
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
    """


class CrawlerJooble:

    def __init__(self, date: Optional[int] = None, employment_type: int = 0, location: int = 0,
                 city: Optional[str] = None, salary_max: Optional[int] = None, salary_min: Optional[int] = None,
                 job: Optional[str] = None, salary: Optional[int] = None, experience: Optional[int] = None):
        self.date = date
        self.employment_type = employment_type
        self.location = location
        self.city = city
        self.salary_max = salary_max
        self.salary_min = salary_min
        self.job = job
        self.salary = salary
        self.experience = experience
        self._current_page = 1

    @staticmethod
    def headers() -> dict:
        return {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88'
                          ' Safari/537.36'
        }

    def main_page_url(self) -> str:
        url = f'https://ua.jooble.org/SearchResult?date={self.date}&jt={self.employment_type}&' \
                        f'loc={self.location}&p={self._current_page}&rgns={self.city}&salaryMax={self.salary_max}&' \
                        f'salaryMin={self.salary_min}&ukw={self.job}&withSalary={self.salary}&workExp={self.experience}'
        return url

    def crawl_main_page(self):
        session = HTMLSession()
        url = 'https://ua.jooble.org/SearchResult?rgns=%D0%9A%D0%B8%D1%97%D0%B2&ukw=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82%20python'
        resp = requests.get(url, self.headers())
        return resp.text

    def crawl_subpage(self, url: str):
        resp = requests.get(url=url)
        return resp.text

    def handler(self):
        pages_amount = None
        while True:
            first_page_raw = self.crawl_main_page()
            if pages_amount is None:
                pages_amount = ParserJooble().parse_pages_amount(first_page_raw)
            main_page_items_gen = ParserJooble().parse_main_page(first_page_raw)
            for item in main_page_items_gen:
                item_subpage_raw = self.crawl_subpage(item.get('job_url'))
                updated_item = ParserJooble().parse_subpage(item_subpage_raw, item)
                yield updated_item
            if self._current_page >= pages_amount:
                break
            self._current_page += 1
            print('---------------', self._current_page)

    def write_item_to_json(self, item: dict, file_name: str = 'data.json') -> None:
        with open(file_name, 'r', encoding="UTF-8") as r_file:
            data = json.load(r_file)
        data.append(item)
        with open(file_name, 'w', encoding='UTF-8') as w_file:
            json.dump(data, w_file, indent=4, ensure_ascii=False)

    def main(self):
        counter = 1
        for item in self.handler():
            self.write_item_to_json(item)
            print(f'item #{counter}')
            counter += 1


if __name__ == '__main__':
    x = CrawlerJooble(date=2, city='Київ', job='python программист')
    x.main()
