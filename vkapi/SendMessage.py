import json

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
                                   keyboard=self.keyboard, )
        except Exception as e:
            print(e)

    def sendMessage(self, message, uid):
        self.api.messages.send(access_token=self.token, user_id=uid, message=message, keyboard=self.keyboard,
                               )

    def sendmsg(self, msg):
        pass

    def sendSuccess(self):
        pass

    def sendError(self, uid):
        self.api.messages.send(access_token=self.token, user_id=uid, message="я не понимаю", keyboard=self.keyboard,
                               )
