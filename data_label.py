import requests as rq
from sys import argv

API = 'https://wikidata.org/w/api.php'


def fetch_label(id):
    data = {'action': 'wbgetentities',
            'ids': id,
            'sites': 'enwiki',
            'props': 'labels',
            'language': 'en',
            'format': 'json'}

    response = rq.get(API, params=data)

    if response.ok:
        parsed_json = response.json()
        #print map(lambda x:
                  #parsed_json['entities'][x]['labels']['en']['value'], ids)
        return parsed_json['entities'][id]['labels']['en']['value']
    else:
        print 'Failed!'


if __name__ == '__main__':
    print fetch_label(argv[1])
