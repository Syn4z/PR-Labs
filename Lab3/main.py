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
                    linkList.append(baseUrl + pageLink.get('href'))
            else:
                print(f"Failed to retrieve the web page for page {page}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    return linkList


def extractInfoFromPage(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    caracteristiciSection = soup.find('h2', string='Caracteristici')

    if not caracteristiciSection:
        print(f"No 'Caracteristici' section found on {url}")
        return None

    info = {}
    for li in caracteristiciSection.find_next('ul').find_all('li', class_='m-value'):
        key = li.find('span', class_='adPage__content__features__key').text.strip()
        value = li.find('span', class_='adPage__content__features__value').text.strip()
        info[key] = value

    return info


if __name__ == "__main__":
    inputUrl = "https://999.md/ro/list/real-estate/apartments-and-rooms?applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776"

    links = parseLinks(inputUrl, 1)
    pageInfo = []
    resultInfo = extractInfoFromPage(links[0])
    if resultInfo:
        pageInfo.append(resultInfo)
    jsonData = json.dumps(pageInfo, ensure_ascii=False, indent=2)
    print(jsonData)
