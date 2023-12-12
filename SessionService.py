import requests
from config import TOKEN
class SessionService():
    _instances = {}
    
    def __new__(cls, user_id):
        if user_id not in cls._instances:
            cls._instances[user_id] = super(SessionService, cls).__new__(cls)
            cls._instances[user_id].user_id = user_id
            cls._instances[user_id].website = ""
            cls._instances[user_id].balance = ""
            cls._instances[user_id].total_balance = ""
            cls._instances[user_id].event = "No events"
            cls._instances[user_id].nav_point = "profil"
            cls._instances[user_id].sending_file = False
        return cls._instances[user_id]
    
    def set_balance(self, balance):
        
        self.balance += balance
        
        self.total_balance += balance
        message = f"Your balance will be updated on {balance} credits. Your current balance is {self.balance}"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={self.user_id}&text={message}"
        requests.get(url)
        
        
class EventSessions:
    _instances = {}
    _last_event_id = 0  # Keep track of the last assigned event ID

    def __new__(cls, user_id):
        cls._last_event_id += 1  # Increment the event ID
        event_id = cls._last_event_id

        if event_id not in cls._instances:
            cls._instances[event_id] = super(EventSessions, cls).__new__(cls)
            cls._instances[event_id].event_id = event_id
            cls._instances[event_id].user_id = user_id
            cls._instances[event_id].admin_event = ""
            cls._instances[event_id].event_status = "Deactivated"
            cls._instances[event_id].file_id = ""

        return cls._instances[event_id]

     