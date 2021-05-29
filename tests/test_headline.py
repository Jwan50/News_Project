from firebase_admin import firestore


def test_headline(headline, data_name):
    db = firestore.client()
    headline_scraped = str(headline)
    docs = db.collection(data_name).where('headline', '==', headline).stream()
    for doc in docs:
        head_f = u'{} => {}'.format(doc.id, doc.to_dict())
        head_f = head_f.split("=>")
        head_f = head_f[1]
        head_f = head_f.replace("'", '')
        head_f = head_f.split("headline: ")
        head_f = str(head_f[1])
        if "\xa0" in headline:
            head_f = head_f.replace("\xa0", " ")
        head_f = head_f.replace(u"'", u"")
        if 'content' in head_f:
            head_f = head_f.split(", content:")
            head_f = head_f[0]
        if 'provider' in head_f:
            head_f = head_f.split(", provider:")
            head_f = head_f[0]
        if 'category' in head_f:
            head_f = head_f.split(", category:")
            head_f = head_f[0]
        if 'date' in head_f:
            head_f = head_f.split(", date:")
            head_f = head_f[0]
        if "}" in head_f:
            head_f = head_f.replace("}", " ")
        head_f = head_f.replace(u"'", u"")
        head_f = head_f.strip()
        if head_f == headline_scraped:
            return True
        else:
            return False