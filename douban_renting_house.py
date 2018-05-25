import sys
import time
import argparse
import requests
import bs4

# Douban house renting groups
MAIN_URL = {
    'Hangzhou': 'https://www.douban.com/group/145219/',
    'Beijing' : 'https://www.douban.com/group/fangzi/',
    'Shanghai': 'https://www.douban.com/group/shanghaizufang/'
}

# Open URL, return HTML data
def open_url(url):
    # fake User-Agent
    ua_headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    res = requests.get(url, headers = ua_headers)
    return res.text

# Find target
def find_target(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    target_table = soup.find_all("table", class_ = "olt")
    target_td = target_table[0].find_all("td", class_ = "title")
    return target_td

# Search keywords in target
def find_keyword(target_td, keyword = ''):
    for i in target_td:
        # keyword fit
        if(i.a['title'].find(keyword) != -1):
            print(i.a['title'])
            print(i.a['href'])
        else:
            continue

# Main process
def main():
    # Parser CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search', help='search keywords')
    parser.add_argument('-l', '--limit',  help='records limitation')
    parser.add_argument('-r', '--region', help='regions')
    args = parser.parse_args()
    # Get the CLI arguments
    # s = args.search; l = args.limit; r = args.region;

    # Set default arguments
    s = ''
    l = 1000
    r = 'Hangzhou'
    # Set CLI arguments
    if(args.search != None):
        s = args.search
    if(args.limit != None):
        l = args.limit
    if(args.region != None):
        r = args.region

    # form 0 to limit, step 25
    for i in range(0, int(l), 25):
        r = open_url(MAIN_URL[r] + 'discussion' + '?start=' + str(i))
        t = find_target(r)
        find_keyword(t, s)

if __name__ == '__main__':
    main()

