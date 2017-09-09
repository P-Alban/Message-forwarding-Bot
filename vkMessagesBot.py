import vk_api
import telebot
import datetime
from time import sleep

token = '...'
bot = telebot.TeleBot(token)
def authSession(login, password):
	# get vk session
	vk_session = vk_api.VkApi(login, password)
	try:
		vk_session.auth()
	except Exception as authorizationError:
		print(authorizationError)
	return vk_session.get_api()

def getMessages(session):
	# get all unread messages
	while True:
		for msg in session.messages.get(count = 5)['items']:
			if not msg['read_state']:
				if msg['body']:
					sendMessageInTelegram(msg, session)
				if 'attachments' in msg:
					# if photo in message
					if msg['attachments'][0]['type'] == 'photo':
						sendMessageInTelegram(msg, session, True)
			sleep(0.3)

def markMessageAsRead(message, session):
	# mark unread message as read
	return session.messages.markAsRead(message_ids = message)

def sendMessageInTelegram(message, session, is_media = False):
	# get user firstname and lastname
	Name = session.users.get(user_ids = message['user_id'])[0]
	# get post date
	value = datetime.datetime.fromtimestamp(message['date'])
	date = value.strftime('%Y-%m-%d %H:%M:%S')
	bot.send_message(chat_id = '@GroupUserName', parse_mode = 'Markdown', text = '[[{0} {1}]]\n`{2}`\n{3}'.format(Name['first_name'], 
		Name['last_name'],
		date,
		message['body']))
	if is_media:
		# get photo size
		maxPhotoSize = getMaxPhotoSize(message['attachments'][0]['photo'])
		bot.send_photo(chat_id = '@GroupUserName', photo = message['attachments'][0]['photo'][maxPhotoSize])
	# mark message as read
	markMessageAsRead(message['id'], session)

def getMaxPhotoSize(photo):
	# get max photo size
	size = max([int(x.split('_')[1]) for x in photo.keys() if 'photo' in x])
	return list(filter(lambda x: str(size) in x, photo))[0] 

def main():
	while True:
		try:
			getMessages(authSession(login = '', password = ''))
		except Exception as ConnectionVkError:
			print(ConnectionVkError)

if __name__ == '__main__':
	main() # run
