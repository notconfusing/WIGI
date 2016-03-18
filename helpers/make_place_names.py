import pywikibot
import json
import sys

infile, outfile = sys.argv[1], sys.argv[2]

pobs = json.load(open(infile,'r'))


enwp = pywikibot.Site('en','wikipedia')
wikidata = enwp.data_repository()

def is_or_has_country(qid):
    countries = list() #we're going to return this
    page = pywikibot.ItemPage(wikidata, qid)
    data = page.get()
    claims = data['claims']
    for pid, claimlist in claims.iteritems():
        if pid == 'P17':
            for claim in claimlist:
                if claim.target:
                    countries.append(claim.target.title()) #this is part of a country
        if pid == 'P31':
            for claim in claimlist:
                    if claim.target.title() == 'Q6256':
                        countries.append(qid) #this actually is a  country

    return countries 

place_country = dict()

count=0
for place in pobs: #1 because the first index is nan
    try:
        place_country[place] = is_or_has_country(place)
        count += 1
        if count % 100 == 0:
            print count
    except:
        print 'error on {}'.format(place)

json.dump(place_country, open(outfile,'w'))
