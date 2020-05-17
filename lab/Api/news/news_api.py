'''
 For any lookup please visit to newsapi.org
 Functions:
    get_top_headlines(api_key, **kwargs)
    get_custom_news(api_key, **kwargs)

 FOR TOP_HEADLINES:
        !NOTE dont mix sources and either of category or country
 language, pageSize, page, apiKey, sources,
 q, category, country

FOR CUSTOM NEWS
 language, pageSize, page, apiKey, sources,
 q, domains, excludeDomains, _from, to, sortBy
'''

import os
import sys
import time
import json
from datetime import datetime
import requests

t1 = time.time()
API_KEY = os.getenv('NEWS_API_KEY')
if not API_KEY:
    message = """
    No api key found..... Generate an Api key by going to
    newsapi.org and create an environment variable by name
    NEWS_API_KEY...."""
    print(message)
    API_KEY = input("You can also paste here if you have one-> ")
    if not API_KEY:
        sys.exit(1)

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
    AppleWebKit/537.36(KHTML, like Gecko)\
    Chrome/39.0.2171.95 Safari/537.36'
    }

def get_top_headlines(api_key, **kwargs):
    '''
    Returns: A list of news dictionaries
    Params: api_key
    Optional_params: language, pageSize, page, apiKey, sources,
                        q, category, country
    '''

    basic_url = ['https://newsapi.org/v2/top-headlines?language=en&']
    for param,value in kwargs.items():
        string = '{0}={1}&'.format(param, value)
        basic_url.append(string)

    api_str = 'apiKey={0}'.format(api_key)
    basic_url.append(api_str)
    url = "".join(basic_url)

    response = requests.get(url, headers=headers)
    response_dict = response.json()
    total_news = response_dict['totalResults']
    status = response_dict['status']
    news_list = response_dict['articles']
    refined_news_list = []
    for index, news in enumerate(news_list):
        title = news['title']
        source = news['source']['name']
        news_url = news['url']
        image_url = news['urlToImage']
        summary = news['description']
        date = news['publishedAt']

        final_news_dict = {
            'title': title,
            'date': date,
            'source': source,
            'summary':summary,
            'news_url': news_url,
            'image_url': image_url
        }
        refined_news_list.append(final_news_dict)
        print("Written", index, "out of", total_news)

    print("Got", url, "in", response.elapsed.total_seconds())
    return refined_news_list

def get_custom_news(api_key, **kwargs):
    '''
    Returns: A list of news dictionaries
    Params: api_key
    Optional_params: language, pageSize, page, apiKey, sources,
                     q, domains, excludeDomains, _from, to, sortBy
    '''


    basic_url = ['https://newsapi.org/v2/everything?language=en&']
    for param,value in kwargs.items():
        if param == '_from':  # from is reserved keyword in python
            string = 'from={0}&'.format(value)
        else:
            string = '{0}={1}&'.format(param, value)
        basic_url.append(string)

    api_str = 'apiKey={0}'.format(api_key)
    basic_url.append(api_str)
    url = "".join(basic_url)

    response = requests.get(url, headers=headers)
    response_dict = response.json()
    try:
        total_news = response_dict['totalResults']
    except:
        print("totalResults failed at ", url)
    status = response_dict.get('status', None)
    news_list = response_dict['articles']
    refined_news_list = []

    for index, news in enumerate(news_list):
        title = news.get('title', None)
        source_dict = news.get('source', None)
        if source_dict:
            source = source_dict.get('name', None)
        news_url = news.get('url', None)
        image_url = news.get('urlToImage', None)
        summary = news.get('description', None)
        date = news.get('publishedAt', None)

        final_news_dict = {
            'title': title,
            'date': date,
            'source': source,
            'summary':summary,
            'news_url': news_url,
            'image_url': image_url
        }
        refined_news_list.append(final_news_dict)
        print("Written", index, "out of", total_news)

    print("Got", url, "in", response.elapsed.total_seconds())
    return refined_news_list

def write_to_json(content, filename):
    with open(filename, 'w') as wf:
        json.dump(content, wf, indent=2)

#        -- Uncomment The lines  below lines for a demo use --------
top_headlines_list = get_top_headlines(API_KEY, pageSize=100)
write_to_json(top_headlines_list, 'extracted/top_headlines.json')

US_top_headlines_list = get_top_headlines(API_KEY, country='us', pageSize=100)
write_to_json(US_top_headlines_list, 'extracted/US_top_headlines.json')

india_top_headlines_list = get_top_headlines(API_KEY,
                         country='in', pageSize=100)
write_to_json(india_top_headlines_list, 'extracted/india_top_headlines.json')

tech_top_headlines_list = get_top_headlines(API_KEY,
                    category='technology', pageSize=100)
write_to_json(tech_top_headlines_list, 'extracted/tech_top_headlines.json')

sports_top_headlines_list = get_top_headlines(API_KEY,
                     category='sports', pageSize=100)
write_to_json(tech_top_headlines_list, 'extracted/sports_top_headlines.json')

# !!Note if using from: 1 month back from today is limit!
bitcoin_news_list = get_custom_news(API_KEY, q='bitcoin', pageSize=100,
                        _from='2019-03-11', to='2019-4-11')
write_to_json(bitcoin_news_list, 'extracted/bitcoin_news.json')

trump_news_list = get_custom_news(API_KEY, q='trump', pageSize=100,
                     sortBy='popularity')
write_to_json(trump_news_list, 'extracted/trump_news.json')

elon_news_list = get_custom_news(API_KEY, q='elon musk', pageSize=100)
write_to_json(elon_news_list, 'extracted/elonmusk_news.json')
