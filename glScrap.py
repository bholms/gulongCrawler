import urllib
import argparse
import os
from bs4 import BeautifulSoup
from urlparse import urlparse


def main():
    parser = argparse.ArgumentParser(description='Process arguments')
    parser.add_argument('bookURL', type=str,
            help='Book page URL from www.gulongbbs.com')
    args = parser.parse_args()
    url_str = args.bookURL
    # expecting the URL to look like: https://www.gulongbbs.com/book/cqsj/
    book_name = url_str.split('/')[-2]  # "cqsj"
    output_path = make_path(book_name)

    url = clean_url(url_str)
    toHtml = True
    content = crawl(url, toHtml)
    writeOut(content, output_path, toHtml)


def make_path(book_name):
    directory = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(directory, book_name)
    print output_path
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path


def clean_url(url_str):
    if not url_str.startswith('http'):
        url_str += 'http://'
    return urlparse(url_str)


def crawl(url, toHtml):
    abs_url = url.geturl()
    domain = '{url.scheme}://{url.netloc}'.format(url=url)

    r = urllib.urlopen(abs_url).read()
    soup = BeautifulSoup(r, "html.parser")
    chapters = [a for a in soup.find_all('a', href=True)
                if url.path in a['href'] and a.has_attr('title')]

    result_content = []
    for chp_index, chp in enumerate(chapters):
        print "Scraping Chapter {0}: {1}".format(chp_index + 1, chp['title'].encode('utf-8'))
        r = urllib.urlopen(domain + chp['href']).read()
        r = r.decode('GBK', 'ignore').encode('UTF-8')
        soup = BeautifulSoup(r, "html.parser")
        spans = soup.find_all('span')
        # chp_title = soup.find_all('td', {'class': 'main_ArticleTitle'})[0].get_text()
        for span in spans:
            if not span.has_attr('zzz'):
                continue

            span.attrs.pop('style')  # strip styling from the page

            if toHtml:
                content = str(span)
            else:
                if span.p:
                    ps = span.find_all('p')
                    content = "".join([p.get_text() for p in ps])
                else:
                    content = span.get_text()
            result_content.append(content)
    return result_content


def writeOut(content, path, toHtml):
    for i, chp_content in enumerate(content):
        with open('{}/{}.html'.format(path, i), 'w+') as f:
            if toHtml:
                f.write("<meta charset=\"utf-8\">")
                # f.write("<h3>{}</h3>".format(str(chp_title)))
                f.write(chp_content)
            else:
                f.write(chp_content.encode('utf-8'))
    print "Files have been written to: " + path

if __name__ == "__main__":
    main()
