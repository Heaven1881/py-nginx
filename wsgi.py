# coding:utf8
# auther:winton

import json
import datetime
import codecs


class AppHandler:
    '''
    负责处理并分发请求
    '''
    def __init__(self, filename):
        app_setting = self._loadJson(filename)
        self.actions = app_setting['actions']

    def _loadJson(self, filename):
        '''
        读取json文件，返回json obj
        '''
        f = codecs.open(filename, encoding='utf-8')
        return json.loads(f.read())

    def _loadAction(self, actionStr):
        '''
        动态读取对应模块
        '''
        moduleName, className = actionStr.split(':')
        module = __import__(moduleName, fromlist=[className])
        actionClass = getattr(module, className)
        return actionClass

    @staticmethod
    def logging(msg, tag=''):
        logline = '%(datetime)s %(tag)s - %(msg)s' % {
            'datetime': datetime.datetime.now(),
            'tag': tag,
            'msg': msg
        }
        print logline

    def _loadMapAction(self, env):
        '''
        获取和请求相匹配的action
        '''
        path = env['PATH_INFO']
        method = env['REQUEST_METHOD']
        mapActions = [act['action'] for act in self.actions if path in act['path'] and method in act['method']]
        AppHandler.logging('map action %s' % mapActions)
        if len(mapActions) >= 1:
            actionClass = self._loadAction(mapActions[0])
        else:
            AppHandler.logging('Cannot found action for request [path=%s] [method=%s]' % (path, method))
            actionClass = None
        return actionClass

    def handleRequest(self, env, start_response):
        '''
        处理请求
          1. 获取匹配模块
          2. 调用模块
          3. 返回数据
        '''
        actionClass = self._loadMapAction(env)
        actionIns = actionClass(env, start_response, AppHandler.logging)
        return actionIns.handle()


def application(env, start_response):
    configFilename = 'app_settings.json'
    handler = AppHandler(configFilename)
    return handler.handleRequest(env, start_response)
