#! /usr/bin/env python

from __future__ import print_function
import pywikibot


def fetch_label(ids):
    wikidata = pywikibot.Site('en', 'wikipedia').data_repository()

    id_to_label = dict()
    used_ids = set()

    def english_name(item):
        return item.get()['labels']['en']

    while len(ids) > 0:
        _id = ids.pop()
        print(_id)
        used_ids.add(_id)
        page = pywikibot.ItemPage(wikidata, _id)

        # take care of deleted Wikidata entries
        # for example, Q3537387
        try:
            data = page.get()
            claims = data['claims']
        except (pywikibot.NoPage, NotImplementedError):
            id_to_label[_id] = {}
            continue

        try:
            subclass_ofs = claims['P279'] # Property P279 is 'subclass of'
            superclass_items = [superclass.target
                                for superclass in subclass_ofs]
            superclass_ids = [superclass_item.id
                              for superclass_item in superclass_items]
            ids.update(set(superclass_ids) - used_ids)
        except (KeyError, AttributeError):
            superclass_ids = []

        id_to_label[_id] = {'subclass': superclass_ids}
        if 'en' in page.labels:
            id_to_label[_id]['title'] = page.labels['en']

    return id_to_label


if __name__ == "__main__":
    import pandas as pd
    import json
    from sys import argv, exit

    if len(argv) < 3:
        print("Usage: subclass_graph.py <input file> <output file>\n\n"
              "Generates a JSON output file containing the title field of\n"
              "a Wikidata QID and the QIDs of which it is a subclass.\n"
              "The first column of input file must contain Wikidata QIDs.")
        exit(0)

    data = pd.read_csv(argv[1])
    data_qids = set(data['qid'])


    with open(argv[2], 'w') as json_file:
        json.dump(fetch_label(data_qids), json_file)
