# Extracts user's input (text or button click) from Telegram request
def get_user_anime_input_from_request(req_body):
    if 'callback_query' in req_body:
        return req_body.get('callback_query', {}).get('data', '')
    elif 'message' in req_body:
        return req_body.get('message', {}).get('text', '')
    else:
        return ''
