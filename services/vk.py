import threading

from core.models import Message
from services.converter import photo_converter, add_photo_to_file
from services.db import dbInterface
from services.services import MessageService, SavePhoto, PDF
from services.work_with_str import Command
from vkapi.main import Main
from . import work_with_str as wws


class Vk:
    def __init__(self, rq):
        self.vkapi = Main(rq)
        self.db = dbInterface(self.vkapi.uid)
        photo_list = self.vkapi.get_photos_url()
        self.u_info = self.vkapi.get_user_info()
        self.db.add_user_info(uid=self.u_info.uid, first_name=self.u_info.first_name, last_name=self.u_info.last_name)
        last_msg = None
        msg = self.vkapi.text_msg
        print("user msg: " + msg)

        try:
            last_msg = self.db.get_last_msg()
            self.last_msg_txt = last_msg.text
        except IndexError as e:
            print(e)

        if photo_list is None:
            try:
                if last_msg.have_attach:
                    if msg == wws.send:
                        self.create_pdf()
                        self.strings(False)
                else:
                    self.strings(False)
            except Exception as e:
                print(e)
                self.strings(attach=False)
        else:
            print("massage have attachment")
            try:

                if not last_msg.have_attach:
                    self.strings(True, photo_list)
                SavePhoto(photo_list, message=last_msg, db=self.db)
                self.vkapi.set_ex_pdf_keyboard()
                self.vkapi.send_add_photo_invite()

            except Exception as e:
                print(e)
                self.strings(attach=True, pl=photo_list)
                self.vkapi.set_ex_pdf_keyboard()
                self.vkapi.send_add_photo_invite()


    def create_pdf(self):
        last_msg = self.db.get_last_msg()
        title = self.last_msg_txt or self.vkapi.get_user_info().last_name
        pdf = PDF(msg=last_msg, title=title, db=self.db).create_document()
        self.send_pdf(pdf)

    def send_pdf(self, doc):
        self.vkapi.send_doc(uid=self.vkapi.uid, doc={'file': open(doc.path, 'rb')}, name=doc.name, message="")
        print("pdf send to: " + self.vkapi.get_user_info().last_name)
        for user in self.db.get_linked_user():
            from_str = "От: {} {} ".format(self.u_info.first_name, self.u_info.last_name)
            self.vkapi.send_doc(uid=user.vk_uid, doc={'file': open(doc.path, 'rb')}, name=doc.name, message=from_str)
            print("pdf send to: " + user.last_name)

    def strings(self, attach, pl=None):
        txt = self.vkapi.text_msg or None
        msg = MessageService(self.db).create_message(txt=txt, attach=attach)
        if pl is not None:
            SavePhoto(pl, message=msg, db=self.db)
        if txt is not None:
            messages = self.db.get_message_list()
            if len(messages) >= 2:
                Command(command=messages[-2].text, context=messages[-1].text, api=self.vkapi, db=self.db)
            if len(messages) == 1:
                Command(command="", context=messages[-1].text, api=self.vkapi, db=self.db)
