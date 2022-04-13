import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('superjob', 'hh', 'rabota')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]


def superjob(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.superjob.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': '_1ID8B'})
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'Fo44F QiY08 LvoDO'})
                for div in div_lst:
                    title = div.find('span', attrs={'class': '_1BiPY _26ig7 _1d47O'})
                    href = title.a['href']
                    cont = div.find('span', attrs={'class': '_38T7m _3_Xlr _26ig7 OCAdW _18w_0 _3GBbL'})
                    content = cont.text
                    company = 'No name'
                    comp = div.find('span', attrs={'class': 'f-test-text-vacancy-item-company-name'})
                    if comp:
                        company = comp.text
                    jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def hh(url, city=None, language=None):
    jobs = []
    errors = []
    # domain = 'https://hh.ru/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='a11y-main-content')
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})
                for div in div_lst:
                    _div = div.find('div', attrs={'class': 'vacancy-serp-item-body'})
                    if _div:
                        title = div.find('h3', attrs={'class': 'bloko-header-section-3'})
                        href = title.a['href']
                        cont = div.find('div', attrs={'class': 'g-user-content'})
                        content = cont.text
                        company = 'No name'
                        p = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
                        if p:
                            company = p.text
                        jobs.append({'title': title.text, 'url': href, 'description': content, 'company': company,
                                     'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def rabota(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.rabota.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'index-page__body'})
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'vacancy-preview-card__top'})
                for div in div_lst:
                    title = div.find('h3', attrs={'class': 'vacancy-preview-card__title'})
                    href = title.a['href']
                    cont = div.find('div', attrs={'class': 'vacancy-preview-card__short-description'})
                    content = cont.text
                    company = 'No name'
                    a = div.find('span', attrs={'class': 'vacancy-preview-card__company-name'})
                    if a:
                        company = a.text
                    jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


if __name__ == '__main__':
    url = 'https://kaliningrad.rabota.ru/?query=python&sort=relevance'
    jobs, errors = rabota(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
