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
        对参数进行检查并返回
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
        对列表行参数进行检查
        required的数值表示最小列表长度
        '''
        valuelist = self.data.getlist(key)
        if len(valuelist) < required:
            raise Exception('parameter list \'%s\'s size require to be more than %d, but %d given' % (
                key, required, len(valuelist)
            ))
        elif len(valuelist) == 0:
            return default
        else:
            return valuelist

    def setHeader(self, header):
        self.response_header.update(header)

    def setStatus(self, status):
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
