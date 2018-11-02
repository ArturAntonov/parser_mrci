import os


# make path from url
def transform_to_path(url):
    return os.path.normpath(url.strip('/'))


# join url pieces
def url_join(pieces):
    return '/'.join(s.strip('/') for s in pieces)


def cleanup_path(path):
    return path.replace('\r\n', '').replace('\n', '')
