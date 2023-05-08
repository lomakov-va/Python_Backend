import datetime
import sqlalchemy
print(sqlalchemy.__version__)
from sqlalchemy import Table, Column, BigInteger, Integer, String, MetaData, Sequence, ForeignKey, DateTime, Boolean, create_engine, select, update,delete,Join
from sqlalchemy.orm import declarative_base, Session, sessionmaker, relationship,Load

Base = declarative_base()
engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/db_course", echo=True)

class Clients(Base):
    __tablename__ = 'clients'

    clnt_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50))
    phone = Column(String(10))
    mail = Column(String(50))
    login = Column(String(50))
    password = Column(String(1000))
    start_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

Clients.__table__.create(engine, checkfirst=True)


# ACC_NUM_SEQ = Sequence('acc_num_seq', start=100000000001)
# sqlalchemy.engine..execute(schema.CreateSequence(ACC_NUM_SEQ))

class Accounts(Base):
    __tablename__ = 'accounts'

    acc_num = Column(BigInteger, Sequence("acc_num_seq", start=100000000001), primary_key=True)  # autoincrement=True)#server_default=ACC_NUM_SEQ.next_value())
    acc_name = Column(String(50))
    balance = Column(Integer, default=0)
    clnt_clnt_id = Column(ForeignKey('clients.clnt_id'))
    client = relationship(Clients)
    start_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

Accounts.__table__.create(engine, checkfirst=True)

class Serv_list(Base):
    __tablename__ = 'serv_list'

    srls_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name_r = Column(String(50))
    start_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

Serv_list.__table__.create(engine, checkfirst=True)

class Rate_plans(Base):
    __tablename__ = 'rate_plans'

    rtpl_id = Column(BigInteger, primary_key=True, autoincrement=True)
    rtpl_name = Column(String(50))
    rtpl_text = Column(String(1000))
    cost = Column(Integer, default=0)
    srls_srls_id = Column(ForeignKey('serv_list.srls_id'))
    service = relationship(Serv_list)
    start_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

Rate_plans.__table__.create(engine, checkfirst=True)

class Serv_histories(Base):
    __tablename__ = 'serv_histories'

    sh_id = Column(BigInteger, primary_key=True, autoincrement=True)
    srls_srls_id = Column(ForeignKey('serv_list.srls_id'))
    service = relationship(Serv_list)
    serv_status = Column(Boolean, default=True)
    adress = Column(String(200))
    acc_acc_num = Column(ForeignKey('accounts.acc_num'))
    account = relationship(Accounts)
    rtpl_rtpl_id = Column(ForeignKey('rate_plans.rtpl_id'))
    rateplan = relationship(Rate_plans)
    start_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

Serv_histories.__table__.create(engine, checkfirst=True)

#Base.metadata.drop_all(engine)
#Serv_histories.__table__.drop(engine)
#Tarif_histories.__table__.drop(engine, checkfirst=True)
#Serv_list.__table__.drop(engine, checkfirst=True)
#Accounts.__table__.drop(engine, checkfirst=True)
#Rate_plans.__table__.drop(engine, checkfirst=True)
#Clients.__table__.drop(engine, checkfirst=True)

# Base.metadata.create_all(engine)

print('КОНЕЦ модели')
