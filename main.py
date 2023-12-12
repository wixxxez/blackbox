from aiogram import Bot, Dispatcher, Router, types , F
from aiogram.filters import CommandStart , Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder 
import asyncio
import logging
import sys
from aiohttp import ContentTypeError
import ReadFileService, CheckManager
import config
import os
from aiogram import types
from AdminsMessage import AdminsMessage
import SessionService
import AdminEvents
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from DataBaseManager import DatabaseManager
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import requests as req
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

token =  config.TOKEN

dp = Router()

bot = Bot(f"{token}")

WEBHOOK_PATH = f"/bot/{token}"
TUNNEL_URL = "http://38.180.114.16/"
WEBHOOK_URL = f"{TUNNEL_URL}{WEBHOOK_PATH}"
pages = open("pages.txt", 'r')
pages = pages.readlines()
web_pages = []
requests = []
actual_req = ""
for i in pages:
    actual_req += i
    i = i.strip()
    x = KeyboardButton(text= f"{i}")
    requests.append(i)
    web_pages.append(x)
#buttons_label = np.reshape(web_pages,(1,-1)).tolist()
sublists = [web_pages[i:i + 3] for i in range(0, len(web_pages), 3)]

async def on_startup():
    webhook_info = await bot.get_webhook_info()
     

    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )
    
def main() -> None:
    # Dispatcher is a root router
     
    dispatcher = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dispatcher.include_router(dp)

    # Register startup hook to initialize webhook
    dispatcher.startup.register(on_startup)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token, parse_mode=ParseMode.HTML)

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dispatcher, bot=bot)

    # And finally start webserver
    web.run_app(app, host= "127.0.0.1", port=80)

    
 



system_payments = ["🍋Bitcoin", "USDT TRC-20", "🛒Market LZT"]

system_payments_dict = {"🍋Bitcoin": 'Bitcoin', 
                        "USDT TRC-20": "USDT TRC-20",
                        "🛒Market LZT" : "Market LZT"}

@dp.message(Command('start'))
async def start(message: types.Message):
    db = DatabaseManager()
    id= message.from_user.id
    text = db.insert_user(id)
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(KeyboardButton(text ="💼Загрузить логи💼"))
    keyboard.row(KeyboardButton(text= "👑Профиль👑"), KeyboardButton(text= "🧠Инструкция🧠"), KeyboardButton(text= "🔎Актуальные запросы🔎"))
    await message.answer(text= "Нажмите на кнопку ниже 👇, чтобы начать работу", reply_markup= keyboard.as_markup(one_time_keyboard = True, resize_keyboard = True))

@dp.message(F.text == "🧠Инструкция🧠")
async def instruction(message: types.Message):
    await message.answer(text= "🧠Инструкция🧠\n\nhttps://pl.wikipedia.org/wiki/Jan_Pawe%C5%82_II")
    
@dp.message(F.text == "🔎Актуальные запросы🔎")
async def actual_requests(message: types.Message):
    await message.answer(text= f"🔎Актуальные запросы которые мы скупаем:\n\nLogin:Password\n\n```\n{actual_req}```", parse_mode = ParseMode.MARKDOWN)


@dp.message(F.text == "👑Профиль👑")
async def profil(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="💰Вывод", callback_data= "вывод")
    builder.button(text="⚙️Очередь", callback_data= "очередь")
    builder.button(text="📥Задать вопрос", callback_data= "задать вопрос")
    builder.adjust(1)
    db = DatabaseManager()
    user = db.get_user_by_telegram_id(telegram_id=message.from_user.id)
    current = user.current_balance
    total = user.total_balance
    #messa = await message.answer(text= "...", reply_markup= ReplyKeyboardRemove())
    await message.answer(text= f"💼Профиль\n\n💸Баланс: <i>{current} рублей</i>\n💲Вы заработали с нами: <i>{total} рублей</i>", reply_markup= builder.as_markup(), parse_mode= ParseMode.HTML)
    #await bot.edit_message_text(text= "💼Профиль\n\n💸Баланс: <i>0 рублей</i>\n💲Вы заработали с нами: <i>0 рублей</i>",chat_id= message.chat.id, message_id= messa.message_id, reply_markup= builder.as_markup(), parse_mode= ParseMode.HTML  )
    config = SessionService.SessionService(message.chat.id)
    config.nav_point = "profil"


@dp.message(F.text == "💼Загрузить логи💼")
async def process_button_click(message: types.Message):
    keyboard = ReplyKeyboardMarkup(keyboard= [
        [KeyboardButton(text= "login:password")]
    ],resize_keyboard= True, one_time_keyboard= True)
    await message.answer("📄Выберите формат базы📄", reply_markup= keyboard)
    config = SessionService.SessionService(message.chat.id)
    config.nav_point = "profil"
     
     
@dp.message(F.text == "login:password")
async def pages(message: types.Message):
    keyboard = ReplyKeyboardBuilder(markup= sublists)
    keyboard.adjust(3)
    keyboard.row(KeyboardButton(text= "Назад"))
    #keyboard = ReplyKeyboardMarkup(keyboard= [buttons_label[i]], resize_keyboard= True, one_time_keyboard= True)
    builder = InlineKeyboardBuilder()
    builder.button(text= "🧠Инструкция🧠", url= "https://pl.wikipedia.org/wiki/Jan_Pawe%C5%82_II")
    await message.answer(text= "📎Отлично, теперь выберите запрос:\n\n <b>ПРЕЖДЕ ЧЕМ ГРУЗИТЬ ЧИТАЙТЕ ИНСТРУКЦИЮ</b>",reply_markup=builder.as_markup(), parse_mode= ParseMode.HTML)
    await message.answer(text= "🔎Выберите запрос🔎", reply_markup= keyboard.as_markup(resize_keyboard = True))

@dp.message(F.text == "Назад")
async def back_to_work_nigga(message: types.Message):
    config = SessionService.SessionService(message.chat.id)
    if config.nav_point == "📄Выберите формат базы📄":
        keyboard = ReplyKeyboardMarkup(keyboard= [
            [KeyboardButton(text= "login:password")]
        ],resize_keyboard= True, one_time_keyboard= True)
        await message.answer("📄Выберите формат базы📄", reply_markup= keyboard)
        config = SessionService.SessionService(message.chat.id)
        config.nav_point = "📄Выберите формат базы📄" 
    if config.nav_point == "profil":
        keyboard = ReplyKeyboardBuilder()
        keyboard.row(KeyboardButton(text ="💼Загрузить логи💼"))
        keyboard.row(KeyboardButton(text= "👑Профиль👑"), KeyboardButton(text= "🧠Инструкция🧠"), KeyboardButton(text= "🔎Актуальные запросы🔎"))
        await message.answer(text= "Нажмите на кнопку ниже 👇, чтобы начать работу", reply_markup= keyboard.as_markup(one_time_keyboard = True, resize_keyboard = True))
        config.nav_point = "profil"


@dp.callback_query(F.data == "вывод")
async def withdrawal(call):
    builder = ReplyKeyboardBuilder()
    builder.button(text = "🍋Bitcoin")
    builder.button(text= "USDT TRC-20")
    builder.button(text= "🛒Market LZT")
    builder.button(text= "Назад")
    builder.adjust(3)
    
    await call.message.answer(text = "💸Выберите платежную систему", reply_markup = builder.as_markup(one_time_keyboard = True, resize_keyboard = True))
   
@dp.message(F.document)
async def handle_document(message: types.File):
    
    # Handle the received document
    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)

    # Download the file
    file_path = file_info.file_path
    file_data = await bot.download_file(file_path)
    ss = SessionService.SessionService(message.from_user.id)
    if not ss.sending_file:
        
        return
    def count_files_in_directory(directory_path):
        try:
            
            files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

            
            num_files = len(files)

            return num_files

        except FileNotFoundError:
            return -1  
        
    number_of_files = count_files_in_directory('./user_input')
    # Save the file to the specified directory
    base_name = os.path.splitext(message.document.file_name)[0]
    save_path = f"user_input/{base_name}_f{ number_of_files+ 1}"
    await bot.download_file(file_path, save_path) 
    existing_file_path = save_path # Replace with the actual path to your existing file

    
    # Check if the file exists
    if os.path.exists(existing_file_path):
        # Get the directory and base name of the file
        directory, base_name = os.path.split(existing_file_path)

        # Add the ".txt" extension to the base name
        new_file_name = os.path.join(directory, base_name + '.txt')

        # Rename the file
        os.rename(existing_file_path, new_file_name)
        
    try:
        reader = ReadFileService.FileProcessorFacade()
        data = reader.process_file(new_file_name)    
        website = ss.website
        check_service = CheckManager.CheckForUniqRowsService(data, website)
        rows , duplicates= check_service.getUniqRows()
    except Exception:
        await message.reply('Неверный формат файла.')
        return
    db = DatabaseManager()
    
    file_id = db.insert_event(message.from_user.id, new_file_name, "Waited")
    ss.sending_file = False
    await AdminsMessage(bot=bot).send_message(rows,file_id,new_file_name,website,message.from_user.id)
    
    await message.reply('⌛️ Ожидайте сейчас наш бот проверит строки на уникальность.')
    await message.reply(f"👑 Файл - # {file_id} был загружен 👑.\n\n\n✅ Уникальных строк. {rows}.\n❌ Повторений: {duplicates}.\n⚠️ Совпадений с базой: {duplicates}")


        
@dp.callback_query(F.data.endswith('NOTIFY'))
async def recieve_callback(call):

    user_id = call.data.replace("NOTIFY","")

    await call.answer("✔️Оповестил пользователя что был найден валид и в скором времени начислят баланс.") 
    builder = InlineKeyboardBuilder()
    file_id = call.message.caption.split("File_id: ")[1]
    builder.button(text="Пополнить баланс пользователю", callback_data=f"{file_id}SETBALANCE")
     
    await call.message.edit_caption(caption = call.message.caption , reply_markup = builder.as_markup(), parse_mode = ParseMode.HTML  )
    await bot.send_message(user_id, f"Отработчик приступил к чеку вашего файла - {file_id}\nОжидайте в скором времени результаты",parse_mode= ParseMode.HTML)

@dp.callback_query(F.data.endswith("SETBALANCE"))
async def revieve_balance(call):
    file_id = call.data.replace("SETBALANCE","")

    
    await bot.send_message(call.from_user.id,  f"Введите команду  ```\n /set_balance {file_id}:баланс ``` ", parse_mode=ParseMode.MARKDOWN)
    
@dp.message(Command('set_balance'))
async def handle_balance(message: types.Message):
    
    db = DatabaseManager()
    
    if str(message.from_user.id) != str(config.RECEPIENT_ID):
        
        await bot.send_message(text="Нету прав администратора", chat_id=message.from_user.id) 
        return
    text = message.text.replace("/set_balance ","")
    file_id = text.split(":")[0]
    balance = text.split(":")[1]
    
    if db.it_closed(file_id=file_id): 
         
        await bot.send_message(text="Деньги за этот файл уже начислены на баланс", chat_id=message.from_user.id)
        return
     
    validator = AdminEvents.SetBalance()
    
    valid_text = validator.valide([file_id, balance])
    
    if valid_text == "Valid":
        db = DatabaseManager()
        file = db.get_file_by_id(int(file_id))
        telegram_id = file.user_id
        user_id = db.get_user_by_telegram_id(telegram_id=telegram_id).user_id
        balance = int(balance)
        db.update_current_balance(user_id=user_id, amount = balance)
        db.update_event_status(file_id=file_id, status_id='CLOSED')
        await bot.send_message(text = "Сумма зачислена на баланс пользователя", chat_id=message.from_user.id)
        
    else: 
    
        await bot.send_message(text= valid_text, chat_id=message.from_user.id)
        
 
async def vivod(message: types.Message):
    telegram_id = message.from_user.id
    ss = SessionService.SessionService(telegram_id)
    if ss.event  == 'No events':
        
        
        ss.event = "Billing:amounts"

        await message.answer("Введите сумму которую желаете вывести: ")
        return 
@dp.message()
async def message(message: types.Message):      
    
    telegram_id = message.from_user.id
    ss = SessionService.SessionService(telegram_id)
    if message.text in requests:
        await message.answer(text= "📁Отправьте мне .txt файл с базой!")
         
        ss.sending_file = True
        ss.website = message.text
        return
    if message.text in system_payments:
        ss.payment_system = system_payments_dict[message.text]
        db = DatabaseManager()
        if db.getRequestOpenedRequestForUser(telegram_id=telegram_id):
            
            await vivod(message)
        else:
            await message.answer("Вы уже открыли запрос на вывод денег. Дождитесь закрытия предыдущего. ")
            ss.event = "No events"
            ss.rekvizits = ""
            ss.amount_to_wayout = ""
            return
        
        return
        
       
    if ss.event == "Billing:amounts":
        
        validator = AdminEvents.Payments()
         
        text = validator.valid_amount(message.text)
        
        if text == "OK":
            
            db = DatabaseManager()
            if not db.balanceQuotte(telegram_id, int(message.text)): 
                await message.answer("У вас недостачно денег на балансе: ")
                return 
            ss.event = "Billing:rekvizits"
            ss.amount_to_wayout = message.text
            
            await message.answer("Введите реквизиты: ")
            return
        else:
            await message.answer(text)
            return
        
        
    
    if ss.event == 'Billing:rekvizits':
        
        ss.rekvizits = message.text
        payment = ss.payment_system 
        text = f"Система выплаты: {payment},\nСумма: {ss.amount_to_wayout},\nРеквизиты: {ss.rekvizits}"
        builder = InlineKeyboardBuilder()
        builder.button(text = "Подтвердить",callback_data='ApproveCreate_order')
        builder.button(text = "Отменить" , callback_data='DeclineCreate_order')
        await message.answer(text , parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())
        
@dp.callback_query(F.data.endswith('Create_order'))
async def create_order(call):
    telegram_id = call.from_user.id
    ss = SessionService.SessionService(telegram_id)
    text = call.data.replace('Create_order', '')
            
    if text == "Approve":
        db = DatabaseManager()
       
        input_string = call.message.text
        pairs = [pair.strip() for pair in input_string.split(',')]
        result_dict = {}
        for pair in pairs:
            key, value = [part.strip() for part in pair.split(':')]
            result_dict[key] = value
        
        await AdminsMessage(bot).request_for_money(result_dict, telegram_id)
        await call.message.edit_text("Запрос на вывод средств в обработке. Ждите уведомление об изменении баланса")
        ss.event = "No events"
    if text == "Decline": 
        ss.event = "No events"
        ss.amount_to_wayout = ""
        ss.rekvizits = ""
        
        await call.message.edit_text("Запрос на вывод средств отменен.")
        
    call.answer('')
    
@dp.callback_query(F.data.endswith('finish_payment'))
async def finish_payment(call):
    telegram_id = call.data.replace('finish_payment', '')
    db = DatabaseManager()
    input_string = call.message.text
    pairs = [pair.strip() for pair in input_string.split(',')]
    result_dict = {}
    for pair in pairs:
        key, value = [part.strip() for part in pair.split(':')]
        result_dict[key] = value
    
    
    user_id = db.get_user_by_telegram_id(telegram_id=telegram_id).user_id
    db.close_requests(telegram_id=telegram_id)
    db.update_current_balance(user_id=user_id, amount=int(result_dict['Сумма']) * -1)
    await call.message.edit_text("Заявка выполнена. Средства списаны из баланса пользователя.")

@dp.callback_query(F.data.endswith('cancel_payment'))
async def close_payment(call):
    telegram_id = call.data.replace('cancel_payment', '')
    db = DatabaseManager()
     
    db.close_requests(telegram_id=telegram_id)
    message = 'Ваша заявка была отклонена администратором'
    url = f"https://api.telegram.org/bot{config.TOKEN}/sendMessage?chat_id={telegram_id}&text={message}"
       
    req.get(url)     
    await call.message.edit_text("Заявка отменена. ") 
 
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    print("Bot Stoped!")