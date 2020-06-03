#!/usr/bin/env python3

from pprint import pprint
# Not sure if this is builtin or just something we have from installing
# mechanize
import urllib

import pandas as pd
import mechanize


def main():
    petition_excel = 'sign_list.xlsx'
    pdf = pd.read_excel(petition_excel)

    name_col_idx = 1
    form_data_rows = pdf.iloc[:, name_col_idx]

    br = mechanize.Browser()
    form_idx = 1

    possible_noncaltech = []
    for i, form_data_row in enumerate(form_data_rows):
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
        except urllib.error.HTTPError as e:
            possible_noncaltech.append((i, form_data_row, name))

    if len(possible_noncaltech) > 0:
        print('Possible non-Caltech signatures:')
        pprint(possible_noncaltech)
    else:
        print('All good')


if __name__ == '__main__':
    main()

