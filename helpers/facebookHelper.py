__author__ = 'bartoszcwynar'
import httplib2
import json
from mooderServer.settings import FACEBOOK_CLIENT_APPID

def validateUserByToken(third_party_token):
    return True
    h = httplib2.Http()
    body = '?access_token=' + third_party_token
    resp, content = h.request("https://graph.facebook.com/app" + body, method="GET", body=body)
    print content
    return json.loads(content)["id"] == FACEBOOK_CLIENT_APPID
