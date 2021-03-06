import json
import time

import requests
from vk_api.utils import get_random_id


class Messages:
    def __init__(self, token, keyboard, api):
        self.token = token
        self.keyboard = keyboard
        self.api = api

    def sendPdfToUser(self, attach, uid, message=None):
        try:
            self.api.messages.send(access_token=self.token, user_id=uid, message=message, attachment=attach,
                                   keyboard=self.keyboard, random_id=int(time.time()))
        except Exception as e:
            print(e)

    def sendMessage(self, message, uid):
        self.api.messages.send(access_token=self.token, user_id=uid, message=message, keyboard=self.keyboard,random_id=int(time.time())
                               )

    def sendmsg(self, msg):
        pass

    def sendSuccess(self):
        pass

    def sendError(self, uid):
        self.api.messages.send(access_token=self.token, user_id=uid, message="я не понимаю", keyboard=self.keyboard,random_id=int(time.time())
                               )

    def send_add_image_invite(self, uid):
        self.sendMessage(uid=uid, message="Добавить?")
