import os

from parser_mrci.utils.paths import cleanup_path


def read_file(filename):
    with open(filename) as fin:
        text = fin.read()
        return text


# create folder if it doesn't exists
def create_folder(foldername):
    if not os.path.exists(foldername):
        print('create folder', foldername)
        os.makedirs(foldername)
    return foldername


# create file and create table structure
def create_file_csv(filename, headers=[], delimiter=','):
    file_name = cleanup_path(filename + '.csv')
    with open(file_name, 'w') as fout:
        fout.write(delimiter.join(str(h) for h in headers))
        fout.write('\n')
    return file_name


# test
# create_file_csv('test_create_headers', ['col1', 'col2'])
# create_file_csv('test_create_wo_headers')
# create_file_csv('test_create_headers_delimiter', ['col1', 'col2'], ';')

# create or update file
# should return name of file


def create_or_update_file(filename, table_columns, extension='csv'):
    if not os.path.exists(filename + '.' + extension):
        filename = create_file_csv(filename, table_columns)
        print('created file', filename)
        return filename
    #     filename = create_file_csv(filename, table_columns) # for test
    return filename + '.' + extension


# write html to file
def write_html_file(path, text):
    with open(path, 'w') as fout:
        fout.write(text.encode('utf-8'))


# write row to existed file
# by default write mode is a [append]


def write_row(filename, row, mode='a', delimiter=','):
    with open(filename, mode) as fout:
        fout.write(delimiter.join(str(s) for s in row))
        fout.write('\n')


# write ticker data to path
# by default write into folder where script (root)


def write_ticker_data(ticker_data, path=''):
    # print ticker_data
    for row in ticker_data:
        filename = cleanup_path(row[0])
        data = row[1:]
        filepath = create_or_update_file(os.path.join(path, filename))
        write_row(cleanup_path(filepath), data)


# Main method for write ticker
def write_ticker(name, values):
    foldername = create_folder(name)
    write_ticker_data(values, foldername)

