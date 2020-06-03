#!/usr/bin/env python3

import argparse
from pprint import pprint
# Not sure if this is builtin or just something we have from installing
# mechanize
import urllib

import pandas as pd
import mechanize
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', action='store',
        help='Only process the first N rows.'
    )
    args = parser.parse_args()
    if args.n:
        n = int(args.n)
    else:
        n = None

    petition_excel = 'sign_list.xlsx'
    pdf = pd.read_excel(petition_excel)

    name_col_idx = 1
    form_data_rows = pdf.iloc[:, name_col_idx]

    br = mechanize.Browser()
    form_idx = 1

    if n:
        form_data_rows = form_data_rows[:n]
    n_rows = len(form_data_rows)

    good_indices = []
    bad_indices = []
    possible_noncaltech = []
    for i, form_data_row in tqdm(enumerate(form_data_rows), total=n_rows):
        # Could also get part after and include an request to the Advanced
        # Search form if you wanted.
        name = form_data_row.split('(')[0].strip()

        # Hack to filter out parts we likely don't want to include in search.
        name = ' '.join([x for x in name.split() if len(x) > 2])
        br.open('https://directory.caltech.edu/search/search')
        br.form = br.forms()[form_idx]
        br['searchtext'] = name

        try:
            # We don't actually care what the response is, just that we don't
            # get a 404. Could probably make this more efficient.
            response = br.submit()
            good_indices.append(i)
        except urllib.error.HTTPError as e:
            bad_indices.append(i)
            possible_noncaltech.append((i, form_data_row, name))

    if len(possible_noncaltech) > 0:
        print('Possible non-Caltech signatures:')
        pprint(possible_noncaltech)
    else:
        print('All good')

    good_df = pdf.iloc[good_indices]
    good_df.to_csv('good.csv')

    bad_df = pdf.iloc[bad_indices]
    bad_df.to_csv('bad.csv')

    import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    main()

