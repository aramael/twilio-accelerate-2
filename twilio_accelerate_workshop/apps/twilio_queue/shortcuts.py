import urllib


def redirect_url(to, **kwargs):

    if kwargs is not None:
        query_args = '?' + urllib.urlencode(kwargs)
    else:
        query_args = ''

    return to + query_args