import grequests as gq
from sys import argv

API = ('https://wikidata.org/w/api.php?action=wbgetentities'
       '&sites=enwiki&props=labels&languages=en&format=json&ids=%s')


def fetch_label(ids):
    urls = [API % id for id in ids]

    rs = (gq.get(url) for url in urls)

    response = gq.imap(rs, size=20)

    for i, res in enumerate(response):
        parsed_json = res.json()
        print parsed_json['entities']

if __name__ == '__main__':
    print fetch_label(argv[1:])
