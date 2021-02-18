

import telegram
token = '1645992533:AAFvEflavorLqjagQ2EmCoC2h3rF3KjFg8o'

print("Obtaining bot information")
print()

ham_bot=telegram.Bot(token)
get = ham_bot.getMe()

print('bot id is: ' + str(get['id']))
print('The name of the bot is: ' + str(get['first_name']))
print('user name is: ' + str(get['username']))
print()

print('73')

