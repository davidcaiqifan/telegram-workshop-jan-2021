from pprint import pprint

import telebot
from flask import request
from mal import Anime
from pip._internal import commands

from api.dialogflow_api import detect_intent_via_text, detect_intent_via_event
from api.telegram_api import send_message, bot
from beans.session import Session
from beans.user import User
from cache import get_current_session
from command_handlers import COMMAND_HANDLERS, handle_invalid_command
from intent_handlers import INTENT_HANDLERS, handle_invalid_intent
from main import app
from utils import \
    get_user_from_request, \
    get_user_input_from_request, \
    default_if_blank, \
    is_not_blank, \
    get_user_command_from_request


@app.route('/')
def hello_world():
    return 'Hello, World!'


# Validates incoming webhook request to make sure required fields are present, before processing
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     # FILL IN CODE
#     req_body = request.get_json()
#     user = get_user_from_request(req_body)
#     session = get_current_session(user)
#     user_input = get_user_input_from_request(req_body)
#
#     if is_not_blank(user.id, user_input):
#         __process_dialogflow_input(user, session, user_input)
#     return 'Got your message'

# Validates incoming webhook request to make sure required fields are present, before processing
@app.route('/webhook', methods=['POST'])
def webhook():
    req_body = request.get_json()
    user = get_user_from_request(req_body)
    session = get_current_session(user)
    user_input = get_user_input_from_request(req_body)
    anime = Anime(1)  # Cowboy Bebop

    print(anime.score)  # prints 8.82

    anime.reload()  # reload object
    anime.score.as_integer_ratio()
    print(anime.score)  # prints 8.81
    bot.send_message(user.id, 'Anime is rated ' + str(anime.score))
    #send_message(user, session, 'Anime is rated ' + str(anime.score))
    return 'Anime is rated ' + str(anime.score)


# Calls Dialogflow API to trigger an intent match
# Calls the corresponding function handler for the intent result action if present
def __process_dialogflow_input(user: User, session: Session, user_input):
    intent_result = detect_intent_via_text(session.id, user_input)
    intent_action = default_if_blank(intent_result.action, '')
    if is_not_blank(intent_action):
        INTENT_HANDLERS.get(intent_action, handle_invalid_intent)(user, intent_result, session.id)
    return intent_result
