from bs4 import BeautifulSoup
import requests
import random
import json
import wikipedia

#-- get request to site

curSession = requests.Session()
agents_idx = 0

def get_request(url):
    global curSession
    global agents_idx

    agents = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
        'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFAPWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36'
    ]

   # выставляем и передаем такой заголовок в запросе чтобы притворяться настоящим браузером,
   # а то сайт проверяет
    headers = {
       'User-Agent': agents[agents_idx % 12]
    }
    agents_idx += 1

    #-- reuests
    resp = curSession.get(url, headers = headers)
    resp.encoding = resp.apparent_encoding
    res = resp.text

    # проверяем что страница пришла хорошая
    soup = BeautifulSoup(res, 'html.parser')
    a_s = soup.find_all('a', {'class': 'page-header__search-btn'})
    if len(a_s) <= 0:
        print("\n\n !!!! ПУСТАЯ СТРАНИЦА !!!!", url)
        f = open("_page.html", "w")
        f.write(res)
        f.close
        res = ""

    return res


#-- parse pages

def find_book(book):

    url = f'https://www.livelib.ru/find/works/{book}'

    book2 = book.replace(' ', '+')
    url = f'https://www.livelib.ru/find/{book2}'

    resp = get_request(url)
    if (resp == ""):
        return "","","",""
    soup = BeautifulSoup(resp, 'html.parser')


    urls = []
    divs = soup.find_all('div', {'class': 'll-redirect-book'})
    if len(divs) != 0:
        div = divs[0]

        a_s = div.find_all('a', {'class': 'title'})
        if len(a_s) != 0:
            a_0 = a_s[0]
            href = a_0['href']
            urls.append(href)
        else:
            return "","","",""


        spans = div.find_all('span', {'class': 'brow-stats'})
        a_s = spans[0].find_all('a')
        if len(a_s) >= 3:
            a_0 = a_s[2]
            href = a_0['href']
            if href != "javascript:void(0);":
                urls.append(href)
        else:
            return "","","",""

    print(url, urls)

    #----------------

    url = 'https://www.livelib.ru' + urls[0]
    resp = get_request(url)
    if (resp == ""):
        return "","","",""
    soup = BeautifulSoup(resp, 'html.parser')


    #-- find_facts

    facts = []
    divs_1 = soup.find_all('div', {'class': 'bc-info__wrapper'})
    for div in divs_1:
        labels_1 = div.find_all('label')
        for label in labels_1:
            label_text = label.text
            if (label_text == "История") or (label_text == "Интересные факты"):
                p_s = div.find_all('p')
                for p in p_s:
                    facts.append(p.text)
    if len(facts) != 0:
        r = random.randint(0, len(facts) - 1)
        fact = facts[r]
    else:
        fact = ""

    #-- find_plot

    plot = ""
    divs_2 = soup.find_all('div', {'class': 'bc-info__wrapper'})
    for div in divs_2:
        labels_2 = div.find_all('label')
        for label in labels_2:
            label_text = label.text
            if (label_text == "Сюжет"):
                p_s = div.find_all('p')
                for p in p_s:
                    plot += p.text
                    break
    #----- annotate
    anot = ""
    divs_4 = soup.find_all('div', {'class': 'bc-annotate without-readmore'})
    #d_4 = divs_4.find_all('div', {'class': 'lenta-card__text-edition-full'})
    for d in divs_4:
        anot = d.text
        break

    #-- find_rating

    a = soup.find_all('a', {'class': 'bc-rating-medium'})
    a_0 = a[0]
    rating = a_0['title']


    #-- find_quote

    resp = ""
    if len(urls) > 1:
        url_quote = 'https://www.livelib.ru' + urls[1]
        resp = get_request(url_quote)
    if (resp == ""):
        return "","","",""

    soup = BeautifulSoup(resp, 'html.parser')
    quotes = []
    divs_3 = soup.find_all('div', {'class': 'quote-card'})
    for div in divs_3:
        divs2 = div.find_all('div', {'class': 'lenta-card'})
        for div2 in divs2:
            p_s = div2.find_all('p')
            for p in p_s:
                quotes.append(p.text)

    if len(quotes) !=0:
        r1 = random.randint(0, len(quotes) - 1)
        quote = quotes[r1]
    else:
        quote = ""

    return fact, plot, anot, rating, quote

def save_data(data_books):
    with open('data_books.json', 'w', encoding="utf-8") as outfile:
        json.dump(data_books, outfile, indent=4, ensure_ascii=False)



###----- read json

with open('books.json', 'r', encoding="utf-8") as json_file:
    data = json.load(json_file)

data_books = {}

s = data["data"]["meta"]["_getSrcObsWh6Q9"]["edges"]
for i in s:
    book_all = i["node"]
    book = book_all["name"]

    if book not in data_books.keys():
        #facts, plot, rating, quote = "", "", "", ""
            
        facts, plot, anot, rating, quote = find_book(book)
        if plot == "":
            plot = anot
            
        data_books[str(book)] = { "facts": facts,
                    "plot": plot,
                    "rating": rating,
                    "quote": quote}
        #print(data_books)
        save_data(data_books)




"""
    if facts != "":
        print('\n\n', "ФАКТЫ: ", facts)

    if plot != "":
        print('\n', '\n', "СЮЖЕТ: ", plot)

    print('\n', '\n', "РЕЙТИНГ НА LiveLib: ", rating[:len(rating)-3])

    print('\n\n', "ЦИТАТА: ", quote)
"""
#------------



