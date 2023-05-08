# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

print_hi('cot')
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


import sqlalchemy
from sqlalchemy import create_engine
print(sqlalchemy.__version__)
engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/db_course")


import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# Устанавливаем соединение с postgres
connection = psycopg2.connect(user="postgres", password="1111")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


from sqlalchemy import Table, Column, bigInteger, Integer, String, MetaData, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base(

)
metadata = MetaData()
users_table = Table('Test_TABLE', metadata,
Column('id', Integer, primary_key=True),
Column('name', String(50)),
Column('fullname', String(50)),
Column('password', String(50))
 )
metadata.create_all(engine)

class Test_TABLE(object):
    def __init__(self, name, fullname, password):
                 self.name = name
                 self.fullname = fullname
                 self.password = password

    def __repr__(self):
        return "<Test_TABLE('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

#from sqlalchemy.orm import mapper  #достать "Отобразитель" из пакета с объектно-реляционной моделью
#print (mapper(Test_TABLE, users_table))  # и отобразить. Передает класс User и нашу таблицу
#user = Test_TABLE("Вася", "Василий", "qweasdzxc")
#print (Test_TABLE)  #Напечатает <User('Вася', 'Василий', 'qweasdzxc'>
#print (Test_TABLE.id)  #Напечатает None