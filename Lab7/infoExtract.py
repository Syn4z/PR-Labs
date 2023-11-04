import requests
from bs4 import BeautifulSoup


def extractInfoFromPage(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    info = {}

    for groupTitle in ['Titlu', 'Preț', 'Vânzător', 'Caracteristici', 'Opțiuni și dotări autoturism']:
        info[groupTitle] = {}
        if groupTitle == 'Titlu':
            category = soup.find('h2', class_='product-title')
            value = category.text.strip()
            info[groupTitle] = value
        elif groupTitle == 'Preț':
            value = soup.find('span', class_='cardojo-Price-amount amount').text.strip()
            value += soup.find('span', class_='cardojo-Price-currencySymbol').text.strip()
            info[groupTitle] = value
        elif groupTitle == 'Vânzător':
            category = soup.find('div', class_='media-body')
            value = category.find('h5', class_='mb-0').text.strip()
            info[groupTitle] = value
        elif groupTitle == 'Caracteristici':
            for category in soup.find_all('div', class_='rounded shadow bg-dark position-relative single_car__specifications'):
                for row in category.find_all('div', class_='col-6 col-md-4 item'):
                    key = row.find('h6').text.strip()
                    value = row.find('h4').text.strip()
                    info[groupTitle][key] = value
        elif groupTitle == 'Opțiuni și dotări autoturism':
            for category in soup.find_all('div', class_='rounded shadow bg-dark d-print-none single_car__specifications'):
                for li in category.find_next('ul').find_all('li'):
                    key = li.text.strip()
                    info[groupTitle][key] = None
    return info
