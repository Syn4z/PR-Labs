import requests
from bs4 import BeautifulSoup
import json


def parseLinks(url, maxPages=None):
    linkList = []
    baseUrl = "https://999.md"
    page = 1
    try:
        while True:
            if maxPages is not None and page > maxPages:
                break
            response = requests.get(url + f"&page={page}")
            page += 1
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                pageLinks = soup.find_all("a", class_="js-item-ad")
                maxPageLink = soup.find("a", class_="is-last-page")
                for pageLink in pageLinks:
                    if pageLink == maxPageLink:
                        break
                    if baseUrl + pageLink.get('href') not in linkList:
                        linkList.append(baseUrl + pageLink.get('href'))
            else:
                print(f"Failed to retrieve the web page for page {page}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    return linkList


def extractInfoFromPage(url):
    baseUrl = "https://999.md"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    info = {}

    for groupTitle in ['Caracteristici', 'Condiții de utilizare', 'Adăugător', 'Subcategorie', 'Preț', 'Regiunea', 'Contacte']:
        section = soup.find('h2', string=groupTitle)
        if section or groupTitle == 'Preț' or groupTitle == 'Regiunea' or groupTitle == 'Contacte':
            info[groupTitle] = {}
            if groupTitle == 'Caracteristici':
                for li in section.find_next('ul').find_all('li', class_='m-value'):
                    key = li.find('span', class_='adPage__content__features__key').text.strip()
                    value = li.find('span', class_='adPage__content__features__value').text.strip()
                    info[groupTitle][key] = value
            elif groupTitle == 'Condiții de utilizare':
                for li in section.find_next('ul').find_all('li', class_='m-value'):
                    key = li.find('span', class_='adPage__content__features__key with-rules').text.strip()
                    value = li.find('span', class_='adPage__content__features__key with-rules').text.strip()
                    info[groupTitle][key] = value
            elif groupTitle == 'Adăugător':
                for li in section.find_next('ul').find_all('li', class_='m-no_value'):
                    key = li.find('span', class_='adPage__content__features__key').text.strip()
                    info[groupTitle][key] = None
            elif groupTitle == 'Subcategorie':
                value = (baseUrl + soup.find("a", class_="adPage__content__features__category__link").get('href'))
                info[groupTitle] = value
            elif groupTitle == 'Preț':
                key = ''
                for ul in soup.find_all('ul', {'class': 'adPage__content__price-feature__prices'}):
                    for li in ul.find_all('li'):
                        if not (not (li.get('class') != ['tooltip', 'adPage__content__price-feature__prices__price',
                                                         'is-main']) or not (
                                li.get('class') != ['tooltip', 'adPage__content__price-feature__prices__price'])):
                            continue
                        value = li.find('span', class_='adPage__content__price-feature__prices__price__value').text.strip()
                        value += ' ' + li.find('span', class_='adPage__content__price-feature__prices__price__currency').text.strip()
                        if li.find('span', class_='adPage__content__price-feature__prices__price__currency').text.strip() == '€':
                            key = 'Euro'
                        elif li.find('span', class_='adPage__content__price-feature__prices__price__currency').text.strip() == 'lei':
                            key = 'Lei'
                        elif li.find('span', class_='adPage__content__price-feature__prices__price__currency').text.strip() == '$':
                            key = 'USD'
                        info[groupTitle][key] = value
            elif groupTitle == 'Regiunea':
                address = ''
                value = soup.findAll('dd', {'itemprop': 'address'})
                for v in value:
                    address += v.text.strip()
                info[groupTitle] = address
            elif groupTitle == 'Contacte':
                value = soup.findAll('dt', string=groupTitle+': ')
                if not value:
                    info[groupTitle] = None
                else:
                    for v in value:
                        info[groupTitle] = v.find_next('dd').find_next('ul').find_next('li').find('a').get('href')
    return info


if __name__ == "__main__":
    inputUrl = "https://999.md/ro/list/real-estate/apartments-and-rooms?applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776"
    links = parseLinks(inputUrl, 1)
    pageInfo = []
    for link in links:
        print(link)
        resultInfo = extractInfoFromPage(link)
        if resultInfo and resultInfo:
            pageInfo.append(resultInfo)
    jsonData = json.dumps(pageInfo, ensure_ascii=False, indent=2)
    fileName = "extractedData.json"
    try:
        with open(fileName, 'w', encoding='utf-8') as json_file:
            json_file.write(jsonData)
        print(f"Data saved to {fileName}")
    except IOError as e:
        print(f"Error writing to {fileName}: {e}")
