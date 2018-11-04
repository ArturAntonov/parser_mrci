import os
import re

import numpy as np

from parser_mrci.utils.files_n_folders import write_ticker
from parser_mrci.utils.parse import parse_for_days, parse_day_html


def is_block_end(tr_lxml):
    end_line = 'Total Volume and Open Interest'
    td_node = tr_lxml.xpath('.//td/text()')
    if not td_node:
        return True
    return td_node[0] == end_line


def print_dict_raw_data(dict_raw):
    for key in dict_raw.keys():
        print(key)
        data = dict_raw[key]
        for row in data:
            print(row)


def select_data_by_columns(raw_dictionary, all_columns, target_columns):
    dictionary = dict()
    indexes = [all_columns.index(col) for col in target_columns]

    for key in raw_dictionary.keys():
        updated_values = [np.array(value)[indexes].tolist() for value in raw_dictionary[key]]
        dictionary.update({key: updated_values})
    return dictionary


def cleanup_html(html_string):
    return html_string.replace('\r\n', '').replace('\n', '').replace('<br/>', '')


# extract year value from /ohlc/2019/
def extract_year(url):
    return url.strip('/').split('/')[-1]


# extract day value 190225 from /ohlc/2019/190225.php
def extract_day(url):
    return url.strip('/').split('/')[-1].split('.')[0]


# check html_tree for valid. If html has table[@class='strat'] then valid
def valid_html_tree(tree):
    table_lxml = tree.xpath('//table')
    if len(table_lxml) == 0:
        return False
    return True


s = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL /ohlc/2018/180831.php was not found on this server.</p>
</body></html>"""


# test_tree = html.fromstring(s)
# print valid_html_tree(test_tree)


# parse root folder and get paths to all "year" pages
def get_years_htmls(root_path):
    # print('get list of paths for', root_path)
    folders_list_all = [folder for folder in os.walk(root_path)][0][1]
    folders_list = filter(lambda folder: re.match(r'\d{4}', folder), folders_list_all)
    # print('folders_list', folders_list)

    years_html_paths = [os.path.join(root_path, folder, '%s.html' % (folder)) for folder in folders_list]
    # print('years_paths', years_html_paths)
    return years_html_paths


# test
# print get_years_htmls('ohlc')
# for path in get_years_htmls('ohlc'):
#     print path


def get_days_htmls(year_full_path):
    # print('get days_htmls from', year_full_path)
    folder = os.path.dirname(year_full_path)
    print('folder', folder)

    # 0 - for current root, 2 - for inner files, 1 - for inner folders
    days_htmls_all = [file for file in os.walk(folder)][0][2]
    days_htmls = filter(lambda file: re.match(r'\d{6}', file), days_htmls_all)
    return [os.path.join(folder, day_html) for day_html in days_htmls]


# test
# for path in get_days_htmls('ohlc\\2000\\2000.html'):
#     print path


# requests all data about days from years
def request_days_htmls(years_html_paths):
    for year_path in years_html_paths:
        print('working on ', year_path)
        parse_for_days(year_path)
    print('parsing was finished')


def process_day_html(day_html_file, ticker_names, target_columns):
    success = []
    failed = []
    try:
        print('process START', day_html_file)
        # parse html for single date
        dictionary, columns = parse_day_html(day_html_file, ticker_names)

        # print information
        # print_dict_raw_data(dictionary)
        # from all data choose target columns
        selected_dict = select_data_by_columns(dictionary, columns, target_columns)

        # write selected data to files
        for key in selected_dict.keys():
            write_ticker(key, selected_dict[key])
        print('process COMPLETE', day_html_file)
        success.append(day_html_file)
    except Exception as e:
        print('process FAIL', day_html_file, e)
        failed.append(day_html_file)
    return success, failed

# test
# process_day_html('ohlc\\2014\\140702.html')
