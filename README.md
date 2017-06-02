# py-nginx
这是我结合nginx+python搭建的一个服务器样例，里面包含一些课程上用到的作业代码。

这个可以算是一个简单的web框架了，搭建这个最初的目的就是希望可以使用python来进行服务端编程

相关的文档参考自：https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-uwsgi-web-server-with-nginx

相关的nginx+python也可以参考我的博客：[基于Nginx搭建Python WSGI应用](http://heaven1881.github.io/2016/05/25/nginx-python/)

## 部署方法
在部署之前，需要确保服务器上安装了`nginx`以及`uwsgi`，你可以自己从网络获取安装方法，也可以参考这篇博客：[基于Nginx搭建Python WSGI应用](http://heaven1881.github.io/2016/05/25/nginx-python/)

克隆代码
```bash
$ cd /git
$ git clone https://github.com/Heaven1881/py-nginx.git
```
在开始前，需要将`py-nginx.conf`和`wsgi.ini`中的配置修改为你的配置，大部分配置都可以使用默认值，只需要修改如下几项：
- `py-nginx.conf`中，将`root /homw/winton/www/py-nginx`指定的目录修改为项目实际的目录
- `wsgi.ini`中，将`chdir  = /home/winton/www/py-nginx`指定的目录修改为项目实际的目录
- 需要保证nginx对上面的目录有读权限

配置nginx
```
$ cd /etc/nginx/cond.d
# ln -s /git/py-nginx/py-nginx.conf
```
> 你也可以直接将`py-nginx.conf`的内容拷贝到nginx配置文件内的对应位置

使用如下命令重启nginx以让服务生效
```
sudo service nginx restart
```

使用如下命令启动服务的方法，可能会提示一些目录不存在，需要手动创建对应目录
```bash
$ uwsgi --py-autoreload=1 --ini wsgi.ini
```
使用如下命令关闭服务器
```
$ kill `cat /tmp/uwsgi/uwsgi_pid.pid`
```

## 主要结构说明
- action文件夹下存放调用的单个py脚本
- 所有脚本的调用配置参照app_setting.json



## 内容说明
### 清华大学SOA课程小作业
使用新浪Oauth协议获取最近用户发布的100条微博，并统计emoji表情个数，判断用户的幸福指数
对应的action文件
- `action/SinaAction.py`

#### 说明
- 使用nginx+uwsgi部署
- 根据新浪用户的授权，获取用户最近的100条微博， 统计里面emoji表情的个数，判断幸福指数
- 幸福指数的定义如下：
 - 定义一系列表情为代表幸福的表情（[发红包啦][抢到啦][偷乐][微笑][嘻嘻][哈哈][可爱][害羞][挤眼][爱你][偷笑][亲亲][太开心][抱抱][馋嘴][色][酷][鼓掌]）
 - 统计这些表情占所有表情的百分比，这个百分比就是幸福指数

### 清华大学成绩统计系统
根据教务默认的格式，上传xlsx文件，统计文件中的信息

### 说明
- 统计xlsx文件里每个课程的分数分布，同时统计所有课程的分数分布
- 借助highChart绘制分布图
