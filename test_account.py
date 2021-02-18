

import telegram
token = 'Bot access token'

print("Obtaining bot information")
print()

hambot=telegram.Bot(token)
get = hambot.getMe()

print('bot id is: ' + str(get['id']))
print('The name of the bot is: ' + str(get['first_name']))
print('user name is: ' + str(get['username']))
print()

print('73')

