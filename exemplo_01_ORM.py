from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, ForeignKey, inspect, select, func
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    # Criando a tabela:
    __tablename__ = "user_account"

    # Definindo os atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    #Estabelecendo uma relação entre a tabela Address e a tabela User
    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, full name={self.fullname})"

class Address(Base):
    # Criando a tabela:
    __tablename__ = "address"

    # Definindo os atributos
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    #Estabelecendo uma relação entre a tabela Address e a tabela User
    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_address})"


print(User().__tablename__)
print(Address().__tablename__)

#Conexão com o banco de dados do tipo sqlite
engine = create_engine('sqlite:///meu_banco_de_dados.db')
#Criando as classes como tabelas no banco de dados
Base.metadata.create_all(bind=engine)

#O inspetor investiga o banco de dados
inspetor_engine = inspect(engine)

#Retornando o nome das tabelas
print(inspetor_engine.get_table_names())

#Buscando o nome do esquema do banco
print(inspetor_engine.default_schema_name)

#Criando uma sessão para add dados ao banco
with Session(engine) as session:
    user1 = User(
        name = 'Filipe',
        fullname = 'Cardoso',
        address=[Address(email_address='filipe@email.com')]
    )
    user2 = User(
        name = 'Fulano',
        fullname = 'de Tal',
        address=[
            Address(email_address='fulano@email1.com'),
            Address(email_address='fulano@email2.com'),
        ]
    )
    #Isso pode ser feito pois na linha 32 " nullable=False"
    user3 = User(
        name = 'Ciclano',
        fullname = 'de Tal'
    )

    #Add tudo ao banco de dados
    session.add_all([user1, user2, user3])
    session.commit()

#Lendo do banco de dados criando um statement
stmt = select(User).where(User.name.in_(['Fulano', 'Filipe']))
for user in session.scalars(stmt):
    print(user)

#Lendo da tabela Address os e-mails do registro cujo id na tabela User é = 2
stmt_address = select(Address).where(Address.user_id.in_([2]))
for address in session.scalars(stmt_address):
    print(address)

#Recuperando de forma ordenada e decrescente pelo fullname os Users
print("ORDER BY DECRESCENTE")
stmt_order = select(User).order_by(User.fullname.desc())
for resoult in session.scalars(stmt_order):
    print(resoult)
print("ORDER BY ASCENDENTE")
stmt_order = select(User).order_by(User.fullname)
for resoult in session.scalars(stmt_order):
    print(resoult)

#Usando o JOIN (Junção entre as tabelas)
#Ele vai fazer o match pela foreingkey
stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
for resoult in session.scalars(stmt_join):
    print(resoult)

#Segunda forma de ter o mesmo resultado apresentado acima:
connection = engine.connect()
resoults = connection.execute(stmt_join).fetchall()
for resoult in resoults:
    print(resoult)

#Usando a função SQL COUNT:

stmt_count = select(func.count('*')).select_from(User)
for resoult in session.scalars(stmt_count):
    print(resoult)