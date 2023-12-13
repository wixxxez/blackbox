from config import RECEPIENT_ID
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.enums import ParseMode
from SessionService import EventSessions
class AdminsMessage():

    def __init__(self, bot) -> None:
        
        self.bot = bot
    
    
    async def send_message(self, numrows, file_id, file_path, website, recepient_id, username):

        builder = InlineKeyboardBuilder()
     
        builder.button(text= "Оповестить ⌛️", callback_data= f'{recepient_id}NOTIFY')
        laba_name = FSInputFile(f"{file_path}")
         
        for admin in RECEPIENT_ID:
            await self.bot.send_document(admin,laba_name, caption = f"Username: {username} \nСовпадений: {numrows}\nЗапрос: {website} \nFile_id: {file_id}", reply_markup = builder.as_markup(),  parse_mode = ParseMode.HTML)    
        
        return -1 
        
    async def request_for_money(self, dict, user_id):
        
        builder = InlineKeyboardBuilder()
        
        builder.button(text="Оплачено", callback_data=f"{user_id}finish_payment")
        builder.button(text="Отменить заявку", callback_data=f"{user_id}cancel_payment")
        payment_system = dict["Система выплаты"]
        amount = dict['Сумма']
        rec = dict['Реквизиты']
        for admin in RECEPIENT_ID:
            
            await self.bot.send_message(chat_id = admin,text= f'Система выплаты: {payment_system},\nСумма: {amount},\nРеквизиты:{rec}', reply_markup = builder.as_markup(), parse_mode = ParseMode.HTML )
        
        
        