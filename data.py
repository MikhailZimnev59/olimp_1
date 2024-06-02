''' Module for getting and saving data '''
from datetime import datetime as dt
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import declarative_base
import pswrd

str_eng = "postgresql+psycopg2://postgres:"+pswrd.PSWRD+"@localhost:5433/olimp"
engine = create_engine(str_eng)
session = Session(bind=engine)

Base = declarative_base()
class T_Debug(Base):
    # create table t_debug(id SERIAL PRIMARY KEY, stroka text)
    __tablename__ = 't_debug'
    id = Column(Integer, primary_key=True, index=True)
    stroka = Column(String(100), nullable=False)
class T_Projname(Base):
    __tablename__ = 't_projname'
    id = Column(Integer, primary_key=True, index=True)
    projname = Column(String(100), nullable=False)

class T_Candidate(Base):
    __tablename__ = 't_candidate'
    id = Column(Integer, primary_key=True, index=True)
    txt_cand = Column(String(100), nullable=False)

class T_Ebz(Base):
    __tablename__ = 't_ebz'
    id = Column(Integer, primary_key=True)
    son = Column(String(100), nullable=False)
    father = Column(String(100), nullable = False)

DEBUG = 'TXT'
EBZ = 'SQL'
PROJ = 'TXT'
CANDIDATE = 'SQL'
PROJNAME = 'SQL'
def get_ebz():
    if EBZ == 'TXT':
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
    elif EBZ == 'SQL':
        result = session.query(T_Ebz)
        dct = {}
        for i in result:
            dct[i.son] = i.father
    return dct
def post_ebz(dct):
    if EBZ == 'TXT':
        with open('ebz.txt', 'w', encoding = 'utf-8') as f:
            f.write(str(dct))
    elif EBZ == 'SQL':
        session = Session(bind=engine)
        new_son, new_father = list(dct.items())[-1]
        new_id = len(list(dct.items())) + 1
        new_pair = T_Ebz(id = new_id, son = new_son, father = new_father)
        session.add(new_pair)
        session.commit()

def get_proj():
    if PROJ == 'TXT':
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
    elif PROJ == 'SQL':
        pass
    return dct_proj

def post_proj(dct_proj):
    if PROJ == 'TXT':
        with open('proj.txt', 'w', encoding = 'utf-8') as f:
            f.write(str(dct_proj))
    elif PROJ == 'SQL':
        pass

def get_candidate():
    if CANDIDATE == 'TXT':
        try:
            with open('candidate.txt', encoding='utf-8') as f:
                txt_cand = f.read()
        except:
            txt_cand = "python mysql"
            with open('candidate.txt', 'w', encoding='utf-8') as f:
                f.write(txt_cand)
    elif CANDIDATE == 'SQL':
        result = session.query(T_Candidate).one()
        txt_cand = result.txt_cand
    return txt_cand

def post_candidate(txt_cand):
    if CANDIDATE == 'TXT':
        with open('candidate.txt', 'w', encoding = 'utf-8') as f:
            f.write(txt_cand)
    elif CANDIDATE == 'SQL':
        session = Session(bind=engine)
        i = session.query(T_Candidate).get(1)
        i.txt_cand = txt_cand
        session.add(i)
        session.commit()

def get_projname():
    if PROJNAME == 'TXT':
        try:
            with open('projname.txt', encoding='utf-8') as f:
                dctext = f.read()
                dct_projname = eval(dctext)
        except:
            dct_projname = {'proj_name': "Проект1"}
            with open('projname.txt', 'w', encoding='utf-8') as f:
                f.write(str(dct_projname))
    elif PROJNAME == 'SQL':
        result = session.query(T_Projname).one()
        dct_projname = eval(result.projname)
    return dct_projname

def post_projname(dct_projname):
    if PROJNAME == 'TXT':
        with open('projname.txt', 'w', encoding = 'utf-8') as f:
            f.write(str(dct_projname))
    elif PROJNAME == 'SQL':
        session = Session(bind=engine)
        i = session.query(T_Projname).get(1)
        i.projname = str(dct_projname)
        session.add(i)
        session.commit()

def post_debug(from_string='_', what_string='_'):
    if DEBUG == 'TXT':
        with open('debug.txt', 'a', encoding ='utf-8') as f:
            f.write('\n'+'_'.join([str(dt.now()), from_string, what_string]))
    elif DEBUG == 'SQL':
        #create table t_debug(id SERIAL PRIMARY KEY, stroka text)
        session = Session(bind=engine)
        new_stroka = T_Debug(stroka = '_'.join([str(dt.now()), from_string, what_string]))
        session.add(new_stroka)
        session.commit()