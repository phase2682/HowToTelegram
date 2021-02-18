
import time
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#action to be executed when a message is received
def action(update, context):
	message = update.message.text
	chat_id = update.effective_chat.id
	now = datetime.datetime.utcnow()
	
	print('sender id is: ' + str(chat_id))
	print('The message is: '+ str(message))


token = 'Bot access token'

print()

updater_hambot = Updater(token)						#establishes update link to the bot
dispatcher_hambot = updater_hambot.dispatcher		#dispatches the updates
updater_hambot.start_polling()						#starts polling service to get updates from Telegram

#handler for messages	
msg_handler = MessageHandler(Filters.text & (~Filters.command), action)
dispatcher_hambot.add_handler(msg_handler)			#adds msg handler 


while 1:
		print('listening')
		time.sleep(30)

