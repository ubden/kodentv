# -*- coding: utf-8 -*-
import requests
import json
# from tikimeta.utils import logger

API_ENDPOINT = "https://api-v2launch.trakt.tv"
CLIENT_ID = "46a691933d7cf646fd73ce846a44d1951b7a2d28304a370b4ebd4c06bab83f63"
CLIENT_SECRET = "f0145ebe05107a6655edfd581aca11d632f97a04e0896e5da843310153b82ffd"

def traktGetIDs(db_type, id_type, media_id):
    from tikimeta.metacache import cache_function
    if '_id' in id_type:
        id_type = id_type.split('_id')[0]
    string = "%s_%s_%s_%s" % ('traktGetIDs', db_type, id_type, str(media_id))
    url = "/search/%s/%s?type=%s" % (id_type, media_id, db_type)
    response = cache_function(getTrakt, string, url, 168)
    response = response[0].get(db_type, {}).get('ids', [])
    return response

def getTrakt(path):
    headers = {'Content-Type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': CLIENT_ID}
    return requests.get("{0}/{1}".format(API_ENDPOINT, path), headers=headers, timeout=10)
