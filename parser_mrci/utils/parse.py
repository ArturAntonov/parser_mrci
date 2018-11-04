# method for parse single html file for taget tickers
import os
import re

import requests
from lxml import html

from parser_mrci.utils.files_n_folders import create_folder, write_html_file, read_file
from parser_mrci.utils.paths import url_join, transform_to_path
from parser_mrci.utils.utils import extract_year, extract_day, valid_html_tree


def parse_day_html(file, tickers):
    text = read_file(file)

    tree = html.fromstring(text)
    table_tr_lxml = tree.xpath('//table/tr')
    columns = tree.xpath('//th[(@class = "colhead" or @class = "note") and not(@colspan)]/text()')
    # condition start parse

    dictionary = dict()
    rows = []
    for_load = False
    title = ''
    for tr in table_tr_lxml:
        th_lxml = tr.xpath('.//th')
        # if only one header per cell and header from targets
        if len(th_lxml) == 1 and th_lxml[0].text in tickers:
            title = th_lxml[0].text
            for_load = True
        else:
            if for_load:
                # init new block
                if is_block_end(tr):
                    # finish filling the block
                    dictionary.update({title: rows})
                    rows = []
                    for_load = False
                else:
                    # fill rows
                    rows.append(tr.xpath('.//td/text()'))
    return dictionary, columns


# parsing for root page and create root folder and root .html file
def parse_root_page(root_page, ohlc_page):
    http_root_url = url_join([root_page, ohlc_page])
    # create folder
    foldername = ohlc_page
    create_folder(foldername)
    # request for html
    r = requests.get(http_root_url)
    filename = '%s.html' % (str(ohlc_page))
    path = os.path.join(foldername, filename)
    write_html_file(path, r.text)
    return (foldername, filename, path)


# test
# parse_root_page()


# write year-html file to root_page/year folder
def request_and_write_year(root_page, year_url):
    # request
    r = requests.get(url_join([root_page, year_url]))

    # make folder
    folder_path = transform_to_path(year_url)
    create_folder(folder_path)

    # write file
    year_filename = '%s.html' % (str(extract_year(year_url)))
    path = os.path.join(folder_path, year_filename)
    print('path for html', path)
    write_html_file(path, r.text)


# write year-html file to root_page/year folder.
# In this case name of the folder for html is not equal url fro loader html
def request_and_write_year_current(root_page, current_year_url, year_url_original, current_year):
    # request
    r = requests.get(url_join([root_page, year_url_original]))

    # make folder
    folder_path = transform_to_path(current_year_url)
    create_folder(folder_path)

    # write file
    current_year_filename = '%s.html' % (str(current_year))
    path = os.path.join(folder_path, current_year_filename)
    print('path for year', path)
    write_html_file(path, r.text)


def request_and_write_day(root_page, day_url):
    print('request for ', url_join([root_page, day_url]))
    r = requests.get(url_join([root_page, day_url]))

    # from /ohlc/2018/180802.php take /ohlc/2018
    folder_path = transform_to_path(day_url[0:day_url.rfind('/')])

    # read html file and make tree from it
    tree = html.fromstring(r.text)

    if not valid_html_tree(tree):
        print('not valid', day_url)
        return

    # write file
    day_filename = '%s.html' % (extract_day(day_url))
    path = os.path.join(folder_path, day_filename)
    print('path for day', path)
    write_html_file(path, r.text)


# parsing years
# steps: open root page. find all date a/href. find current year "history".
# For all of years make folder (name - year) and load htmls <year>.html
# For current year make folder with year number.


def parse_for_years(root_page, root_html_path):
    # read html file and make tree from it
    text = read_file(root_html_path)
    tree = html.fromstring(text)

    # find all hrefs
    hrefs_original = tree.xpath('//table//a[contains(@href, "20") or contains(@href, "19")]/@href')
    current_href_original = tree.xpath('//table//a[contains(@href, "history")]/@href')[0]

    # create correct url for current year
    curr_year_mark = 'history.php'
    current_year_url = current_href_original.replace(curr_year_mark, '2018')

    # query html and store to specified folders
    for year_url in hrefs_original:
        request_and_write_year(root_page, year_url)

    # query current year
    request_and_write_year_current(root_page, current_year_url, current_href_original, '2018')


# test
# parse_for_years('ohlc\\ohlc.html')


def parse_for_days(root_page, year_html_path):
    # read html file and make tree from it
    text = read_file(year_html_path)
    tree = html.fromstring(text)

    xpath_re = re.compile(r'.*\d{6}')
    hrefs = tree.xpath('//table//th[@class = "field"]//a[match(@href)]/@href',
                       extensions={(None, 'match'): (lambda c, a: bool(xpath_re.match(a[0])))})
    # print hrefs
    for href in hrefs:
        request_and_write_day(root_page, href)

# test
# parse_for_days('ohlc\\2018\\2018.html')
