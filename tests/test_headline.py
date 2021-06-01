from firebase_admin import firestore


def test_headline(headline, data_name):
    db = firestore.client()
    headline_scraped = str(headline)
    docs = db.collection(data_name).where('headline', '==', headline).stream()      # Get news with the given headline
    for doc in docs:                                                                # Forloop whithin Json file recieved from firebase
        head_f = u'{} => {}'.format(doc.id, doc.to_dict())                          # to convert and reformat from Json to set of strings
        head_f = head_f.split("=>")
        head_f = head_f[1]                                                          # To exclude the first index as it is the document id which is not needed in the set
        head_f = head_f.replace("'", '')                                            # Clean the set strings from '
        head_f = head_f.split("headline: ")                                         # Splitting the string from where headline is located
        head_f = str(head_f[1])                                                     # Take index 1 as it contain the string after headline.
        if "\xa0" in headline:                                                      # \xa0 seen in string when retrieving object from Firebase
            head_f = head_f.replace("\xa0", " ")                                    # Remove \xa0
        head_f = head_f.replace(u"'", u"")
        if 'content' in head_f:                                                     # If content in string
            head_f = head_f.split(", content:")
            head_f = head_f[0]                                                      # removing content to keep only string related to headline
        if 'provider' in head_f:
            head_f = head_f.split(", provider:")
            head_f = head_f[0]
        if 'category' in head_f:
            head_f = head_f.split(", category:")
            head_f = head_f[0]
        if 'date' in head_f:
            head_f = head_f.split(", date:")
            head_f = head_f[0]
        if "}" in head_f:                                                           # If curly bracket found, to be removed
            head_f = head_f.replace("}", " ")
        head_f = head_f.replace(u"'", u"")
        head_f = head_f.strip()
        if head_f == headline_scraped:                                              # Compare the cleaned headline from firebase with the scraped headline
            return True
        else:
            return False