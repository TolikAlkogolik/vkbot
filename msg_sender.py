import random
import json
import requests

class Sender:
    def __init__(self, vk):
        self.vk = vk

    def define_type(self, type="text"):
        if type == 'text':
            return self.send_text

        elif type == 'keyboard':
            return self.send_keyboard

        elif type == 'image':
            return self.send_image

    def send_text(self, id, message):
        self.vk.method("messages.send", {"peer_id": id, "message": message, "random_id": 0})

    def send_keyboard(self, id, keyboard, message=""):
        self.vk.method("messages.send", {"peer_id": id, "message": message, "random_id": 0,
                                         "keyboard": keyboard})

    def send_image(self, file_name, id, message=""):
        method = self.vk.method("photos.getMessagesUploadServer")
        request = requests.post(method['upload_url'], files={'photo':open(file_name,mode='rb')}).json()
        save = self.vk.method('photos.saveMessagesPhoto', {'photo': request['photo'], 'server': request['server'], 'hash': request['hash']})[0]
        self.vk.method('messages.send', {'peer_id':id, "message": message, "attachment": f'photo{save["owner_id"]}_{save["id"]}', "random_id": 0})
