def altinget_getContent(header):
    content = header.find('p').text.strip()
    return content