from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker,relationship, declarative_base
from psycopg2 import OperationalError
import sys




try:
    #utworzenie silnika
    engine=create_engine("postgresql://postgres:postgres@localhost:5432/audyty_", echo=False)
    # Utworzenie sesji do interakcji z bazą danych
    Session = sessionmaker(bind=engine)
    session = Session()
except OperationalError as e:   #Jezeli nie polaczymy sie z baza danych
    print(f"Błąd połączenia z bazą danych: {e}")
    exit()



# Deklaracja bazy modeli
Base= declarative_base()

#tabela auditors
class Auditor(Base):
    __tablename__='auditors'
    id = Column(Integer, primary_key=True)
    name=Column(String(50))
    lastname=Column(String(50))
    audits = relationship('Audit', back_populates='auditor')
   
#tabela audits
class Audit(Base):
    __tablename__='audits'
    id = Column(Integer, primary_key=True)
    type=Column(String(50))
    status=Column(String(50))
    auditor_id= Column(Integer, ForeignKey('auditors.id'))
    auditor = relationship('Auditor', back_populates='audits')

Base.metadata.create_all(engine)


def check_auditor_exists(auditor_id):
    existing_auditor = session.query(Auditor).filter_by(id=auditor_id).first()  
    return existing_auditor is not None


def check_audit_exists(audit_id):
    existing_audit = session.query(Audit).filter_by(id=audit_id).first()
    return existing_audit is not None


def finish():
    print("Finished.")
    session.close()
    sys.exit()


def insert():
    print("Complete: ")
    _type = input("Type of audit>>")
    _status=input("State of audit (o - open, c - closed)")
    _auditor_id = input("Auditor ID >>")
    if check_auditor_exists(_auditor_id):
        if type != "" and _auditor_id != "" and (_status == "o" or _status =="c"):
            audit=Audit(type=_type, status=_status,auditor_id=_auditor_id)
            session.add(audit)
            session.commit()
            print("Audit has been added")
        else:
            print("Wrong data")
    else:
        print(f"Auditor with ID {_auditor_id} does not exist.")


def show_audits():
    print("Table audits content:")
    print("Id | Type | Status | Auditor_id ")
    _audit=session.query(Audit)
    for i in _audit:
        print(i.id, i.type, i.status, i.auditor_id)

def show_auditors():
    print("Table audits content:")
    print("Id | Name | Lastname")
    _auditor=session.query(Auditor)
    for i in _auditor:
        print(i.id, i.name, i.lastname)


def edit_audit():
    _id= int(input("Choose audit's id to edit>>"))
    
    if check_audit_exists(_id):
        _audit=session.query(Audit).filter(Audit.id==_id).first()
        print("Record to edit:")
        print(f"ID: {_audit.id}, Type: {_audit.type}, Status: {_audit.status}, Auditor ID: {_audit.auditor_id}")
        confirm=input("Do you want to edit this record? Yes - type 'y'.")
        if confirm.lower()=="y":
            _type = input("New type of audit>>")
            _status = input("New status of audit (o - open, c - closed)>>")
            _auditor_id = input("New id of auditor>>")

            _audit.type = _type if _type else _audit.type
            if _status == "o" or _status =="c":
                 _audit.status = _status if _status else _audit.status
            else:
                print("Status should be 'o' or 'c'")
            if check_auditor_exists(_auditor_id): 
                _audit.auditor_id = _auditor_id if _auditor_id else _audit.auditor_id
            else:
                print(f"Auditor with ID {_auditor_id} does not exist.")
            print("Audit has been edited.")
    else:
        print("No audit with the given Id ")


def delete_audit():
    _id= int(input("Choose audit's id to delete>>"))
    if check_audit_exists(_id):
        _audit=session.query(Audit).filter(Audit.id==_id).first()
        print("Record to delete:")
        print(f"ID: {_audit.id}, Type: {_audit.type}, Status: {_audit.status}, Auditor ID: {_audit.auditor_id}")
        confirm=input("Do you want to delete this record? Yes - type 'y'.")
        if confirm.lower()=="y":
            session.delete(_audit)
            session.commit()
            print("Audit has been deleted.")
    else:
        print("No audit with the given Id ")


def inner_join():
    inner_join_results = session.query(Audit, Auditor).join(Auditor).all()
    for audit, auditor in inner_join_results:
        print("Audit:")
        print(f"ID: {audit.id}, Type: {audit.type}, Status: {audit.status}, Auditor ID: {audit.auditor_id}")
        print("Auditor:")
        print(f"ID: {auditor.id}, Name: {auditor.name}, Lastname: {auditor.lastname}")
        print("-" * 30)


def left_join():
    left_join_results = session.query(Audit, Auditor).outerjoin(Auditor).all()
    for audit, auditor in left_join_results:
        print("Audit:")
        print(f"ID: {audit.id}, Type: {audit.type}, Status: {audit.status}, Auditor ID: {audit.auditor_id}")
        if auditor:
            print("Auditor:")
            print(f"ID: {auditor.id}, Name: {auditor.name}, Lastname: {auditor.lastname}")
        else:
            print("No corresponding auditor.")
        print("-" * 30)    


def menu():
    while True:
        print("""Options:
            0. Finish.
            1. Insert audit.
            2. Edit audit
            3. Delete audit
            4. Show audits 
            5. Show auditors 
            6. Inner join
            7. Left join

    """)
        choice=input("Chosen option:")

        if choice == "0":
            finish()
        elif choice == "1":
            insert()
        elif choice =="2":
            edit_audit()
        elif choice =="3":
            delete_audit()
        elif choice =="4":
            show_audits()
        elif choice =="5":
            show_auditors()
        elif choice =="6":
            inner_join()
        elif choice =="7":
            left_join()
        else:
            print("Incorrect. Try again.")



"""
new_auditor = Auditor(name="Hannah", lastname="James")
session.add(new_auditor)
session.commit()

new_auditor = Auditor(name="John", lastname="Smith")
session.add(new_auditor)
session.commit()

new_auditor = Auditor(name="Alex", lastname="Jones")
session.add(new_auditor)
session.commit()

new_auditor = Auditor(name="Tom", lastname="Evans")
session.add(new_auditor)
session.commit()

new_auditor = Auditor(name="Simon", lastname="White")
session.add(new_auditor)
session.commit()

new_auditor = Auditor(name="Julia", lastname="Roberts")
session.add(new_auditor)
session.commit()

new_audit = Audit(type="Management", status="o", auditor_id=1)
session.add(new_audit)
session.commit()

new_audit = Audit(type="Production", status="o", auditor_id=2)
session.add(new_audit)
session.commit()

new_audit = Audit(type="HR", status="o", auditor_id=3)
session.add(new_audit)
session.commit()

new_audit = Audit(type="Logistics", status="o", auditor_id=2)
session.add(new_audit)
session.commit()

new_audit = Audit(type="Quality", status="o", auditor_id=3)
session.add(new_audit)
session.commit()

new_audit = Audit(type="Engineering", status="o", auditor_id=4)
session.add(new_audit)
session.commit()

new_audit = Audit(type="IT systems", status="o", auditor_id=3)
session.add(new_audit)
session.commit()

new_audit = Audit(type="Quality", status="o", auditor_id=1)
session.add(new_audit)
session.commit()

new_audit = Audit(type="Quality", status="o", auditor_id=1)
session.add(new_audit)
session.commit()

"""
menu()
            


