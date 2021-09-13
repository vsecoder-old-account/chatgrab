import telethon, json, asyncio, random
from telethon.sync import TelegramClient
from telethon import connection
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

async def dump_all_participants(channel, text):
	offset_user = 0    # номер участника, с которого начинается считывание
	limit_user = 100   # максимальное число записей, передаваемых за один раз
	result = 0         # получило рекламу
	replace_link = ['https://t.me/', 'http://t.me/', '@']
	for repl in replace_link:
		channel = channel.replace(repl, '')

	all_participants = []   # список всех участников канала
	filter_user = ChannelParticipantsSearch('')

	async with TelegramClient('client', 123456, '123456123456123456123456') as client:
		while True:
			participants = await client(GetParticipantsRequest(channel,
				filter_user, offset_user, limit_user, hash=0))
			if not participants.users:
				break
			all_participants.extend(participants.users)
			offset_user += len(participants.users)

		all_users_details = []   # список словарей с интересующими параметрами участников канала

		for participant in all_participants:
			try:
				send = False
				await asyncio.sleep(random.choice([1, 2, 0.5, 0.3]))
				if participant.bot == False and participant.username:
					text1 = text.replace('%name%', f'{participant.first_name}')
					text1 = text1.replace('%username%', f'{participant.username}')
					await client.send_message(participant.username, text1)
					send = True
					result += 1
			except Exception as e:
				print(e)
				if e == 'Too many requests (caused by SendMessageRequest)':
					await asyncio.sleep(random.choice([8, 9, 10.5, 13.3]))
			
			all_users_details.append({"id": participant.id,
				"first_name": participant.first_name,
				"last_name": participant.last_name,
				"username": participant.username,
				"phone": participant.phone,
				"is_bot": participant.bot,
                "send": send})

	with open('channel_users.json', 'w', encoding='utf8') as outfile:
		json.dump(all_users_details, outfile, ensure_ascii=False)
	
	return result
