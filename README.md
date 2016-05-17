# py-nginx
这是我结合nginx+python搭建的一个服务器样例，里面包含一些课程上用到的作业代码。

这个可以算是一个简单的web框架了，搭建这个最初的目的就是希望可以使用python来进行服务端编程

相关的文档参考自：https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-uwsgi-web-server-with-nginx


### 清华大学SOA课程的一次小作业，使用新浪Oauth协议获取最近用户发布的100条微博，并统计emoji表情个数，判断用户的幸福指数
## 说明
- 使用nginx+uwsgi部署
- 根据新浪用户的授权，获取用户最近的100条微博， 统计里面emoji表情的个数，判断幸福指数
- 幸福指数的定义如下：
 - 定义一系列表情为代表幸福的表情（[发红包啦][抢到啦][偷乐][微笑][嘻嘻][哈哈][可爱][害羞][挤眼][爱你][偷笑][亲亲][太开心][抱抱][馋嘴][色][酷][鼓掌]）
 - 统计这些表情占所有表情的百分比，这个百分比就是幸福指数
