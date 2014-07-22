# -*- coding:utf-8 -*-
"""

"""

__author__ = 'Ryosuke'
__date__ = '2014/07/20'


class Account(object):
    name = None
    screen_name = None
    user_id = None
    oauth_token = None
    oauth_token_secret = None
    follows = list()
    followers = list()

    def __init__(self, d):
        self.name = d.get("name")
        self.screen_name = d.get("screen_name")
        self.user_id = d.get("user_id")
        self.oauth_token = d.get("oauth_token")
        self.oauth_token_secret = d.get("oauth_token_secret")
        self.follows = d.get("follows", list())
        self.followers = d.get("followers", list())

    def to_dict(self):
        d = list()
        if self.name is not None:
            d["name"] = self.name
        if self.screen_name is not None:
            d["screen_name"] = self.screen_name
        if self.user_id is not None:
            d["user_id"] = self.user_id
        if self.oauth_token is not None:
            d["oauth_token"] = self.oauth_token
        if self.oauth_token_secret is not None:
            d["oauth_token_secret"] = self.oauth_token_secret
        d["follows"] = self.follows
        d["followers"] = self.followers

    def get_follows_and_followers(self):
        pass

    def get_name_and_screen_name(self):
        pass

    def tweet(self, text):
        pass

    def favorite(self, status_id):
        pass

    def retweet(self, status_id):
        pass