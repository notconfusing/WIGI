from __future__ import print_function
import pywikibot

def fetch_label(ids):
    wikidata = pywikibot.Site('en','wikipedia').data_repository()

    def english_name(item):
        return item.get()['labels']['en']

    id_to_label = {}
    for id in ids:
        print(id)
        page = pywikibot.ItemPage(wikidata, id)
        data = page.get()
        claims = data['claims']

        try:
            subclass_ofs = claims['P279'] #Property P279 is subclass of
            superclass_items = [superclass.target for superclass
                                in subclass_ofs]

            superclass_names = [english_name(superclass_item) for
                                superclass_item in superclass_items]
        except KeyError:
            superclass_names = ['Uncategorized']

        id_to_label[id] = {'subclass': superclass_names}

        if 'en' in page.labels:
            id_to_label[id]['title'] = page.labels['en']

    return id_to_label

if __name__ == '__main__':
    """ Categorizes pages from Wikidata based on their subclass.

    First argument is output file name followed by list of Wikidata ids.
    """
    import json, sys

    if sys.argv[1].startswith('Q'):
        print(fetch_label(sys.argv[1:]))
    else:
        with open (sys.argv[1], 'w') as f:
            json.dump(fetch_label(sys.argv[2:]), f)
