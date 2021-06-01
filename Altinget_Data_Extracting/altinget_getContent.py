def altinget_getContent(header):
    content = header.find('p').text.strip()         # Targeting 'p' tage to get the content
    return content