# coding:utf8
# author:winton

import cgi
import json
import traceback


class BaseAction:
    tag = 'BaseAction'

    def __init__(self, env, start_response, logging):
        self.env = env
        self.start_response = start_response
        self.logging = logging
        self.data = cgi.FieldStorage(
            fp=env['wsgi.input'],
            environ=env,
            keep_blank_values=True
        )

        self.response_header = {}
        self.response_status = '200 OK'

    def checkValue(self, key, required=False, default=None):
        '''
        对参数进行检查并返回，以key为键值寻找对应的参数
        寻找的位置包括:
            - url中的参数
            - 使用post方法时的参数，支持的Content-Type包括form-data和x-www-form-urlencoded
        函数只会反对对应的值，如果key对应的值是一个列表，则只会返回列表的第一个元素
        key         参数的索引字段
        required    如果为True，则会在key对应的value不存在时抛出异常
        default     key对应的value不存在时，返回的默认值，如果required=True，参数将被忽略
        '''
        value = self.data.getfirst(key)
        if required and value is None:
            raise Exception('parameter \'%s\' is required' % key)
        elif value is None:
            return default
        else:
            return value

    def checkList(self, key, required=0, default=[]):
        '''
        对参数进行检查并返回，以key为键值寻找对应的参数
        寻找的位置包括:
            - url中的参数
            - 使用post方法时的参数，支持的Content-Type包括form-data和x-www-form-urlencoded
        该函数默认只会返回列表，如果key对应的字段只有一个元素，则会返回包含这一个元素的列表
        key         参数的索引字段
        required    一个大于等于0的数字，如果获取到的参数列表的长度小于required，则抛出异常
        default     key对应的值不存在时返回的默认值，如果指定了required>0，该参数将被忽略
        '''
        valuelist = self.data.getlist(key)
        if len(valuelist) < required:
            raise Exception('parameter \'%s\'has length %d, but %d required ' % (
                key, len(valuelist), required
            ))
        elif len(valuelist) == 0:
            return default
        else:
            return valuelist

    def setHeader(self, header):
        '''
        设置对应的header, 支持同时设置多对 key-value值
        '''
        self.response_header.update(header)

    def setStatus(self, status):
        '''
        设置返回的状态描述,例如
        200 OK
        '''
        self.response_status = str(status)

    def logging(self, msg, tag=None):
        tag = self.tag if tag is None else tag
        self.logging(msg, tag)

    def handle(self):
        try:
            response_body = self.run()
        except Exception as e:
            self.logging(e)
            traceback.print_exc()
            response_body = json.dumps({
                'err': 1,
                'res': str(e)
            })
        self.setHeader({'Content-Length': str(len(response_body))})
        self.start_response(self.response_status, self.response_header.items())
        return [response_body]
