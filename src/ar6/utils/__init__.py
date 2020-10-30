import os
import urllib.request
import errno


def check_and_download(filepath, url):
    """Checks prescence of a file and downloads if not present.

    Inputs
    ------
        filepath : str
            filename to download to
        url :
            url to download from
    """
    if not os.path.isfile(filepath):
        urllib.request.urlretrieve(url, filepath)
    return


def mkdir_p(path):
    """Checks to see if directory exists, and if not, creates it.

    Inputs
    ------
        path : str
            directory to create

    Raises
    ------
        OSError:
            if directory cannot be created
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
