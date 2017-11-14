python 代理池升级版v1.1

### 概述
前段时间，因为项目的需要，简单的实现了一个代理池，只是实现了预想的基本功能，后边想在完善。可是没想到我太（tai）忙(lan)了(le),之前也有反馈各种bug,一直没有维护,作为一个崇尚开源的超能力者，既然开源了，只要有人在用就应该维护下去，于是花了点时间，有重新做了一下设计，只是没想到,这一拖竟然是7个月之后。

[代理池的1.0版在这](http://www.jianshu.com/p/fd92ca79c9c7) ，这个应该能体现我最初的想法。

最近花了点时间，对项目进行了整体的重构。开源地址见文末。

#### 新特性
说一下这次重构后添加的新特性 ：

- 数据源数量达到8个，一次任务刷新ip总量在2000左右，有效ip（数据库无记录）在500个，刷新时间30分钟。
- 支持文件配置，添加读取配置文件类，采用单例模式实现。
- 对程序中的常量进行抽取，添加了常量文件，减少维护成本。
- 将代理验证和代理刷新进行分离，分别管理。
- 对数据库客户端进行统一管理，加入数据库工厂类，采用工厂模式。
- 通过配置文件调用数据源，类似java中的反射机制，减少模块间的耦合和侵入性。
- 抽离下载工具类，添加user-agent列表，支持随机产生user-agent,下载失败默认重试3次，随机睡眠，3次失败后放弃任务，重试次数可自行配置。
- 添加日志模块。
- 封装创建进程工具类。
- 添加发送邮件模块。
- 提供程序启动的总入口，也可以分模块启动。

### 框架图
![模块设计](http://upload-images.jianshu.io/upload_images/2192701-accb64d9e9373df4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 核心时序图
![核心时序图.png](http://upload-images.jianshu.io/upload_images/2192701-c4b4de6c21f915b4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上面的两幅图，基本上已经体现了代理池的核心逻辑，既然是池，就要有新源的注入，不然就成为一个死池，所以定时任务就是这个新源，网络上的免费ip资源可用性本来就不是很高，交流学习可以用，生产环境就不要想了，因为特别的不稳定。

#### 依赖库
程序默认数据库类型为mongodb ,请确保已经安装该库，并能成功启动。
```
APScheduler==3.3.1
Flask==0.12.1
lxml==3.7.3
requests==2.13.0
pymongo==3.4.0
```
相关的依赖库及版本号已经导入到requirements.txt中，可以使用`(venv) $ pip install -r requirements.txt` 命令安装依赖

#### 使用配置

conf.ini 
```
[db]
#数据库类型
db_type = mongodb
db_host = 127.0.0.1
db_port = 27017

[freeProxy]
firstFreeProxy = firstFreeProxy
secondFreeProxy = secondFreeProxy
thirdFreeProxy = thirdFreeProxy
fourFreeProxy = thirdFreeProxy
fiveFreeProxy = thirdFreeProxy
sixFreeProxy = thirdFreeProxy
sevenFreeProxy = thirdFreeProxy
eightFreeProxy = eightFreeProxy

[WebApi]
port = 5001

[config]
#是否删除原有数据
isDelete = 1
#是否启用邮件通知
isEmail = 1

[WebUrl]
verifyUrl = 'http://www.baidu.com'
```
常量文件 Constants.py
```
'''配置文件键值对'''
db = 'db'
db_type = 'db_type'
db_host = 'db_host'
db_port = 'db_port'
db_name = 'db_name'
freeProxy = "freeProxy"

'''定义数据库类型'''
mongodb = 'mongodb'
redisdb = 'redis'
mysqldb = 'mysql'

'''定义参数常量'''
type = 'type'
name = 'name'
host = 'host'
port = 'port'
clazz = 'getfreeproxy'

'''配置数据库相关信息'''
mongoClient = 'MongoDBClient'
dbName = "IpProxyPool" #数据库名字
commonPool = 'Common_IP'  #ip池总表
validatePool = 'verify_ip' #验证ip表
defaultHost = '127.0.0.1'  #默认本机地址
defaultPort = 27017        #端口默认为mongodb端口

'''Http请求配置'''
retryTime = 3
timeout = 30

'''进程配置'''
processNum = 3 #设置进程的数量
sleepTime = 60*31 #设置验证进程休眠的时间

'''任务下载刷新周期'''
schedulerMinutes = 30 #单位为分钟

'''邮件配置'''
smtp_server = 'smtp.xxx.com'
from_email = 'xxx' #发件人邮件地址
email_password = 'xxx'
to_email = 'xxx' #接收人邮件地址

'''打印日志输出等级配置'''
logLevel = 0  #0代表debug级别(默认) 1 为info 级别
```
若要修改程序的刷新时间，请修改上面的schedulerMinutes值，sleepTime 为数据库为空时的休眠时间。休眠时间应该大于定时刷新时间。默认刷新周期为30分钟，休眠时间为31分钟。关于日志的输出等级设置logLevel的值即可。

采用了约定大于配置的规则，在配置文件和常量文件中关于Key的设置尽量不要改变，以免产生不必要的麻烦，如果要更改数据库的类型，请参考常量文件的定义进行更改。在conf.ini中有一个[config]的配置，此版本没有用到。发送邮件的功能此版本也没有用到，预想是在网站进行改版，提取不到数据的情况下，程序自动发出邮件通知，及时通知开发人员进行提取规则的升级。另外程序只是内置了对mongodb的支持，工厂类实现了redis和mysql的相关代码，但是并没有创建实体类，如果要使用redis或者mysql或者其他的数据库， 请自行修改源码，参考mongodb实现方式。 

#### 新增ip源
关于ip源的增加，只需要修改两个地方，一个是CollectFreeProxy.py,将新增加的源，放入此文件中，第二个是修改conf.ini文件，修改【freeProxy】节点。具体请参考已有的代码。

#### 启动
进入到此程序的根目录IpProxyPool文件夹下， 使用 :
```
python -m Run.Run
```
运行，若是第一次运行，效果图如下：

![初次运行.png](http://upload-images.jianshu.io/upload_images/2192701-0fe182f428309309.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####提取ip
conf.ini ,端口默认为 5000 ， 默认地址为 127.0.0.1/5000 . 会有相关api的介绍。   

#### 封装代理方法：
```
def proxy():
    import json
    response = requests.get('http://xxxx.xxxx.xxxx.xxxx:5001/get/')
    jsonStr = json.loads(response.text)
    proxy = jsonStr['proxy']
    proxy = {
        'http': proxy,
        'https': proxy}
    return proxy
```

#### 地址：

源码地址：https://github.com/topyuluo/IPProxyPool

程序的下载地址：https://github.com/topyuluo/IPProxyPool.git 可下载zip文件。

#### 版本迭代：
- 当前python只支持2.7版，3 版本不支持，迭代过程中会改善
- 当前的代理属性还不完整，只有一个ip地址，迭代中会逐渐的增加属性
- 会增加ip的评分机制，验证代理的活性。根据活性取得分数
- 无效代理的删除，当前的删除机制是不完善的。初步预想的删除是根据时间和评分来删除
- 代理验证进程目前只有一个验证功能，可能会增加删除功能，在验证的过程中如果发现有不符合规则的代理，直接删除掉
- 可用代理池的删除还没有想好该怎么实现，是在api调用的时候进行判断删除，还是启动一个新的进程进行实时规则验证删除，又或者通过api调用删除，还要在想一下。

提供一个API地址：http://47.94.236.225:5001 ，单机，小水管机器，勿压测和频繁请求，谢谢 ！
----------------------------------------------------
    少年听雨歌楼上，红烛昏罗帐。  
    壮年听雨客舟中，江阔云低，断雁叫西风。
    感谢支持！
										     ---起个名忒难
--------------------------------------------------------