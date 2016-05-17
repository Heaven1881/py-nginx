# coding:utf8
# auther:winton

import json
import codecs
import urlparse
import traceback


def loadJsonFile(jsonFile):
    try:
        f = codecs.open(jsonFile, encoding='utf-8')
    except:
        raise Exception('error while loading app_setting.json')
    return json.loads(f.read())


def loadAndRun(actionStr, env, data):
    moduleName, className = actionStr.split(':')
    module = __import__(moduleName, fromlist=[className])
    actionClass = getattr(module, className)
    action = actionClass()
    return action.handle(env, data)


def application(env, start_response):
    try:
        path = env['PATH_INFO']
        method = env['REQUEST_METHOD']
        data = urlparse.parse_qs(env['QUERY_STRING'])

        appSettings = loadJsonFile('app_settings.json')
        actions = appSettings['actions']
        found = False
        for act in actions:
            if path == act['path'] and method == act['method']:
                response_body, response_header, response_status = loadAndRun(act['action'], env, data)
                found = True
                break
        if not found:
            raise Exception('Can not found action [path=%s] [method=%s]' % (path, method))
    except Exception as e:
        traceback.print_exc()
        response_body, response_header, response_status = (json.dumps({
            'res': 1,
            'desc': '%s' % e
        }), [], '500 Internal Server Error')

    response_header += [
        ('Content-Length', str(len(response_body)))
    ]
    start_response(response_status, response_header)
    return [response_body]
