import requests
from bs4 import BeautifulSoup


def parseLinks(url, maxPages=None):
    linkList = []
    baseUrl = "https://interauto.md"
    page = 1
    try:
        while True:
            if maxPages is not None and page > maxPages:
                break
            response = requests.get(url + f"/page/{page}")
            page += 1
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                pageLinks = soup.find_all("a", class_="cardojo-vehicle-block-thumbnail")
                # maxPageLink = soup.find("a", class_="is-last-page")
                for pageLink in pageLinks:
                    if len(linkList) != 0:
                        if pageLink == linkList[-1]:
                            break
                    if baseUrl + pageLink.get('href') not in linkList:
                        if "/booster" in pageLink.get('href'):
                            continue
                        else:
                            linkList.append(pageLink.get('href'))
            else:
                print(f"Failed to retrieve the web page for page {page}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    return linkList
