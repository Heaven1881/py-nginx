# coding:utf8
# author:winton

import urllib
import re
import httplib
import urllib2
import json
from BaseAction import BaseAction

# config for soa
config = {
    'client_id': '4213853954',
    'client_secret': 'cc398ffbcb0eef98da563a90acbf89d8',
    'redirect_uri': 'http://139.129.32.184:8081/app/weibo/postcode',
    'authorize_url': 'https://api.weibo.com/oauth2/authorize',
    # 'get_access_token_url': 'https://api.weibo.com/oauth2/access_token',
    'get_user_timeline_url': 'https://api.weibo.com/2/statuses/user_timeline.json',
    'lastest_num': 100,
}


class WeiboOauthAction(BaseAction):
    '''
    处理用户的请求，将其引导至新浪授权页面
    '''
    name = 'WeiboOauthAction'

    def run(self):
        # 重定向到授权页面
        authorizeUrl = config['authorize_url']
        encodedArgs = urllib.urlencode({
            'client_id': config['client_id'],
            'response_type': 'code',
            'redirect_uri': config['redirect_uri']
        })
        url = authorizeUrl + '?' + encodedArgs
        self.logging('redirect url=%s' % url)

        self.setHeader({'Location': url})
        self.setStatus('301 Moved Permanently')
        return ''


class WeiboPostcodeAction(BaseAction):
    '''
    处理新浪的回调并获取用户的信息
    '''
    name = 'WeiboPostcodeAction'

    def run(self):
        code = self.checkValue('code', required=True)
        # 获取access info
        encodedArgs = urllib.urlencode({
            'client_id': config['client_id'],
            'client_secret': config['client_secret'],
            'grant_type': 'authorization_code',
            'redirect_uri': config['redirect_uri'],
            'code': code,
        })
        self.logging(encodedArgs)
        conn = httplib.HTTPSConnection('api.weibo.com')
        conn.request("POST", '/oauth2/access_token' + '?' + encodedArgs)
        response = conn.getresponse()
        jsonStr = response.read()
        accessInfo = json.loads(jsonStr)
        lastestTexts = self.getLastWeibo(accessInfo, length=config['lastest_num'])
        emojis = self.statEmoji(lastestTexts)

        return '\n'.join(lastestTexts + ['\n'] + emojis)

    def statEmoji(self, testlist):
        emojiList = []
        for text in testlist:
            emojis = re.findall('\[[^\[\]]+\]', text)
            emojiList += emojis

        # 统计列表中的表情信息
        happinessEmo = [
            '[发红包啦]',
            '[抢到啦]',
            '[偷乐]',
            '[微笑]',
            '[嘻嘻]',
            '[哈哈]',
            '[可爱]',
            '[害羞]',
            '[挤眼]',
            '[爱你]',
            '[偷笑]',
            '[亲亲]',
            '[太开心]',
            '[抱抱]',
            '[馋嘴]',
            '[色]',
            '[酷]',
            '[鼓掌]'
        ]
        print 'DEBUG', ','.join([e for e in happinessEmo])
        statedlist = []
        stattext = []
        happinessCount = 0
        for emoji in emojiList:
            if emoji not in statedlist:
                stattext += ['%s: %s' % (emoji, emojiList.count(emoji))]
                statedlist += [emoji]
                if emoji in happinessEmo:
                    happinessCount += emojiList.count(emoji)
        stattext += ['\n', '幸福表情(%s)\n总数: %d 占%d%%' % (','.join([e for e in happinessEmo]), happinessCount, happinessCount*100.0/len(emojiList))]
        return stattext

    def getLastWeibo(self, accessInfo, maxId=0, length=5):
        if length <= 0:
            return []
        encodedArgs = urllib.urlencode({
            'access_token': accessInfo['access_token'],
            'uid': accessInfo['uid'],
            'max_id': maxId,
        })
        print 'DEBUG', 'get last weibo', encodedArgs
        response = urllib2.urlopen(config['get_user_timeline_url'] + '?' + encodedArgs)
        jsonStr = response.read()
        timeline = json.loads(jsonStr)
        texts = [status['text'].encode('utf-8') for status in timeline['statuses']]
        print '\n'.join(texts)
        if len(texts) < length and len(texts) != 0:
            texts += self.getLastWeibo(accessInfo, timeline['statuses'][-1]['id'], length - len(texts))[1:]
        return texts
