from random import choice, randint

def get_response(user_input: str) -> str:
    lowered : str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent you ni'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'suck my dickkkkkkk'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}' 
    else:
        return choice(['I do not understand...',
                       'Please repeat again...',
                       'What the fuckkkkkkkkk'])