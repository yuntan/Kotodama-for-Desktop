# -*- coding:utf-8 -*-
"""
OAuthライブラリ
"""
__author__ = 'Hayashi'
__date__ = '2014/07/01'

import requests
import time
import random
import hashlib
import hmac
import base64

OAUTH_TOKEN = "oauth_token"
OAUTH_TOKEN_SECRET = "oauth_token_secret"

def get_request_token(consumer_key, consumer_secret,
                      request_token_url, call_back_url):
    """
    認証用URL生成

    :param consumer_key: ConsumerKey
    :param consumer_secret: Consumer_secret
    :param request_token_url: リクエストトークンURL
    :param call_back_url: コールバックURL
    :return: (oauth_token, oauth_token_secret)
    """
    params = {
        "oauth_callback": call_back_url,
        "oauth_consumer_key": consumer_key,
        "oauth_nonce": str(random.getrandbits(64)),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_version": "1.0"
    }
    params_str = '&'.join([requests.utils.quote(key, "") + "=" + requests.utils.quote(params[key], "")
                           for key in sorted(params)])
    message = "GET&" + requests.utils.quote(request_token_url, "") + "&" + requests.utils.quote(params_str, "")
    key = consumer_secret + "&"
    signature = base64.b64encode(hmac.new(key.encode(), message.encode(), hashlib.sha1).digest()).strip()
    url = request_token_url + "?" + params_str + "&oauth_signature=" + requests.utils.quote(signature, "")
    response = requests.get(url)
    data = dict()
    for k_v in response.text.split("&"):
        pair = k_v.split("=")
        data[pair[0]] = pair[1]
    return data


def get_access_token(consumer_key, consumer_secret,
                     request_token, request_token_secret,
                     oauth_verifier, access_token_url):
    params = {
        "oauth_consumer_key": consumer_key,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_nonce": str(random.getrandbits(64)),
        "oauth_version": "1.0",
        "oauth_token": request_token,
        "oauth_verifier": oauth_verifier
    }
    params_str = '&'.join([requests.utils.quote(key, "") + "=" + requests.utils.quote(params[key], "")
                           for key in sorted(params)])
    message = "GET&" + requests.utils.quote(access_token_url, "") + "&" + requests.utils.quote(params_str, "")
    key = consumer_secret + "&" + request_token_secret
    signature = base64.b64encode(hmac.new(key.encode(), message.encode(), hashlib.sha1).digest()).strip()
    headers = {"Authorization": "OAuth"}
    url = access_token_url + "?" + params_str + "&oauth_signature=" + requests.utils.quote(signature, "")
    response = requests.get(url, headers=headers)
    data = dict()
    for k_v in response.text.split("&"):
        pair = k_v.split("=")
        data[pair[0]] = pair[1]
    return data


def api_post(api_url, consumer_key, consumer_secret,
             access_token, access_token_secret, post_data):
    params = {
        "oauth_consumer_key": consumer_key,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_nonce": str(random.getrandbits(64)),
        "oauth_version": "1.0",
        "oauth_token": access_token,
    }
    params.update(post_data)
    params_str = '&'.join([requests.utils.quote(key, "") + "=" + requests.utils.quote(params[key], "")
                           for key in sorted(params)])
    message = "POST&" + requests.utils.quote(api_url, "") + "&" + requests.utils.quote(params_str, "")
    key = consumer_secret + "&" + access_token_secret
    signature = base64.b64encode(hmac.new(key.encode(), message.encode(), hashlib.sha1).digest()).strip()
    params['oauth_signature'] = signature
    for k in post_data:
        del params[k]
    header_params_str = ",".join([(requests.utils.quote(key, "") + "=" + requests.utils.quote(params[key], ""))
                                  for key in sorted(params)])
    headers = {"Authorization": "OAuth " + header_params_str}
    response = requests.post(api_url, headers=headers, data=post_data)
    return response.status_code, response.text


def api_get(api_url, consumer_key, consumer_secret,
            access_token, access_token_secret, get_data):
    params = {
        "oauth_consumer_key": consumer_key,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_nonce": str(random.getrandbits(64)),
        "oauth_version": "1.0",
        "oauth_token": access_token,
    }
    params.update(get_data)
    params_str = '&'.join([requests.utils.quote(key, "") + "=" + requests.utils.quote(params[key], "")
                           for key in sorted(params)])
    message = "GET&" + requests.utils.quote(api_url, "") + "&" + requests.utils.quote(params_str, "")
    key = consumer_secret + "&" + access_token_secret
    signature = base64.b64encode(hmac.new(key.encode(), message.encode(), hashlib.sha1).digest()).strip()
    params['oauth_signature'] = signature
    for k in get_data:
        del params[k]
    header_params_str = ",".join([(requests.utils.quote(key, "") + "=" + requests.utils.quote(params[key], ""))
                                  for key in sorted(params)])
    headers = {"Authorization": "OAuth " + header_params_str}
    response = requests.get(api_url, headers=headers, params=get_data)
    return response.status_code, response.text


def streaming(api_url, consumer_key, consumer_secret,
              access_token, access_token_secret, data, method="GET"):
    params = {
        "oauth_consumer_key": consumer_key,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_nonce": str(random.getrandbits(64)),
        "oauth_version": "1.0",
        "oauth_token": access_token,
    }
    params.update(data)
    params_str = '&'.join([requests.utils.quote(key, "") + "=" + requests.utils.quote(params[key], "")
                           for key in sorted(params)])
    message = "GET&" + requests.utils.quote(api_url, "") + "&" + requests.utils.quote(params_str, "")
    key = consumer_secret + "&" + access_token_secret
    signature = base64.b64encode(hmac.new(key.encode(), message.encode(), hashlib.sha1).digest()).strip()
    params['oauth_signature'] = signature
    for k in data:
        del params[k]
    header_params_str = ",".join([(requests.utils.quote(key, "") + "=" + requests.utils.quote(params[key], ""))
                                  for key in sorted(params)])
    headers = {"Authorization": "OAuth " + header_params_str}
    if method == "GET":
        response = requests.get(api_url, headers=headers, params=data, stream=True)
    else:
        response = requests.post(api_url, headers=headers, data=data, stream=True)
    return response