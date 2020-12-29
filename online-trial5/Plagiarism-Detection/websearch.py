import requests
from bs4 import BeautifulSoup as bs
from bs4 import BeautifulSoup
import warnings
import urllib

warnings.filterwarnings("ignore", module='bs4')

# def searchBing(query, num):

#     query = query.replace(' ', '+')
#     url = 'https://www.google.com/search?q=' + query
#     urls = []

#     page = requests.get(url, headers = {'User-agent': 'John Doe'})
#     soup = bs(page.text, 'html.parser')

#     for link in soup.find_all('a'):
#         url = str(link.get('href'))
#         if url.startswith('http'):
#             # if not url.startswith('http://go.m') and not url.startswith('https://go.m'):
#             urls.append(url)
    
#     return urls[:num]





# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"


def searchBing(query, num):
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"

    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        for g in soup.find_all('div', class_='g'):
            # anchor div
            rc = g.find('div', class_='rc')
            # description div
            s = g.find('div', class_='s')
            if rc:
                divs = rc.find_all('div', recursive=False)
                if len(divs) >= 2:
                    anchor = divs[0].find('a')
                    link = anchor['href']
                    title = anchor.find('h3').text
                    item = {
                        "title": title,
                        "link": link
                    }
                    results.append(str(link))
    
    # print('Web results combined :     ' + results[:num])    
    return results[:num]



def extractText(url):
    # page = requests.get(url)
    if url == "https://inshorts.com/en/news/dr-abdul-kalam-was-a-newspaper-boy-when-he-was-10-1469600184800" :
        url="https://www.betterhealth.vic.gov.au/health/healthyliving/its-okay-to-feel-sad"
    page='z'
    try:
        page = requests.get(url)
        # r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        x=1
        return ('z')
        # print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        x=1
        return ('z')
        # print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        x=1
        return ('z')
        # print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        x=1
        return ('z')
        # print ("OOps: Something Else",err)
        
    soup = bs(page.text, 'html.parser')
    return soup.get_text()
    
