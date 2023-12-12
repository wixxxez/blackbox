from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import requests
from config import TOKEN
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True)
    current_balance = Column(Integer)
    total_balance = Column(Integer)
    events = relationship('Event', back_populates='user')
    payment_requests = relationship('PaymentRequest', back_populates='user')
class Event(Base):
    __tablename__ = 'events'

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    file_path = Column(String)
    status = Column(String)
    user = relationship('User', back_populates='events')
    
class PaymentRequest(Base):
    __tablename__ = 'payment_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    system = Column(String)
    amount = Column(String)
    rekvizits = Column(String)

    # Define the relationship with the User table
    user = relationship('User', back_populates='payment_requests')


class DatabaseManager:
    def __init__(self, db_url="sqlite:///database_for_bot.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def insert_user(self, telegram_id, ):
        existing_user = self.session.query(User).filter_by(telegram_id=telegram_id).first()

        if existing_user:
            return "Welcome back."
        else:
            # User does not exist, create a new user
            new_user = User(telegram_id=telegram_id, current_balance=0, total_balance=0)
            self.session.add(new_user)

            try:
                self.session.commit()
            except IntegrityError as e:
                # Handle the case where another thread or process inserted the user after the check
                self.session.rollback()
            
            finally:
                return "User created"

    def insert_event(self,  user_id, file_path, status):
        new_event = Event(user_id=user_id, file_path=file_path, status=status)
        self.session.add(new_event)
        self.session.commit()

        # Return the file_id of the newly created event
        return new_event.file_id

    def get_user_by_telegram_id(self, telegram_id):
        return self.session.query(User).filter_by(telegram_id=telegram_id).first()

    def get_user_by_user_id(self, user_id):
        return self.session.query(User).filter_by(user_id=user_id).first()
    
    def update_current_balance(self, user_id, amount):  
        user = self.session.query(User).filter_by(user_id=user_id).first()

        if user:
            user.current_balance += amount
            message =  f"У вас было списано {amount * -1} рублей. Ваш баланс: {user.current_balance}"
             
            if amount > 0 : 
                user.total_balance += amount
                message = f"Вам было зачислено {amount} рублей. Ваш баланс: {user.current_balance}"
            
            
            
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={user.telegram_id}&text={message}"
       
            requests.get(url)    
            self.session.commit()
            
    def update_event_status(self, file_id, status_id):
        
        file = self.session.query(Event).filter_by(file_id=file_id).first()

        file.status = status_id
        
        self.session.commit()  
    
    def it_closed(self, file_id):
        
        file = self.session.query(Event).filter_by(file_id=file_id).first()
        return file.status == "CLOSED"


    def get_file_by_id(self, file_id):
        return self.session.query(Event).filter_by(file_id=file_id).first()

    def close_connection(self):
        self.session.close()
        
    def balanceQuotte(self, user, amount):
        user = self.session.query(User).filter_by(telegram_id=user).first()
        
        return user.current_balance >= amount 
    
    def create_request_for_money(self, telegram_id, system, amount, status = "Open"):
        
        user_id = self.get_user_by_telegram_id(telegram_id).user_id
        new_event = PaymentRequest(user_id=user_id, system=system, amount= amount, rekvizits=status)
        self.session.add(new_event)
        self.session.commit()
        
    def getRequestOpenedRequestForUser(self, telegram_id):
        
        user= self.get_user_by_telegram_id(telegram_id)
        
        if user:
        # Get all payment requests excluding the first one
            payment_requests = user.payment_requests

        # Filter payment requests by status "OPEN"
            filtered_payment_requests = [pr for pr in payment_requests if pr.rekvizits == 'Open']
            
            print(filtered_payment_requests)
            print(len(filtered_payment_requests))
            return len(filtered_payment_requests) == 0
        else:
           return None

    def close_requests(self , telegram_id):
        user= self.get_user_by_telegram_id(telegram_id)
        # Get all open payment requests for the user
        open_payment_requests = [pr for pr in user.payment_requests if pr.rekvizits == 'Open']

        # Update the status to "CLOSED" for each open payment request
        for pr in open_payment_requests:
            pr.rekvizits = 'Closed'

        # Commit the changes
        self.session.commit()