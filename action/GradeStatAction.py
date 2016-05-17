# coding:utf8
# author:winton

import cgi
import json
import xlrd

from BaseAction import BaseAction


class ParseXlsxAction(BaseAction):
    '''
    功能：将用户上传的xlsx文件解析为json数据返回
    '''
    def run(self, env, data):
        uploadData = cgi.FieldStorage(environ=env, fp=env['wsgi.input'])

        # 如果type是gradestat，则统计结果
        stat = True if data.get('type', [None])[0] == 'gradestat' else False
        # hasTilte 表示 xlsx 的第一行是标题
        hasTitle = True if data.get('hasTitle', ['false'])[0] == 'true' else False

        if not uploadData:
            raise Exception('Upload xlsx file is no found')

        if 'xlsxFile' in uploadData and uploadData['xlsxFile'].filename != '':
            fileContent = uploadData['xlsxFile'].file.read()
            book = xlrd.open_workbook(file_contents=fileContent)
            sheet = book.sheet_by_index(0)

            content = [sheet.row_values(i) for i in range(sheet.nrows)]
            # 处理第一行的标题
            if hasTitle:
                content = {'title': content[0], 'content': content[1:]}
            else:
                content = {'content': content}

            if stat:
                # 统计每个课程的分数
                statObj = {}
                for row in content['content']:
                    if str(row[2]) not in statObj:
                        statObj[str(row[2])] = {
                            'name': row[3],
                            'grade': [x[4] for x in content['content'] if x[2] == row[2]]
                        }
                # 统计所有课程的分数
                statObj['all'] = {
                    'name': '==所有课程==',
                    'grade': [x[4] for x in content['content']]
                }
                content['stat'] = statObj

            body = json.dumps(content)
            header = []
            status = '200 OK'
            return body, header, status
        else:
            raise Exception(' \'xlsxFile\' is reqried')
