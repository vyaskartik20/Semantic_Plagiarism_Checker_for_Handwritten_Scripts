import requests

# page = requests.get("https://www.iist.ac.in/aboutus/chancellor/drkalambiodata")

url="https://www.iist.ac.in/aboutus/chancellor/drkalambiodata"

page='z'
try:
    page = requests.get(url,timeout=3)
    # r.raise_for_status()
except requests.exceptions.HTTPError as errh:
    x=1
    # print ("Http Error:",errh)
except requests.exceptions.ConnectionError as errc:
    x=1
    # print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    x=1
    # print ("Timeout Error:",errt)
except requests.exceptions.RequestException as err:
    x=1
    # print ("OOps: Something Else",err)