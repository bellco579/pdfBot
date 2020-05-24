from services.model import dataModel
from core.models import Docs, Message
from user.models import Profile


class dbInterface:
    def __init__(self, uid: str):
        self.uid = uid

    def get_user(self, uid=None):
        if uid is None:
            uid = self.uid
        return Profile.objects.get_or_create(vk_uid=uid)[0]

    def add_user_info(self, first_name: str, last_name: str, uid: int):
        return Profile.objects.get_or_create(vk_uid=uid, first_name=first_name, last_name=last_name)

    def create_message(self, message="", attach=False):
        Message.objects.create(sender=self.get_user(), text=message, have_attach=attach)

    def create_doc(self, doc_path, title):
        Docs.objects.create(owner=self.get_user(), name=title, path=doc_path)

    def get_last_doc(self):
        user = self.get_user()
        qset = Docs.objects.filter(owner=user)
        doc = list(doc for doc in qset)[-1]
        return doc

    def get_last_msg(self):
        msg = self.get_message_list()
        return msg[0]

    def get_message_list(self):
        return Message.objects.all()

    def get_linked_user(self):
        return self.get_user().linked_users.all()

    def add_linked_user(self, user_info):
        user = self.add_user_info(first_name=user_info.first_name, last_name=user_info.last_name, uid=user_info.uid)[0]
        lu = self.get_user()
        lu.linked_users.add(user)
        lu.save()
        return user

    def del_linked_user(self, position: int):
        user = self.get_linked_user()[position]
        lu = self.get_user()
        lu.linked_users.remove(user)
        lu.save()
        return user
