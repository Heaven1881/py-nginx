# coding:utf8
# author:winton

import json
from BaseAction import BaseAction


class SimpleAction(BaseAction):
    '''
    测试用action
    测试获取POST和GET数据
    '''
    def run(self):
        self.setHeader(('Content-Type', 'application/json'))
        # 检查get数据
        firstGet = self.checkValue('get', required=True)
        firstGetOptional = self.checkValue('get-optional', default='get-optional not given')
        firstPost = self.checkValue('post', required=True)
        listPost = self.checkList('list', required=2)
        return json.dumps({
            'err': 0,
            'res': {
                'first_get': firstGet,
                'first_get_optional': firstGetOptional,
                'first_post': firstPost,
                'listPost': listPost
            }
        })
