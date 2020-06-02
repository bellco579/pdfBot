class Photo:
    def get_url(self, item):
        phtoUrl = ""
        try:
            photoUrl = item['photo']["sizes"][0]['url']
        except:
            try:
                photoUrl = item['photo']['photo_1280']
                print("hight quality")
            except:
                try:
                    photoUrl = item['photo']['photo_807']
                    print("meddle quality")
                except:
                    photoUrl = item['photo']['photo_604']
                    print("low quality")

        return photoUrl

    def get_photo_url(self, attachments):
        photo_urls = []

        for item in attachments:
            if item['type'] == 'photo':
                url = self.get_url(item)
                photo_urls.append(url)
        if len(photo_urls) == 0:
            return None
        return photo_urls
