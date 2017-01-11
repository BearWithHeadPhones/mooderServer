__author__ = 'bartoszcwynar'
import httplib2
import json
from mooderServer.settings import FACEBOOK_CLIENT_APPID

def validateUserByToken(third_party_token):
    h = httplib2.Http()
    body = '?access_token=' + third_party_token
    resp, content = h.request("https://graph.facebook.com/app" + body, method="GET", body=body)
    print content
    return json.loads(content)["id"] == FACEBOOK_CLIENT_APPID


def getUsersFriends(third_party_token, userid):
    h = httplib2.Http()
    print "SIEMAHCAAAAAAAA"
    print userid
    body = str(userid) + "/friends?access_token=" + third_party_token
    resp, content = h.request("https://graph.facebook.com/" + body, method="GET", body=body)
    print content
    return json.loads(content)["data"]