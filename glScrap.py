from bs4 import BeautifulSoup
import urllib
import sys
from urlparse import urlparse

output_html = True

url_str = sys.argv[1]
if not url_str.startswith('http'):
    url_str += 'http://'

url = urlparse(url_str)
abs_url = url.geturl()
domain = '{url.scheme}://{url.netloc}'.format(url=url)

r = urllib.urlopen(abs_url).read()
soup = BeautifulSoup(r, "html.parser")
chapters = [a for a in soup.find_all('a', href=True) \
            if url.path in a['href'] and a.has_attr('title')]

for i, c in enumerate(chapters):
    print "Scraping Chapter {}".format(i)
    r = urllib.urlopen(domain + c['href']).read()
    r = r.decode('GBK', 'ignore').encode('UTF-8')
    soup = BeautifulSoup(r, "html.parser")
    spans = soup.find_all('span')
    for span in spans:
        if not span.has_attr('zzz'):
            continue

        chp_title = soup.find_all('td', {'class': 'main_ArticleTitle'})[0] \
                                                                    .get_text()
        span.attrs.pop('style')  # strip styling from the page

        if output_html:
            content = str(span)
        else:
            if span.p:
                ps = span.find_all('p')
                content = "".join([p.get_text() for p in ps])
            else:
                content = span.get_text()
    
    with open('{}.html'.format(i), 'w+') as f:
        if output_html:
            f.write("<meta charset=\"utf-8\">")
            #f.write("<h3>{}</h3>".format(str(chp_title)))
            f.write(content)
        else:
            f.write(content.encode('utf-8'))
