#!/usr/bin/env python
#coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapper, sessionmaker
# 创建实例，并连接test库
engine = create_engine("mysql+mysqldb://mysql:123456@113.200.60.105/monitor",
                                    encoding='utf-8', echo=True)
Base = declarative_base()

class Mem(Base):
    __tablename__ = 'mem'
    id = Column(Integer, primary_key=True)
    totle = Column(String(32))
    used = Column(String(32))
    ip = Column(String(32))

class Cpu(Base):
    __tablename__ = 'cpu'
    id = Column(Integer, primary_key=True)
    idle = Column(String(32))
    iowait = Column(String(32))
    ip = Column(String(32))


Base.metadata.create_all(engine)

Session_class = sessionmaker(bind=engine)
Session = Session_class()
data_mem = Mem(totle="fgf",used="123456")
data_cpu = Cpu(idle="",iowait="")
Session.add(data_mem)
Session.commit()
