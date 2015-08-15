from __future__ import print_function
import pywikibot


def fetch_label(ids):
    wikidata = pywikibot.Site('en','wikipedia').data_repository()

    id_to_label = dict()
    used_ids = set()

    def english_name(item):
        return item.get()['labels']['en']

    # using _id to avoid rewriting the keyword id
    while len(ids) > 0:
        _id = ids.pop()
        used_ids.add(_id)
        page = pywikibot.ItemPage(wikidata, _id)
        data = page.get()
        claims = data['claims']

        try:
            subclass_ofs = claims['P279'] # Property P279 is subclass of
            superclass_items = [superclass.target for superclass
                                in subclass_ofs]

            superclass_ids = [superclass_item.id
                              for superclass_item in superclass_items]

            ids.update(set(superclass_ids) - used_ids)
        except KeyError:
            superclass_ids = []

        id_to_label[_id] = {'subclass': superclass_ids}

        if 'en' in page.labels:
            id_to_label[_id]['title'] = page.labels['en']

    return id_to_label


if __name__ == "__main__":
    import pandas as pd
    import json

    fow = pd.read_csv('./flatten_field_of_work-index.csv')
    fow_names = set(fow.iloc[:, 0])
    # We can have the labels in the same json file for both the csvs
    with open('fow_ids.json', 'w') as json_file:
        json.dump(fetch_label(fow_names), json_file)
