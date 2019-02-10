from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists, and_
import sqlalchemy.ext.declarative
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy import func
import json
import time



base = sqlalchemy.ext.declarative.declarative_base()

def create_session():
    engine = create_engine('sqlite+pysqlite:///ir.db')
    db_session = sessionmaker(bind = engine)
    return db_session()

class question(base):
    __tablename__ = 'question'
    qid = Column(String, primary_key = True)
    questionname = Column(String)

class wordcount(base):
    __tablename__ = 'wordcount'
    word = Column(String, primary_key = True)
    times = Column(Integer)

class topfive(base):
    __tablename__ = 'topfive'
    word = Column(String, primary_key = True)
    times = Column(Integer)

def writequestion(ques, words):
    dbsession = create_session()
    question = question(qid = 'QS'+str(int(time.time()*100000)), questionname = ques)
    dbsession.add(question)
    for word in words:
        query = dbsession.query(wordcount).filter(wordcount.word == word)
        if query.first():
            query.first().times = query.first().times + 1
        else:
            newword = wordcount(word = word, times = 1)
            dbsession.add(newword)
    dbsession.commit()
    for word in words:
        addtotop(word)
    return "success"

def addtotop(word):
    dbsession = create_session()
    if (howmany < 5): 
        newin = topfive(word, dbsession.query(wordcount).filter(wordcount.word == word).first().times)
        dbsession.add(newin)
    if howmany >= 5: 
        query = dbsession.query(topfive)
        minword = query.first().word
        mintimes = query.first().times
        for eachone in query:
            if eachone.times >= mintimes:
                minword = eachone.word
                mintimes = eachone.times
        tempreplace = dbsession.query(topfive).filter(topfive.word == minword).first()
        wordtime = dbsession.query(wordcount).filter(wordcount.word == word).first().times
        if wordtime >= tempreplace.times:
            tempreplace.times = wordtime
            tempreplace.word = word
    dbsession.commit()
    return "success"

def topfive():
    dbsession = create_session()
    return dbsession.query(wordcount)