import os

ROOT = os.path.join(os.path.dirname(__file__), '..')

COMMANDS_PATH = os.path.join(ROOT, 'commands')

REACTIONS_YESORNO = ['â', 'â']
REACTIONS_ANSWERS = ["đĻ", "đ§", "đ¨", "đŠ", "đĒ", "đĢ", "đŦ", "đ­", "đŽ", "đ¯", "đ°", "đą", "đ˛", "đŗ", "đ´", "đĩ", "đļ", "đˇ", "đ¸", "đš", "đē"]
REACTIONS_FINISH = ['âšī¸']

REACTIONS = {
    'yesorno': REACTIONS_YESORNO,
    'answers': REACTIONS_ANSWERS,
    'finish': REACTIONS_FINISH
}