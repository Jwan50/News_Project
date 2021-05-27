import requests
import bs4 as bs


def berlingske_getContent(header):
    hrefs = header.find('h4', {'class': 'teaser__title d-inline-block font-s4'})('a')[0]['href']
    link_to_more = 'https://www.berlingske.dk' + hrefs
    link_urltxt = requests.get(link_to_more)
    link_urltxt = link_urltxt.content
    soup = bs.BeautifulSoup(link_urltxt, 'lxml')
    unwanted = soup.find('aside', {'class': 'embedded-element embedded-factbox position-relative'})
    if unwanted:
        unwanted.extract()
    if not (soup.find('div', {'class': 'article-body'})):
        return
    contents = soup.findAll('div', {'class': 'article-body'})[0]('p')

    content = ''
    for text in contents:
        text = text.text.strip()
        if 'ritzau' in text:
            break
        content = content + ' ' + text
        if 'Fold sammen' in content:
            content = content.split('Fold sammen')
            content = content[0]

    return content