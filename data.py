''' Module for getting and saving data '''
from datetime import datetime as dt
def get_ebz():
    try:
        with open('ebz.txt', encoding = 'utf-8') as f:
            dctext = f.read()
            dct = eval(dctext)
    except:
        dct = {"python": "programming languages",
               "programming languages": "it",
               "it": "_root",
               "php": "programming languages",
               "postgresql": "rdbms",
               "rdbms": "databases",
               "databases": "it",
               "engineering": "_root"}
        with open('ebz.txt', 'w', encoding = 'utf-8') as f:
            f.write(str(dct))
    return dct
def post_ebz(dct):
    with open('ebz.txt', 'w', encoding = 'utf-8') as f:
        f.write(str(dct))

def get_proj():
    try:
        with open('proj.txt', encoding='utf-8') as f:
            dctext = f.read()
            dct_proj = eval(dctext)

    except:
        dct_proj = {"Проект 1": "python english postgresql",
                    "Проект 2": "php mysql german",
                    }
        with open('proj.txt', 'w', encoding='utf-8') as f:
            f.write(str(dct_proj))
    return dct_proj

def post_proj(dct_proj):
    with open('proj.txt', 'w', encoding = 'utf-8') as f:
        f.write(str(dct_proj))

def get_candidate():
    try:
        with open('candidate.txt', encoding='utf-8') as f:
            txt_cand = f.read()
    except:
        txt_cand = "python mysql"
        with open('candidate.txt', 'w', encoding='utf-8') as f:
            f.write(txt_cand)
    return txt_cand

def post_candidate(txt_cand):
    with open('candidate.txt', 'w', encoding = 'utf-8') as f:
        f.write(txt_cand)

def get_projname():
    try:
        with open('projname.txt', encoding='utf-8') as f:
            dctext = f.read()
            dct_projname = eval(dctext)
    except:
        dct_projname = {'proj_name': "Проект1"}
        with open('projname.txt', 'w', encoding='utf-8') as f:
            f.write(str(dct_projname))
    return dct_projname

def post_projname(dct_projname):
    with open('projname.txt', 'w', encoding = 'utf-8') as f:
        f.write(str(dct_projname))

def post_debug(from_string='_', what_string='_'):
    with open('debug.txt', 'a', encoding ='utf-8') as f:
        f.write('\n'+'_'.join([str(dt.now()), from_string, what_string]))
