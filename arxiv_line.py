from datetime import datetime, timedelta
from datetime import date as dat
import re
import requests
import pickle
import os
from googletrans import Translator

import requests

# webhook POST先URL
API_URL = ''

# 検索ワード
QUERY = '(cat:cond-mat.supr-con)+AND+(abs:pressure)+AND+(abs:FeSe)'


def parse(data, tag):
    # parse atom file
    # e.g. Input :<tag>XYZ </tag> -> Output: XYZ

    pattern = '<' + tag + '>([\s\S]*?)<\/' + tag + '>'
    if all:
        obj = re.findall(pattern, data)
    return obj

def search_and_send(query, start, ids, api_url, today, yesterday):
    translator = Translator()
    counter = 0
    while True:
        # counter = 0


        url = 'http://export.arxiv.org/api/query?search_query=submittedDate:[' + yesterday + '0000+TO+' + today + '0000]+AND+' + query + '&start=' + str(start) + '&max_results=100&sortBy=lastUpdatedDate&sortOrder=descending'
        

        # Get returned value from arXiv API
        data = requests.get(url).text
        # Parse the returned value
        entries = parse(data, 'entry')
        for entry in entries:
            # Parse each entry
            url = parse(entry, 'id')[0]
            if not (url in ids):
                # parse
                title = parse(entry, 'title')[0]
                abstract = parse(entry, 'summary')[0]
                date = parse(entry, 'published')[0]

                # abstの改行を取る
                abstract = abstract.replace('\n', '')

                # 日本語化の部分
                title_jap = translator.translate(title, dest='ja')
                abstract_jap = translator.translate(abstract, dest='ja')

                message = '\n'.join(
                    ['<br>Title: ' + title, '<br><br>URL: ' + url, '<br><br>Published: ' + date,
                    '<br><br>JP_Abstract: ' + abstract_jap.text])

                # webhookへPost の部分
                response = requests.post(api_url, data={'value1': message})

                ids.append(url)
                counter = counter + 1
                if counter == 10:
                    return 0
        if counter == 0 and len(entries) < 100:
            requests.post(api_url, data={'value1': 'Currently, there is no available papers'})
            return 0
        elif counter == 0 and len(entries) == 100:
            # When there is no available paper and full query
            start = start + 100
        else:
            # requests.post(api_url, data={'value1': 'Currently, there is no more available papers'})
            return 0


if __name__ == '__main__':
    print('Publish')
    # setup ==========================================================
    # Set URL of API
    api_url = API_URL

    TODAY = dat.today().strftime('%Y%m%d')
    YESTERDAY = (dat.today() + timedelta(days=-1)).strftime('%Y%m%d')

    # Load log of published data
    # if os.path.exists('published.pkl'):
    #     ids = pickle.load(open('published.pkl', 'rb'))
    # else:
    #     ids = []
    ids = []

    # Query for arXiv API
    query = QUERY


    # start ==========================================================
    start = 0

    # Post greeting to your LINE
    dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    requests.post(api_url, data={'value1': dt})

    # Call function
    search_and_send(query, start, ids, api_url, TODAY, YESTERDAY)

    # Update log of published data
    # pickle.dump(ids, open('published.pkl', 'wb'))
