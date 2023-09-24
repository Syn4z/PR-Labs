import requests
from bs4 import BeautifulSoup


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


if __name__ == "__main__":
    url = "https://999.md/ro/list/real-estate/apartments-and-rooms?applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776"
    maxPages = 4

    links = parseLinks(url, maxPages)
    for link in links:
        print(link)
