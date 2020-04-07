from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot


state_manager.set_default_update_types(update_types.Message)


@processor(state_manager, from_states=state_types.Reset, message_types=[message_types.Text])
def send_keyboards(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = str(update.get_message().get_text())

    if text.lower() in ['normal keyboard', 'regular keyboard']:
        send_normal_keyboard(bot, chat_id)
    elif text.lower() in ['inline keyboard']:
        send_inline_keyboard(bot, chat_id)
    else:
        send_options(bot, chat_id)


@processor(state_manager, from_states=state_types.All, update_types=[update_types.CallbackQuery])
def handle_callback_query(bot: TelegramBot, update, state):
    callback_data = update.get_callback_query().get_data()
    bot.answerCallbackQuery(update.get_callback_query().get_id(), text='Callback data received: {}'.format(callback_data))


def send_normal_keyboard(bot, chat_id):
    bot.sendMessage(
        chat_id,
        text='Here is a keyboard for you!',
        reply_markup=ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a('Text 1'), KeyboardButton.a('Text 2')],
                [KeyboardButton.a('Text 3'), KeyboardButton.a('Text 4')],
                [KeyboardButton.a('Text 5')]
            ]
        )
    )


def send_inline_keyboard(bot, chat_id):
    bot.sendMessage(
        chat_id,
        text='Here is an inline keyboard for you!',
        reply_markup=InlineKeyboardMarkup.a(
            inline_keyboard=[
                [
                    InlineKeyboardButton.a('URL Button', url='https://google.com'),
                    InlineKeyboardButton.a('Callback Button', callback_data='some_callback_data')
                ]
            ]
        )
    )


def send_options(bot, chat_id):
    bot.sendMessage(
        chat_id,
        text='I can send you two different types of keyboards!\nSend me `normal keyboard` or `inline keyboard` and I\'ll make one for you ;)',
        parse_mode=bot.PARSE_MODE_MARKDOWN
    )
