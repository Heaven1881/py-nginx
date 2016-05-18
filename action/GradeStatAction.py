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
    def run(self):
        # 如果type是gradestat，则统计结果
        processType = self.checkValue('type', default=None)
        # hasTilte 表示 xlsx 的第一行是标题
        hasTitle = self.checkValue('hasTitle', default=None)
        # 获取上传的文件内容
        fileContent = self.checkValue('xlsxFile', required=True)

        book = xlrd.open_workbook(file_contents=fileContent)
        sheet = book.sheet_by_index(0)

        content = [sheet.row_values(i) for i in range(sheet.nrows)]
        # 处理第一行的标题
        if hasTitle:
            content = {'title': content[0], 'content': content[1:]}
        else:
            content = {'content': content}

        if processType == 'gradestat':
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

        self.setHeader({'Content-Type': 'application/json'})
        return json.dumps(content)
