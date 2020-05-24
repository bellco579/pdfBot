from services.converter import photo_converter, add_photo_to_file
from services.db import dbInterface
from services.work_with_str import Command
from vkapi.main import Main


class Vk:
    def __init__(self, rq):
        self.vkapi = Main(rq)
        self.db = dbInterface(self.vkapi.uid)
        self.photo_list = self.vkapi.get_photos_url()
        self.u_info = self.vkapi.get_user_info()
        self.db.add_user_info(uid=self.u_info.uid, first_name=self.u_info.first_name, last_name=self.u_info.last_name)

        if self.photo_list is None:
            self.strings(False)
        else:
            self.strings(True)
            self.create_pdf()

    def create_pdf(self):
        self.vkapi.set_ex_pdf_keyboard()
        self.vkapi.send_message("добавить фото в pdf?")
        title = self.vkapi.text_msg or self.vkapi.get_user_info().last_name
        doc_path = photo_converter(self.photo_list)
        try:
            last_msg = list(msg for msg in self.db.get_message_list())[-2]
            if last_msg.have_attach:
                last_doc = self.db.get_last_doc()
                path = add_photo_to_file(last_doc.path, doc_path)
                last_doc.path = path
                last_doc.save()
            else:
                self.db.create_doc(title=title, doc_path=doc_path)
        except Exception as e:
            print(e)
            self.db.create_doc(title=title, doc_path=doc_path)

    def strings(self, attach):
        txt = self.vkapi.text_msg or None
        self.db.create_message(txt, attach)
        if txt is not None:
            messages = list(msg for msg in self.db.get_message_list())
            if len(messages) >= 2:
                Command(command=messages[-2].text, context=messages[-1].text, api=self.vkapi, db=self.db)
            if len(messages) == 1:
                Command(command="", context=messages[-1].text, api=self.vkapi, db=self.db)
