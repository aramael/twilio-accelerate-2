import urllib


def redirect_url(to, **kwargs):

    if kwargs is not None:

        cleaned_kwargs = {}

        for key, value in kwargs.iteritems():
            if type(value) is list:
                kwarg = ','.join(value)
            cleaned_kwargs[key] = value

        query_args = '?' + urllib.urlencode(cleaned_kwargs)
    else:
        query_args = ''

    return to + query_args