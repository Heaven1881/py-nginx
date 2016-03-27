# coding:utf8
# author:winton


class BaseAction:
    def handle(self, env, data):
        body, header, status = self.run(env, data)
        response_body = body or ''
        response_header = header or []
        response_status = status or '200 OK'
        return (response_body, response_header, response_status)
