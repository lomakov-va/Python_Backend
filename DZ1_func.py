import datetime
import sqlalchemy
print(sqlalchemy.__version__)
from sqlalchemy import Table, Column, BigInteger, Integer, String, MetaData, Sequence, ForeignKey, DateTime, Boolean, create_engine, select, update,delete,Join
from sqlalchemy.orm import declarative_base, Session, sessionmaker, relationship,Load

Base = declarative_base()
engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/db_course", echo=True)

from DZ1_model import *

import bcrypt
#passssss = "123" #userInput--это коммент
#hashAndSalt = bcrypt.hashpw(passssss.encode(), bcrypt.gensalt())


def ins_clnt(nam, phon, mal, log, pa):
    session = Session(engine, expire_on_commit=True)
    with session:
        session.add(Clients(name=nam, phone=phon, mail=mal,  login=log,  password=bcrypt.hashpw(pa.encode(), bcrypt.gensalt())))
        session.commit()
    return print(f'1.Вставка клиента. Успех')

ins_clnt('Петров Иван Петрович', '9090909001', 'PшP@ya.ru', 'PшP', '117')

def ins_account(acc_nam, clnt):
    session = Session(engine, expire_on_commit=True)
    with session:
        session.add(Accounts(acc_name = acc_nam,  clnt_clnt_id = clnt))
        session.commit()
    return print(f'2.Вставка ЛС. Успех')

ins_account('4327-бис',1)

session = Session(engine, expire_on_commit=True)
with session:

    print('вставка справочников ТП и Услуг')
    Ph1 = Serv_list(name_r='МВНО')
    Ph2 = Serv_list(name_r='ШПД')
    SMS = Serv_list(name_r='ИПТВ')

    session.add_all([Ph1, Ph2, SMS])
    session.flush()

    MWNO1 = Rate_plans(rtpl_name = 'MWNO1',rtpl_text = 'МВНО базовый', cost = 100,srls_srls_id=1)
    MWNO2 = Rate_plans(rtpl_name = 'MWNO2',rtpl_text = 'МВНО для развлечений', cost = 200,srls_srls_id=1)
    SHPD1 = Rate_plans(rtpl_name = 'SHPD1',rtpl_text = 'Модем', cost = 60,srls_srls_id=2)
    SHPD2 = Rate_plans(rtpl_name = 'SHPD2',rtpl_text = 'Проводной интернет', cost = 150,srls_srls_id=2)
    Soush = Rate_plans(rtpl_name = 'IPTV',rtpl_text ='Телевидение',srls_srls_id=3)
    session.add_all([Ph1, Ph2, SMS, MWNO1, MWNO2, SHPD1, SHPD2, Soush])

    session.add_all([MWNO1,MWNO2,SHPD1,SHPD2,Soush]) #Fun,Inf,ADSL,FTTx,
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

ins_serv_acc(2,4,100000000001,'Moscov')

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

ins_rtpl_acc(2,3,100000000001,3)

def serv_block(srls, rtpl, acc):
    session = Session(engine, expire_on_commit=True)
    with session:
        query = update(Serv_histories).where(Serv_histories.acc_acc_num == acc,
                                                 Serv_histories.srls_srls_id == srls).values(serv_status=False)
        session.execute(query)
        session.commit()
    return print('5.Блокировка услуги')

serv_block(2,3,100000000001)

def active_ls(acc):
    session_factory= sessionmaker(engine,expire_on_commit=False)
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

active_ls(100000000006) #в моей базе на ЛС 100000000006 2 абонента. Один заблокирован, второй вернулся в результате

print('КОНЕЦ Функций')