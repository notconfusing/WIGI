import pandas as pd


def split_func(string):
    string = string.replace('\n', ', ')
    cats = string.split(',')
    cats = [cat.strip() for cat in cats]
    cats = list(filter(lambda x: len(x) > 0, cats))
    return cats


bls_wd_match = pd.read_csv('../data/bls_wd.csv')
wd = pd.read_csv('../data/fm_occupation.csv')


# def get_bls_wd(wd):
bls_wd = bls_wd_match.copy(deep=True)
# bls = pd.read_csv('../data/labelled_bls_occupations.csv')
bls_wd = bls_wd[~bls_wd.wd_occupation.isnull()]
bls_wd['bls_total'] = bls_wd['bls_total'].apply(lambda x: float(x))

# Reduce percentage in the range of 0 to 1
bls_wd['bls_p_women'] = bls_wd['bls_p_women'].apply(lambda x: float(x)/100)

bls_wd['wd_occupation'] = bls_wd['wd_occupation'].apply(lambda x: split_func(x))

bls_wd['wd_total'] = bls_wd['wd_occupation'].apply(lambda x: wd.loc[wd['category'].isin(x)].sum().total)
bls_wd['wd_women'] = bls_wd['wd_occupation'].apply(lambda x: wd.loc[wd['category'].isin(x)].sum().female)
bls_wd['wd_p_women'] = bls_wd['wd_women']/bls_wd['wd_total']
bls_wd.to_csv('../data/bls_wd_matchup.csv')
