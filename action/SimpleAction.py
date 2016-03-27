# coding:utf8
# author:winton

from BaseAction import BaseAction


class SimpleAction(BaseAction):
    def run(self, env, data):
        body = '哈哈哈'
        header = []
        status = None
        return body, header, status
