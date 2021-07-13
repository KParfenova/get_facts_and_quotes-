from bs4 import BeautifulSoup
import requests
import random 

def find_book(book):
    urls = []

    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        # выставляем и передаем такой заголовок в запросе чтобы притворяться настоящим браузером, а то сайт проверяет
    resp = requests.get(f'https://www.livelib.ru/find/works/{book}', headers = headers)

    soup = BeautifulSoup(resp.text, 'html.parser')

    divs = soup.find_all('div', {'class': 'll-redirect-book'})
    if len(divs) != 0:
        div = divs[0]

        a_s = div.find_all('a', {'class': 'title'})
        if len(a_s) != 0:
            a_0 = a_s[0]
            href = a_0['href']
            urls.append(href)
        else:
            urls.append("")


        spans = div.find_all('span', {'class': 'brow-stats'})
        a_s = spans[0].find_all('a')
        if len(a_s) >= 3:
            a_0 = a_s[2]
            href = a_0['href']
            urls.append(href)
        else:
            urls.append("")

    return urls


def find_facts(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        # выставляем и передаем такой заголовок в запросе чтобы притворяться настоящим браузером, а то сайт проверяет
    resp = requests.get(url)
        #, headers = headers

    resp.encoding = resp.apparent_encoding

    soup = BeautifulSoup(resp.text, 'html.parser')

    facts = ""
    divs = soup.find_all('div', {'class': 'bc-info__wrapper'})
    for div in divs:
        labels = div.find_all('label')
        for label in labels:
            label_text = label.text

            if (label_text == "История") or (label_text == "Интересные факты"):
                p_s = div.find_all('p')
                for p in p_s:
                    facts += p.text + '\n'
    return facts


def find_plot(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        # выставляем и передаем такой заголовок в запросе чтобы притворяться настоящим браузером, а то сайт проверяет
    resp = requests.get(url)
        #, headers = headers

    resp.encoding = resp.apparent_encoding

    soup = BeautifulSoup(resp.text, 'html.parser')

    plot = ""
    divs = soup.find_all('div', {'class': 'bc-info__wrapper'})
    for div in divs:
        labels = div.find_all('label')
        for label in labels:
            label_text = label.text


            if (label_text == "Сюжет"):
                p_s = div.find_all('p')
                for p in p_s:
                    plot += p.text+'\n'
    return plot

def find_rating(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        # выставляем и передаем такой заголовок в запросе чтобы притворяться настоящим браузером, а то сайт проверяет
    resp = requests.get(url)
        #, headers = headers

    resp.encoding = resp.apparent_encoding

    soup = BeautifulSoup(resp.text, 'html.parser')

    a = soup.find_all('a', {'class': 'bc-rating-medium'})
    a_0 = a[0]
    rating = a_0['title']
    return rating


def find_quote(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
    resp = requests.get(url + "#quotes", headers = headers)
    resp.encoding = resp.apparent_encoding

    soup = BeautifulSoup(resp.text, 'html.parser')

    quotes = []
    divs = soup.find_all('div', {'class': 'quote-card'})
    for div in divs:
        divs2 = div.find_all('div', {'class': 'lenta-card'})
        for div2 in divs2:
            p_s = div2.find_all('p')
            for p in p_s:
                quotes.append(p.text)
    r = random.randint(0, len(quotes) - 1)
    return quotes[r]




book = input()

urls = find_book(book)
url = 'https://www.livelib.ru' + urls[0]

facts = find_facts(url)
if facts != "":
    print("ФАКТЫ: ", facts)

plot = find_plot(url)
if plot != "":
    print('\n', '\n', "СЮЖЕТ: ", plot)

rating = find_rating(url)
print('\n', '\n', "РЕЙТИНГ НА LiveLib: ", rating[:len(rating)-3])

url_quote = 'https://www.livelib.ru' + urls[1]
quote = find_quote(url_quote)
print('\n\n', "ЦИТАТА: ", quote)