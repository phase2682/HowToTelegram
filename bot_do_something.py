import datetime
import time
import RPi.GPIO as gpio
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


token = 'Bot access token'

you = 'your id'

#Other authorized users
ham2 = 'ham2 id'

#list of authorized users
users = [you, ham2]  

LED = 21						#pin for LED
LED_mon = 20					#pin for monitoring LED

##set up outputs
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(LED, gpio.OUT)
gpio.output(LED, False) 		#initial state



#setup inputs
gpio.setup(LED_mon, gpio.IN)      


#action to take with text messages from authorized users
def action(update, context):
	message = update.message.text
	chat_id = update.effective_chat.id
	now = datetime.datetime.utcnow()
	print('The message is: ' + str(message))
	print('sending a reply')
	if ('LEDon' in message or 'Ledon'in message):
		context.bot.send_message(chat_id, 'Ham_bot is turning on LED by message')
		gpio.output(LED, True)
	elif ('LEDoff' in message or 'Ledoff'in message):
		context.bot.send_message(chat_id, 'Ham_Bot is turning off LED by message')
		gpio.output(LED, False)
	elif ('LEDstatus' in message or 'Ledstatus'in message):
		if gpio.input(LED_mon):
			context.bot.send_message(chat_id, 'Ham_Bot has found that the LED is on (message)')
		else:
			context.bot.send_message(chat_id, 'Ham_Bot has found that the LED is off (message)')
			 
	else:
		update.message.reply_text('Message not recognized, no action taken')


#action to take with a /start command
def start(update, context):			
	context.bot.send_message(chat_id=update.effective_chat.id, text="I control your LED, send me the right message or command.  But I will only respond if you are an authorized user.")

#action to take with /LedOn command from authorized users
def LedOn(update, context):
		context.bot.send_message(update.effective_chat.id, 'Ham_Bot is turning on LED by command')
		gpio.output(LED, True)

#action to take with /LedOff command from authorized users
def LedOff(update, context):
		context.bot.send_message(update.effective_chat.id, 'Ham_Bot is turning off LED by command')
		gpio.output(LED, False)

#action to take with /LedStatus command from authorized users
def LedStatus(update, context):
		if gpio.input(LED_mon):
			context.bot.send_message(update.effective_chat.id, 'Ham_Bot has found that the LED is on (command)')
		else:
			context.bot.send_message(update.effective_chat.id, 'Ham_Bot has found that the LED is off (command)')
	
#action to take with text messages from non authorized users
def non_user(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry but you are not an authorized user.")
	context.bot.send_message(chat_id=you, text="Access attempted by " + str(update.effective_chat.id))

#action to take with an unknown command
def unknown(update, context):			
	context.bot.send_message(chat_id=update.effective_chat.id, text= 'Command not recognized, no action taken')

updater_hambot = Updater(token)						#establishes update link to the bot
dispatcher_hambot = updater_hambot.dispatcher		#dispatches the updates

#handler for /start	
start_handler = CommandHandler('start', start)		
dispatcher_hambot.add_handler(start_handler)		#adds /start handler 

#handler for LED messages	
LED_handler = MessageHandler(Filters.chat(users) & Filters.text & (~Filters.command), action)
dispatcher_hambot.add_handler(LED_handler)			#adds LED handler 	

#handler for non authorized user
non_user_handler = MessageHandler(~Filters.chat(users) & Filters.text & Filters.command, non_user)
dispatcher_hambot.add_handler(non_user_handler)		#adds non_user handler 

#handler for /LedOn
LedOn_handler = CommandHandler('LedOn', LedOn, Filters.chat(users))		
dispatcher_hambot.add_handler(LedOn_handler)		#adds /LedOn handler 

#handler for /LedOff
LedOff_handler = CommandHandler('LedOff', LedOff, Filters.chat(users))		
dispatcher_hambot.add_handler(LedOff_handler)		#adds /LedOff handler 

#handler for /LedStatus
LedStatus_handler = CommandHandler('LedStatus', LedStatus, Filters.chat(users))		
dispatcher_hambot.add_handler(LedStatus_handler)	#adds /LedStatus handler 

#handler for unknown command
unknown_handler = MessageHandler(Filters.chat(users) & Filters.command, unknown)
dispatcher_hambot.add_handler(unknown_handler)		#adds unknown handler 

updater_hambot.start_polling()						#starts polling service to get updates from Telegram



#define send message to telegram
def telegram_send_message(message_text, bot_token, chat_id):
	
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' +str(chat_id) + '&parse_mode=Markdown&text=' + message_text
	
	response = requests.get(send_text)
	
	return response.json

#thread that runs on an interupt
def on_off(pin):                    
    if gpio.input(pin):
	    turn_on_time = datetime.datetime.utcnow()
	    telegram_send_message("LED just turned on" + turn_on_time.strftime(" at %H:%M:%S on %B %d, %Y UTC"), token, you)
                           
    if not gpio.input(pin):
	    turn_off_time = datetime.datetime.utcnow()
	    telegram_send_message("LED just turned off" + turn_off_time.strftime(" at %H:%M:%S on %B %d, %Y UTC"), token, you)
	    

#add interrupt on LED_mon
gpio.add_event_detect(LED_mon, gpio.BOTH, on_off, 100)         #interupt on both rise and fall, initiate on_off thread, 100 mS debounce
                                                               #add interrupt now so power up does not cause interrupt

while 1:
		print('listening')
		time.sleep(30)

