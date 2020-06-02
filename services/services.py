import threading

from core.models import Message
from services.converter import photo_converter
from services.db import dbInterface
from services.repositories import save_photo


class MessageService:
    def __init__(self, db: dbInterface, txt=None, attach=None, is_created=False):
        self.db = db

    def parce_message(self, last_msg):
        self.message = last_msg

    def create_message(self, txt, attach):
        return self.db.create_message(txt, attach)

    def add_photo(self, path):
        self.db.add_photo_path(path=path, message=self.message)


class SavePhoto:
    def __init__(self, photo_url_list: list, db: dbInterface, message):
        self.photoUrl = photo_url_list
        self.msg = message
        self.db = db
        for url in self.photoUrl:
            # x = threading.Thread(target=self.photo_save, args=(url,))
            # x.start()
            self.photo_save(url)

    def photo_save(self, url):
        path = save_photo(url=url)
        self.db.add_photo_path(path=path, message=self.msg)
        print("saved photo: " + url)


class PDF:
    def __init__(self, title, db: dbInterface, msg: Message):
        self.db = db
        self.msg = msg
        self.title = title

    def create_document(self):
        urls = self.get_urls()
        urls.reverse()
        doc_path = photo_converter(urls)
        print("Doc path: " + doc_path)
        doc = self.db.create_doc(title=self.title, doc_path=doc_path)
        return doc

    def get_urls(self):
        return list(photo.path for photo in self.msg.photo_set.all())
