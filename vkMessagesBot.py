import vk
import telebot
import datetime
from time import sleep

token = '416525856:AAFfqq'
bot = telebot.TeleBot(token)
sendUserInfoFlag = True
def authSession(login, password):
	# get vk session
	Session = vk.AuthSession(app_id=000, user_login=login, user_password=password,
                                     scope='messages')
	return vk.API(Session)

def getMessages(session):
	global sendUserInfoFlag 
	# get all unread messages
	while True:
		for msg in session.messages.get(count = 4)[1:]:
			if not msg['read_state']:
				sendUserInfoFlag = True
				if msg['body']:
					sendMessageInTelegram(msg, session)
				if 'attachments' in msg:
					# if photo in message
					for photos in msg['attachments']:
						if photos['type'] == 'photo':
							sendPhotos(photos, msg, session)
				# mark message as read
				markMessageAsRead(msg['mid'], session)
			sleep(0.5)

def markMessageAsRead(message, session):
	# mark unread message as read
	return session.messages.markAsRead(message_ids = message)

def sendMessageInTelegram(message, session):
	global sendUserInfoFlag
	# get user firstname and lastname
	Name = session.users.get(user_ids = message['uid'])[0]
	# get post date
	value = datetime.datetime.fromtimestamp(message['date'])
	date = value.strftime('%Y-%m-%d %H:%M:%S')
	bot.send_message(chat_id = '@', parse_mode = 'Markdown', text = '[[{0} {1}]]\n`{2}`\n{3}'.format(Name['first_name'], 
		Name['last_name'],
		date,
		message['body']))
	sendUserInfoFlag = False

def sendPhotos(photo, message, session):
	global sendUserInfoFlag
	# get photo size
	if sendUserInfoFlag:
		Name = session.users.get(user_ids = message['uid'])[0]
		# get post date
		value = datetime.datetime.fromtimestamp(message['date'])
		date = value.strftime('%Y-%m-%d %H:%M:%S')
		bot.send_message(chat_id = '@', parse_mode = 'Markdown', text = '[[{0} {1}]]\n`{2}`'.format(Name['first_name'], 
			Name['last_name'],
			date))
	bot.send_photo(chat_id = '@', photo = photo['photo']['src_big'])
	sendUserInfoFlag = False

def main():
	while True:
		try:
			getMessages(authSession(login = '', password = ''))
		except Exception as Error:
			print(Error)

if __name__ == '__main__':
	main() # run
