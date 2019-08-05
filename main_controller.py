import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
import time
import random
import json
from answers import GetAnswer
from msg_sender import Sender

settings = open("settings", mode="r", encoding="utf-8")
sett_data = json.loads(settings.read())

token = sett_data["other"]["token"]
vk = vk_api.VkApi(token=token)
vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, sett_data["other"]["group_id"])


process_message = GetAnswer
sender = Sender(vk)
while True:
    # try:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            process_message(sender=sender, msg=event.object, settings=sett_data)

        time.sleep(1)
# except Exception:
#     time.sleep(1)
