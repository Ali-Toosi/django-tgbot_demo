from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from ..bot import state_manager, TelegramBot
from ..models import TelegramState


state_manager.set_default_update_types(update_types.Message)


@processor(state_manager, from_states='asked_for_name', success='asked_for_email', fail=state_types.Keep, message_types=message_types.Text)
def get_name(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    name = update.get_message().get_text()
    if len(name) < 3:
        bot.sendMessage(chat_id, 'Name is too short! Try again:')
        raise ProcessFailure

    state.set_memory({
        'name': name
    })

    bot.sendMessage(chat_id, 'Beautiful! What is your email address?')


@processor(state_manager, from_states='asked_for_email', success=state_types.Reset, fail=state_types.Keep, message_types=message_types.Text)
def get_email(bot, update, state):
    chat_id = update.get_chat().get_id()
    email = update.get_message().get_text()
    
    if email.find('@') == -1:
        bot.sendMessage(chat_id, 'Invalid email address! Send again:')
        raise ProcessFailure

    name = state.get_memory()['name']

    bot.sendMessage(chat_id, 'Thanks! You successfully signed up with these details:\nName: {}\nEmail: {}'.format(name, email))
    
    state.set_memory({})
