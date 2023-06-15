from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey 
from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

#Criando a engine e estipulando que os dados serão salvos em memória
engine = create_engine('sqlite:///meu_banco_de_dados.db')

#Objeto associado aos meta dados do banco de dados
metadata_obj = MetaData()

#Criação de tabela user
user = Table(
    'user',
    metadata_obj,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(40), nullable=False), #nullable=False -> A coluna não pode ser nula
    Column('email_address', String(60)),
    Column('nickname', String(50), nullable=False),

)

#Criação de tabela user_prefs
user_prefs = Table(
    'user_prefs',
    metadata_obj,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('pref_name', String(40), nullable=False), #nullable=False -> A coluna não pode ser nula
    Column('pref_value', String(100)),

)
print("\n\rInfo da tabela user_prefs")
print(user_prefs.primary_key)
print(user_prefs.constraints)
print("\n\rDados das tabelas de metadata_obj")
print(metadata_obj.tables)

#Recuperando os dados
print("\n\rTabelas de metadata_obj")
for table in metadata_obj.sorted_tables:
    print(table)

#Criando as tabelas dentro da engine
metadata_obj.create_all(engine)

#Criando outro schema
metadata_db_obj = MetaData()


#Criando o statement:
print("\n\rExecutando o statement SQL")
sql = text('select * from user')
Session = sessionmaker(bind=engine)
session = Session()

result = session.execute(sql)

for row in result:
    print(row)
#Inserindo info na tabela "user"
sql_insert = text("insert into user values(2, 'fulano', 'email@email.com', 'fu')")
result = session.execute(sql_insert)

#Criação de tabela financial_info
financial_info = Table(
    'financial_info',
    metadata_db_obj,
    Column('id', Integer, primary_key=True),
    Column('value', String(100)),

)

print("\n\rInfo da tabela financial_info")
print(financial_info.primary_key)
print(financial_info.constraints)

#Fechando a conexão:
session.close()