import requests
import bs4 as bs


def berlingske_getContent(header):
    hrefs = header.find('h4', {'class': 'teaser__title d-inline-block font-s4'})('a')[0]['href']                # Targeting h4 tage of that class, it contains sub link to other page
    link_to_more = 'https://www.berlingske.dk' + hrefs                                                          # Reformating the url and passing the above result to it
    link_urltxt = requests.get(link_to_more)
    link_urltxt = link_urltxt.content
    soup = bs.BeautifulSoup(link_urltxt, 'lxml')
    unwanted = soup.find('aside', {'class': 'embedded-element embedded-factbox position-relative'})             # To take out text noise found sometime in 'aside' tage
    if unwanted:
        unwanted.extract()
    if not (soup.find('div', {'class': 'article-body'})):                                                       # If no content, return
        return
    contents = soup.findAll('div', {'class': 'article-body'})[0]('p')                                           # 'div' tag and then target first 'p' child

    content = ''
    for text in contents:
        text = text.text.strip()
        if 'ritzau' in text:                                                                          # To stop conisdering content of contain 'ritzau'
            break
        content = content + ' ' + text                                                                # To Build the content from multiple scrapped text as long 'ritzau' not comming yet
        if 'Fold sammen' in content:
            content = content.split('Fold sammen')                                                    # Fold sammen comes at the end, so take whatever before only
            content = content[0]

    return content