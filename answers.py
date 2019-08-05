import json

class GetAnswer:
    def __init__(self, sender, msg=None, settings={}):
        if msg != {} and settings != {}:
            self.sender = sender
            self.msg = msg
            self.id = msg.peer_id
            self.body = msg.text
            self.sett = settings
            self.main_keyboard = settings['other']['main_keyboard']
            self.main_keyboard = json.dumps(self.main_keyboard, ensure_ascii=False).encode('utf-8')
            self.cost_keyboard = settings['other']['costs_keyboard']
            self.cost_keyboard = json.dumps(self.cost_keyboard, ensure_ascii=False).encode('utf-8')

            self.get_answer()
            self.send_to_admins()

    def get_answer(self):
        if self.body.lower() == 'начать':
            ans = self.sett["answers"]["start_message"]
            self.sender.define_type(type="keyboard")(keyboard=self.main_keyboard, id=self.id, message=ans)


        elif self.body.lower() == 'доставка' or self.body.lower() == 'о доставке' or self.body.lower() == 'про доставку' or (
                'payload' in self.msg and 'button' in self.msg['payload'] and json.loads(self.msg['payload'])[
            'button'] == "1"):
            ans = self.sett["answers"]["доставка"]

            self.sender.define_type(type='text')(id=self.id, message=ans)

        elif self.body.lower() == 'цены' or self.body.lower() == 'цена' or (
                'payload' in self.msg and 'button' in self.msg['payload'] and json.loads(self.msg['payload'])[
            'button'] == "2"):
            ans = self.sett["answers"]["cost"]
            self.sender.define_type(type="keyboard")(keyboard=self.cost_keyboard, id=self.id, message=ans)

        elif 'payload' in self.msg and 'button' in self.msg['payload'] and json.loads(self.msg['payload'])[
            'button'] == "3" or self.body.lower() == "фотопечать" or self.body.lower() == "цены на фотопечать" or self.body.lower() == "цены на фото" or self.body.lower() == "фото":
            ans = self.sett["answers"]["cost_photo"]
            self.sender.define_type(type='keyboard')(keyboard=self.main_keyboard, id=self.id, message=" ")
            self.sender.define_type(type="image")(file_name=self.sett['other']['images']['photo'], id=self.id,
                                                  message=ans)

        elif 'payload' in self.msg and 'button' in self.msg['payload'] and json.loads(self.msg['payload'])[
            'button'] == "4" or self.body.lower() == "ксерокопия" or self.body.lower() == "цены на ксерокопию" or self.body.lower() == "цены на ксеро" or self.body.lower() == "ксеро":
            ans = self.sett["answers"]["cost_copy"]
            self.sender.define_type(type='keyboard')(keyboard=self.main_keyboard, id=self.id, message=" ")
            self.sender.define_type(type="image")(file_name=self.sett['other']['images']['copy'], id=self.id,
                                                  message=ans)

        else:
            if self.body.lower() in self.sett["custom_answers"]:
                ans = self.sett["custom_answers"][self.body.lower()]
                self.sender.define_type(type="text")(id=self.id, message=ans)

    def send_to_admins(self):
        if str(self.id) not in self.sett["admins_settings"]["ids"] and (
                len(self.sett["admins_settings"]["words_for_spy"]) == 0 or self.body.lower() in
                self.sett["admins_settings"]["words_for_spy"]):
            for i in range(len(self.sett["admins_settings"]["ids"])):
                if self.sett["admins_settings"]["spy"][i]:
                    a_id = int(self.sett["admins_settings"]["ids"][i])
                    ans = 'Пользователь vk.com/' + str(self.id) + ' напсал в сообщество: \n\n' + self.body
                    self.sender.define_type(type="text")(message=ans, id=a_id)
