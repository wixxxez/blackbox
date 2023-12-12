import SessionService
from DataBaseManager import DatabaseManager
class ValidateCommands():
    
    def valide(self, params):
        
        pass
    
class SetBalance():
    
    def valide(self, params):
        
        if len(params) != 2:
            
            return "Неверно количество параметров"
         
        try:
            file = int(params[0])
            db = DatabaseManager().get_file_by_id(file)
            if db == None:
                return "File id не найден"
        except Exception:
            
            return "Неверный идентификатор файла"
        
        try: 
            balance = int(params[1])
            
        except Exception:
            
            return "Неверный баланс"
        
        return "Valid"

class Payments():
    
    def valid_amount(self, amount): 
        
        try: 
            balance = int(amount)
        
        except Exception as e:
            
            return "Неверная сумма"
        
        return "OK"