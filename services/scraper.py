import requests
import html5lib
from pprint import pprint
from bs4 import BeautifulSoup
from functools import cmp_to_key


def runScrape(url, tags):
    response = requests.get(url)
    results = {}
    for tag in tags:
        if tag == 'url':
            results['urls'] = goScrapeUrl(response, url)
        elif tag == 'img':
            results['images'] = goScrapeImg(response)
        elif tag == 'title':
            results['titles'] = goScrapeTitles(response)
    return results


def goScrapeUrl(response, url):
    tag = 'a'
    soup = BeautifulSoup(response.content, 'html5lib')
    result = soup.find_all(tag, href=True)
    tests = []
    for r in result:
        if r['href'].startswith('http') is False or r['href'].startswith('https') is False:
            test = str(url.rsplit('/')[0]) + '//' + \
                   str(url.rsplit('/')[2]) + r['href']
            tests.append(test)
        else:
            tests.append(r['href'])
    tests = list(set(tests))
    # Sort by number of slashes DESC
    sortedTests = sorted(tests, key=cmp_to_key(
        lambda x, y: y.count('/') - x.count('/')))
    return sortedTests


def goScrapeImg(response):
    tag = 'img'
    soup = BeautifulSoup(response.content, 'html5lib')
    result = soup.find_all(tag)
    links = [r['src']
             for r in result if r['src'].startswith('http') or r['src'].startswith('https')]
    return links


def goScrapeTitles(response):
    tag = 'h'
    soup = BeautifulSoup(response.content, 'html5lib')
    results = {}
    for n in range(1, 7):
        result = soup.find_all(tag + str(n), text=True)
        cleanedResult = [result[idx].getText().strip()
                         for idx, value in enumerate(result)]
        results['h' + str(n)] = cleanedResult
    pprint(results)
    return results
