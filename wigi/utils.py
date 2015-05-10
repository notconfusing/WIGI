import pywikibot
import math


def english_label(qid, wikidata, retrieved=dict()):
    # TODO: write docstring
    if type(qid) is float:
        if math.isnan(qid):
            return qid
    # first see if we've done it
    try:
        return retrieved[qid]
    except KeyError:
        try:
            page = pywikibot.ItemPage(wikidata, qid)
            data = page.get()
            lab = data['labels']['en']
            retrieved[qid] = lab
            return lab
        except:
            retrieved[qid] = qid
            return qid
