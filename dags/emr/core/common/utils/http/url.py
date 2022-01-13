from urllib.parse import urlparse


def slash_join(*args):
    """
    Joins a set of strings with a slash (/) between them. Useful for creating URLs.
    If the strings already have a trailing or leading slash, it is ignored.
    Note that the python's urllib.parse.urljoin() does not offer this functionality.
    :param args: string args to join with slash
    :return string: joined string
    """
    stripped_strings = []
    # strip any leading or trailing slashes
    for a in args:
        if isinstance(a, str):
            if a[0] == '/':
                start = 1
            else:
                start = 0
            if a[-1] == '/':
                stripped_strings.append(a[start:-1])
            else:
                stripped_strings.append(a[start:])
    return '/'.join(stripped_strings)


def url_parse(url):
    if isinstance(url, str):
        return urlparse(url=url)
    else:
        return None
