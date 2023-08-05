import requests
from tenacity import (retry,
                      wait_fixed,
                      retry_if_exception_type,
                      stop_after_attempt)

API_URL = 'https://api.semanticscholar.org/v1'


def paper(id, include_unknown_references=False) -> dict:

    '''Paper lookup

    :param id: S2PaperId, DOI or ArXivId.
    :param include_unknown_references : bool,
        (optional) include non referenced paper.
    :returns: paper data or empty :class:`dict` if not found.
    :rtype: :class:`dict`
    '''

    data = __get_data('paper', id, include_unknown_references)

    return data


def author(id) -> dict:

    '''Author lookup

    :param id: S2AuthorId.
    :returns: author data or empty :class:`dict` if not found.
    :rtype: :class:`dict`
    '''

    data = __get_data('author', id)

    return data


@retry(
    wait=wait_fixed(30),
    retry=retry_if_exception_type(ConnectionRefusedError),
    stop=stop_after_attempt(10)
    )
def __get_data(method, id, include_unknown_references=False) -> dict:

    '''Get data from Semantic Scholar API

    :param method: 'paper' or 'author'.
    :param id: :class:`str`.
    :returns: data or empty :class:`dict` if not found.
    :rtype: :class:`dict`
    '''

    data = {}
    method_types = ['paper', 'author']
    if method not in method_types:
        raise ValueError(
            'Invalid method type. Expected one of: {}'.format(method_types))

    url = '{}/{}/{}'.format(API_URL, method, id)
    if include_unknown_references:
        url += '?include_unknown_references=true'
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
        if len(data) == 1 and 'error' in data:
            data = {}
    elif r.status_code == 429:
        raise ConnectionRefusedError('HTTP status 429 Too Many Requests.')

    return data
