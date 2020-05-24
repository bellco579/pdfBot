import json

import requests

from vkapi.models import UserInfo


def getPhotoUrl():
    return


def getMessageById(id):
    pass


def get_user(uid, api, token):
    vk_user = api.users.get(access_token=token, user_ids=uid)[0]
    return UserInfo(
        first_name=vk_user["first_name"],
        last_name=vk_user['last_name'],
        uid=uid
    )


def upload_file(api, token, file, title):
    maratik = 313941939
    upload_url = api.docs.getMessagesUploadServer(access_token=token, type='doc', peer_id=maratik)['upload_url']

    response = requests.post(upload_url, files=file)
    result = json.loads(response.content)
    file = result['file']

    json1 = api.docs.save(access_token=token, file=file, title=title, tags=[])[0]

    owner_id = json1['owner_id']
    photo_id = json1['id']
    attach = 'doc' + str(owner_id) + '_' + str(photo_id)
    return attach
