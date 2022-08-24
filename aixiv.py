import urllib.request
import datetime as dt
import re


def main():
    basedate = dt.date.today()+dt.timedelta(days=-1)
    previousdate = basedate +dt.timedelta(days=-1)

    url_q = 'http://export.arxiv.org/api/query?search_query=submittedDate:['+previousdate.strftime('%Y%m%d')+'1400+TO+'+basedate.strftime('%Y%m%d')+'1400]+AND+(cat:astro-ph.EP)&start=0&sortBy=submittedDate&sortOrder=ascending'
    data = urllib.request.urlopen(url_q).read().decode('utf-8')
    #
    parse = lambda a,b: re.findall("<" + b + ">([\s\S]*?)<\/" + b + ">", a)
    #
    entries = parse(str(data), "entry")
    for entry in entries:
        url = parse(entry, "id")[0]
        title = parse(entry, "title")[0]
        author = ', '.join(parse(entry, "name") )
        summary = parse(entry, "summary")[0]
        print( '%s\n%s\n%s\n%s' % (url, title, author, summary) )

if __name__ == '__main__':
    main()