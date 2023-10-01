import json
from inClass import parseLinks
from homework import extractInfoFromPage

if __name__ == "__main__":
    inputUrl = "https://999.md/ro/list/real-estate/apartments-and-rooms?applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776"
    links = parseLinks(inputUrl, 3)
    jsonLinks = json.dumps(links, indent=2)
    fileName = "extractedLinks.json"
    try:
        with open(fileName, 'w', encoding='utf-8') as json_file:
            json_file.write(jsonLinks)
        print(f"Links saved to {fileName}")
    except IOError as e:
        print(f"Error writing to {fileName}: {e}")
    pageInfo = []
    for link in links:
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
