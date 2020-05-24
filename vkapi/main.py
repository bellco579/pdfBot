import json

import vk_requests
import requests
import vk_api
import vk

from vkapi import config
from vkapi.SendMessage import Messages
from vkapi.keyboard import getKeyboard, extend_pdf_keybord
from vkapi.models import UserInfo
from vkapi.photo import Photo
from vkapi.services import get_user, upload_file

token = config.token
vk_session = vk_api.VkApi(token=token)
session = vk.Session()
api = vk.API(session, v=5.8)
id = 1

keyboard = getKeyboard()
ex_pdf_keyboard = extend_pdf_keybord()


class Main:
    def __init__(self, request: json):
        self.rq = json.loads(request.body, encoding="utf-8")
        if self.rq['type'] == "message_new":
            body = self.rq["object"]['message']
            self.msg = self.get_message_by_id(body["id"])
        self.uid = self.msg['user_id']
        self.message = Messages(token, keyboard, api=api)
        self.text_msg = self.msg['body']

    def get_user_info(self, uid=None):
        if uid is None:
            uid = self.uid
        return get_user(api=api, token=token, uid=uid)

    def get_photos_url(self):
        try:
            attachments = self.msg['attachments']
            return Photo().get_photo_url(attachments)
        except:
            return None

    def set_ex_pdf_keyboard(self):
        self.message.keyboard = ex_pdf_keyboard

    def set_default_keyboard(self):
        self.message.keyboard = keyboard

    def send_message(self, message, uid=None):
        if uid is None:
            uid = self.uid
        self.message.sendMessage(message=message, uid=uid)

    def send_doc(self, uid, doc, name, message):
        self.message.keyboard = keyboard
        attach = upload_file(api=api, token=token, title=name, file=doc)
        self.message.sendPdfToUser(attach, uid, message=message)

    def get_message_by_id(self, mid):
        return api.messages.getById(access_token=token, message_ids=mid)["items"][0]
