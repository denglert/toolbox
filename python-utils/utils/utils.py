from collections import defaultdict
import os, errno

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))

def print_nested_dict(d):
  for k, v in d.items():
    if isinstance(v, dict):
      print_nested_dict(v)
    else:
      print("{0} : {1}".format(k, v))

def print_nested_dict_keys(d):
  for k, v in d.items():
    if isinstance(v, dict):
      print("{0}".format(k))
      print_nested_dict_keys(v)
    else:
      print("{0}".format(k))

def nested_dict_walker(d):

    for k, v in d.items():
        if isinstance(v, dict):
            print("{0}".format(k))
            print_nested_dict_walker(v)

        else:
            print("{0}".format(k))


def silentrm(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
