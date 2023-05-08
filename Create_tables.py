import datetime
import sqlalchemy
print(sqlalchemy.__version__)
from sqlalchemy import Table, Column, BigInteger, Integer, String, MetaData, Sequence, ForeignKey, DateTime, Boolean, create_engine, select, update,delete,Join
from sqlalchemy.orm import declarative_base, Session, sessionmaker, relationship,Load

Base = declarative_base()
# class Base(declarative_base): pass
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

#Serv_list.__table__.create(engine, checkfirst=True)

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

#Rate_plans.__table__.create(engine, checkfirst=True)

#class Tarif_histories(Base):
#    __tablename__ = 'tarif_histories'
#
#    th_id = Column(BigInteger, primary_key=True, autoincrement=True)
#    srls_srls_id = Column(ForeignKey('serv_list.srls_id'))
#    service = relationship(Serv_list)
#    rtpl_rtpl_id = Column(ForeignKey('rate_plans.rtpl_id'))
#    rateplan = relationship(Rate_plans)
#    start_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
#    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

#Tarif_histories.__table__.create(engine, checkfirst=True)


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
# хэширование паролей
import bcrypt
#passssss = "123" #userInput--это коммент
#hashAndSalt = bcrypt.hashpw(passssss.encode(), bcrypt.gensalt())

#session = Session(engine, expire_on_commit=True)
#with session:
#    print('вставка')
#    ivanov = Clients(name='Иванов Иван Иванович', phone='2128506', mail='III@ya.ru',  login='III',  password='123')
#    ivhash = Clients(name='Иванов Кто Иванович', phone='2128501', mail='IЗI@ya.ru',  login='IЗI',  password=bcrypt.hashpw("112".encode(), bcrypt.gensalt()))
#    session.add(ivhash)
#    session.flush()

#    dogovor= Accounts(acc_name = '2134-моль',  clnt_clnt_id = ivhash.clnt_id)
#    dogovor = Accounts(acc_name='2134-моль', clnt_clnt_id=18)
#    session.add_all([dogovor])
#    session.commit()

def ins_clnt(nam, phon, mal, log, pa):
    session = Session(engine, expire_on_commit=True)
    with session:
        session.add(Clients(name=nam, phone=phon, mail=mal,  login=log,  password=bcrypt.hashpw(pa.encode(), bcrypt.gensalt())))
        session.commit()
    return print(f'1.Вставка клиента. Успех')

#ins_clnt('Петров Петор Петрович', '9090909000', 'PPP@ya.ru', 'PPP', '111')

def ins_account(acc_nam, clnt):
    session = Session(engine, expire_on_commit=True)
    with session:
        session.add(Accounts(acc_name = acc_nam,  clnt_clnt_id = clnt))
        session.commit()
    return print(f'2.Вставка ЛС. Успех')

#ins_account('4322-бис',18)

session = Session(engine, expire_on_commit=True)
with session:
    print('вставка справочников ТП и Услуг')
    Ph1 = Serv_list(name_r='МВНО')
    Ph2 = Serv_list(name_r='ШПД')
    SMS = Serv_list(name_r='ИПТВ')
#    Fun = Serv_list(name_r='Умный дом')
#    Inf = Serv_list(name_r='ЦТВ')
#    ADSL = Serv_list(name_r='Лицей')
#    FTTx = Serv_list(name_r='Доступ по технологии FTTx')

#    session.add_all([Ph1, Ph2, SMS])
#    session.flush()

    MWNO1 = Rate_plans(rtpl_name = 'MWNO1',rtpl_text = 'МВНО базовый', cost = 100,srls_srls_id=1)
    MWNO2 = Rate_plans(rtpl_name = 'MWNO2',rtpl_text = 'МВНО для развлечений', cost = 200,srls_srls_id=1)
    SHPD1 = Rate_plans(rtpl_name = 'SHPD1',rtpl_text = 'Модем', cost = 60,srls_srls_id=2)
    SHPD2 = Rate_plans(rtpl_name = 'SHPD2',rtpl_text = 'Проводной интернет', cost = 150,srls_srls_id=2)
    Soush = Rate_plans(rtpl_name = 'IPTV',rtpl_text ='Телевидение',srls_srls_id=3)
    session.add_all([Ph1, Ph2, SMS, MWNO1, MWNO2, SHPD1, SHPD2, Soush])

#    session.add_all([MWNO1,MWNO2,SHPD1,SHPD2,Soush]) #Fun,Inf,ADSL,FTTx,

#    session.flush()
#    print('вставка связей')
#    q = Tarif_histories(srls_srls_id=Ph1.srls_id ,rtpl_rtpl_id=MWNO1.rtpl_id)
#    w = Tarif_histories(srls_srls_id=Ph1.srls_id ,rtpl_rtpl_id=MWNO2.rtpl_id)
#    e = Tarif_histories(srls_srls_id=Ph2.srls_id ,rtpl_rtpl_id=MWNO1.rtpl_id)
#    r = Tarif_histories(srls_srls_id=Ph2.srls_id ,rtpl_rtpl_id=MWNO2.rtpl_id)
#    t = Tarif_histories(srls_srls_id=SMS.srls_id ,rtpl_rtpl_id=MWNO1.rtpl_id)
#    y = Tarif_histories(srls_srls_id=SMS.srls_id ,rtpl_rtpl_id=MWNO2.rtpl_id)
#    u = Tarif_histories(srls_srls_id=Fun.srls_id ,rtpl_rtpl_id=MWNO2.rtpl_id)
#    i = Tarif_histories(srls_srls_id=Inf.srls_id ,rtpl_rtpl_id=MWNO1.rtpl_id)
#    o = Tarif_histories(srls_srls_id=Inf.srls_id ,rtpl_rtpl_id=MWNO2.rtpl_id)
#    p = Tarif_histories(srls_srls_id=Inf.srls_id ,rtpl_rtpl_id=SHPD1.rtpl_id)
#    a = Tarif_histories(srls_srls_id=Inf.srls_id ,rtpl_rtpl_id=SHPD2.rtpl_id)
#    s = Tarif_histories(srls_srls_id=Inf.srls_id ,rtpl_rtpl_id=Soush.rtpl_id)
#    d = Tarif_histories(srls_srls_id=ADSL.srls_id ,rtpl_rtpl_id=SHPD1.rtpl_id)
#    f = Tarif_histories(srls_srls_id=FTTx.srls_id ,rtpl_rtpl_id=SHPD2.rtpl_id)
#    g = Tarif_histories(srls_srls_id=ADSL.srls_id ,rtpl_rtpl_id=Soush.rtpl_id)

#    session.add_all([q, w, e, r, t, y, u, i, o, p, a, s, d, f, g])
    session.commit()
#    session.rollback()

def ins_serv_acc(srls, rtpl, acc, adr):
    session = Session(engine, expire_on_commit=True)
    with session:
        query = select(Rate_plans).where(Rate_plans.srls_srls_id == srls, Rate_plans.rtpl_id==rtpl)
        query_result = session.execute(query)
        for rate_plans in query_result.scalars().all():
            session.add(Serv_histories(srls_srls_id = srls,  adress = adr, acc_acc_num = acc, rtpl_rtpl_id =rtpl))
        session.commit()
    return print('3.Вставка связей услуг и ТП с абонентом')

#ins_serv_acc(3,5,100000000006,'Moscov')

def ins_rtpl_acc(srls, rtpl, acc, rtpl_new):
    session = Session(engine, expire_on_commit=True)
    with session:
        query = select(Rate_plans).options(
            Load(Rate_plans).load_only(Rate_plans.srls_srls_id, Rate_plans.rtpl_id)).where(Rate_plans.srls_srls_id == srls,Rate_plans.rtpl_id==rtpl)
        query_result = session.execute(query)
        for rate_plans in query_result.scalars().all():
            query = update(Serv_histories).where(Serv_histories.acc_acc_num == acc,
                                                 Serv_histories.srls_srls_id == srls).values(rtpl_rtpl_id=rtpl_new)
            session.execute(query)
        session.commit()
    return print('4.Изменение тарифа ')

#ins_rtpl_acc(2,3,100000000002,4)

def serv_block(srls, rtpl, acc):
    session = Session(engine, expire_on_commit=True)
    with session:
        query = update(Serv_histories).where(Serv_histories.acc_acc_num == acc,
                                                 Serv_histories.srls_srls_id == srls).values(serv_status=False)
        session.execute(query)
        session.commit()
    return print('5.Блокировка услуги')

#serv_block(1,1,100000000001)

def active_ls(acc):
    session_factory= sessionmaker(engine,expire_on_commit=True)
    with session_factory() as session:
        query=select(
            Serv_histories.acc_acc_num.label('LS'),
            Serv_list.name_r,
            Rate_plans.rtpl_name,
        ).join(Serv_list, Serv_list.srls_id==Serv_histories.srls_srls_id,
        ).join(Rate_plans, Rate_plans.rtpl_id==Serv_histories.rtpl_rtpl_id,
        ).where(Serv_histories.acc_acc_num==acc,Serv_histories.serv_status==True)#.srls_srls_id==1)#
        query_result = session.execute(query)
        accounts=query_result.all()
        for account in accounts:
            print(f'a={account.LS},s={account.name_r},r={account.rtpl_name}')

print('6.Написать функцию, которая по ID пользователя возвращает список всех активных ЛС, включая подключенные услуги и тарифы.')
active_ls(100000000006)

print('КОНЕЦ')

session = Session(engine, expire_on_commit=False)
with session:
    query = update(Serv_histories).where(Serv_histories.acc_acc_num == 100000000001,
                                         Serv_histories.srls_srls_id == 1).values(rtpl_rtpl_id=2)
    session.execute(query)
    session.commit()


    print('poisk')
    query = select(Serv_histories).where(Serv_histories.srls_srls_id ==8)
    query_result = session.execute(query)

    for tarif_histories in query_result.scalars().all():
        print(tarif_histories.srls_srls_id, tarif_histories.rtpl_rtpl_id)
        print(tarif_histories.rtpl_rtpl_id+1)
        if tarif_histories.rtpl_rtpl_id>1:
            print('not empty')
        else:   print(' empty')

    print('poisk2')
    query = select(Rate_plans).options(Load(Rate_plans).load_only(Rate_plans.srls_srls_id,Rate_plans.rtpl_id)).where(Rate_plans.srls_srls_id ==1)
    query_result = session.execute(query)
    for rate_plans in query_result.scalars().all():
        print(f'sr={rate_plans.srls_srls_id},rt={rate_plans.rtpl_id}')



session_factory= sessionmaker(engine,expire_on_commit=True)
with session_factory() as session:
    query=select(
        Serv_histories.acc_acc_num.label('LS'),
        Serv_list.name_r,
        Rate_plans.rtpl_name,
    ).join(Serv_list, Serv_list.srls_id==Serv_histories.srls_srls_id,
    ).join(Rate_plans, Rate_plans.rtpl_id==Serv_histories.rtpl_rtpl_id,
    ).where(Serv_histories.serv_status==True)#.srls_srls_id==1)#Serv_histories.acc_acc_num==100000000002,
    query_result = session.execute(query)
    accounts=query_result.all()
    for account in accounts:
        print(f'a={account.LS},s={account.name_r},r={account.rtpl_name}')
