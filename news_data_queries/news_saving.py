from firebase_admin import firestore


def news_save(provider, headline, content, dt, category, data_name):
    try:
        db = firestore.client()
        data = {'category': category,
                'content': content,
                'date': dt,
                'headline': headline,
                'provider': provider
                }
        db.collection(data_name).add(data)
        if news_save:
            print('Category: ', category, ' -Headline', headline, ' -Content', content, '- Date', dt)

    except Exception as e:
        print('Problem sending data to: ' + data_name)
