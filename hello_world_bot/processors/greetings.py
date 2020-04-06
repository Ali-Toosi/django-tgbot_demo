from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.replykeyboardremove import ReplyKeyboardRemove
from ..bot import state_manager, TelegramBot
from ..models import TelegramState


state_manager.set_default_update_types(update_types.Message)


@processor(state_manager, success='asked_for_signup')
def say_hello(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    bot.sendMessage(chat_id, 'Hello! and welcome to this bot :)')
    bot.sendPhoto(chat_id, open('img/welcome.png', 'rb'), upload=True)
    bot.sendMessage(chat_id, 'Have you signed up yet?', reply_markup=ReplyKeyboardMarkup.a(keyboard=[
        [KeyboardButton.a(text='Yes!'), KeyboardButton.a(text='Do it now!')]
    ]))


@processor(state_manager, from_states='asked_for_signup', success=state_types.Keep, exclude_message_types=message_types.Text)
def text_only(bot, update, state):
    bot.sendMessage(update.get_chat().get_id(), 'I\'d appreciate it if you answer in text format 😅')


@processor(state_manager, from_states='asked_for_signup', message_types=message_types.Text)
def start_signup(bot, update, state):
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()
    if text == 'Yes!':
        bot.sendMessage(chat_id, 'Amazing!', reply_markup=ReplyKeyboardRemove.a(remove_keyboard=True))
        state.set_name('')
    elif text == 'Do it now!':
        bot.sendMessage(chat_id, 'Oh absolutely! Let\'s start with your name:', reply_markup=ReplyKeyboardRemove.a(remove_keyboard=True))
        state.set_name('asked_for_name')
    else:
        bot.sendMessage(chat_id, 'I didn\'t get that! Use the keyboard below')


