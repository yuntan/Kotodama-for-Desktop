# -*- coding:utf-8 -*-
"""
DAO
このアプリケーションではデータを連想配列形式で保存することとする
"""

__author__ = 'Ryosuke'
__date__ = '2014/07/22'

from core import config
import json


class DAO(object):
    """
    指定された名前のJsonファイルを読み込み、書き込みする
    """
    data = None
    _name = None
    def __init__(self, name):
        self._name = name
        self._load_json()

    def _load_json(self):
        """
        プライベートメソッド
        Jsonデータを読み込む、指定Jsonファイルが存在しなかった場合、空の辞書を生成する
        :return:
        """
        try:
            fp = open(config.APPLICATION_PATH + "/data/" + self._name)
            self.data = json.load(fp)
            fp.close()
        except FileNotFoundError:
            self.data = dict()

    def save_data(self):
        """
        辞書データをJson形式で保存する
        :return: 成功時はTrue, 失敗時はFalse
        """
        try:
            fp = open(config.APPLICATION_PATH + "/data/" + self._name, mode='w')
            json.dump(self.data, fp)
            fp.close()
            return True
        except IOError:
            return False