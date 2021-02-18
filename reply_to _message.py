
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time
import datetime
from time import sleep


token = 'Bot access token'

#action to be executed with a message
def action(update, context):
	message = update.message.text
	chat_id = update.effective_chat.id
	now = datetime.datetime.utcnow()
	
	print('sender id is: ' + str(chat_id))
	print('The message is: '+ str(message))
	print ('sending a reply')
	if 'cq' in message or 'CQ' in message:
		context.bot.send_message(chat_id, str(chat_id) +' de ur callsign')
	elif 'date' in message or 'Date' in message:
	    context.bot.send_message(chat_id, str('Date: ') + now.strftime ("%B %d, %Y UTC"))
	else:
		# context.bot.sendMessage(chat_id, 'tu fer ur message 73')
		update.message.reply_text('tu fer ur message 73')
		
	
#action to be executed with a /time command
def time(update, context):	
	now = datetime.datetime.utcnow()		
	context.bot.send_message(update.effective_chat.id, str('Time: ') + now.strftime("%H:%M:%S UTC"))

#action to be executed with an unknown command
def unknown(update, context):			
	context.bot.send_message(chat_id=update.effective_chat.id, text= 'Command not recognized, no action taken')

	
	
updater_hambot = Updater(token)						#establishes update link to the bot
dispatcher_hambot = updater_hambot.dispatcher		#dispatches the updates
updater_hambot.start_polling()						#starts polling service to get updates from Telegram

#handler for /time	
time_handler = CommandHandler('time', time)		
dispatcher_hambot.add_handler(time_handler)			#adds /time handler 

#handler for messages	
msg_handler = MessageHandler(Filters.text & (~Filters.command), action)
dispatcher_hambot.add_handler(msg_handler)			#adds msg handler 

#handler for unknown command
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher_hambot.add_handler(unknown_handler)		#adds unknown handler 







while 1:
		print('listening')
		sleep(30)

