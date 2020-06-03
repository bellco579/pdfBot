from services.db import dbInterface
from vkapi.main import Main as vkApp

add_receiver = "Добавить получателя"
delete_receiver = "Удалить получателя"
my_uid = "Мой id"
begin = "Начать"
send = "Отправить"
add = "добавить"
msg_templates = {
    add_receiver: " {} будет получать pdf",
    delete_receiver: " {} больше не будет получать pdf",
    "add_receiver_context": "введите id пользователя",
    "delete_receiver_context": "введите цифру\n",
    "instruction": "Привет! Теперь ты можешь использовать это приложение для перевода фотографий в pdf.\n\
    📎Чтобы отправить свой документ другому человеку, нажми •добавить получателя• и введи его id.\n\
    📍Теперь он тоже будет получать твои документы, пока ты его не удалишь: нажми •удалить получателя•, затем выбери цифру.\n\
    📌Отправляя фотографии, подпиши сообщение так, как должен называться документ. ",

}


class Command:
    def __init__(self, command: str, context: str, api: vkApp, db: dbInterface):
        self.command = command
        self.context = context
        self.api = api
        self.db = db
        if command == add_receiver:
            try:
                user = self.api.get_user_info(uid=int(context))
                receiver = self.db.add_linked_user(user)
                msg = msg_templates[add_receiver].format(receiver.first_name)
                self.api.send_message(msg)
            except Exception as e:
                print(e)
        if context == add_receiver:
            msg = msg_templates["add_receiver_context"]
            self.api.send_message(msg)
        if command == delete_receiver:
            try:
                user = self.db.del_linked_user(int(context))
                msg = msg_templates[delete_receiver].format(user.first_name)
                self.api.send_message(msg)
            except Exception as e:
                print("command {}, error:{}".format(delete_receiver, e))
        if context == delete_receiver:
            msg = msg_templates["delete_receiver_context"]
            count = 0
            for user in self.db.get_linked_user():
                msg += "{0} {1}\n".format(count, user.receiver.first_name)
                count += 1
            self.api.send_message(msg)
        if context == my_uid:
            self.api.send_message(self.api.uid)

        if context == begin:
            msg = msg_templates["instruction"]
            self.api.send_message(msg)