import os

ROOT = os.path.join(os.path.dirname(__file__), '..')

COMMANDS_PATH = os.path.join(ROOT, 'commands')

REACTIONS_YESORNO = ['✅', '❌']
REACTIONS_ANSWERS = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺"]
REACTIONS_FINISH = ['⏹️']

REACTIONS = {
    'yesorno': REACTIONS_YESORNO,
    'answers': REACTIONS_ANSWERS,
    'finish': REACTIONS_FINISH
}