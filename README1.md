#### 代理池


最近遇上一个小难题，验证码啊，我虐你千百遍，你待我真是如初恋。 验证码相对比较工整，破解起来也不是很难，难得是你不知道它什么时候出来，总是那么神不知鬼不觉的就出现，后来无意间发现，当我第一次请求的时候数据取到了，既然第一请求没有问题，那么我每次请求都换一个ip 好不好，既然当不了正规军，只能开展游击战了。于是乎这个程序就出现了。一直以来都想做一个代理池，但是一直都没有时间（其实是懒）。不过趁着这个小假期，终于搞出来了，基本实现了设想功能(新手，刚学了2个星期，各位大神轻拍砖 ，代码写得挺烂的 )。

代码已经上传GitHub : https://github.com/topyuluo/IPProxyPool

下面详述：

#### 环境

windows(64) + python 2.7 + MongoDB + phantomjs + selenium + requests  

#### 设计思想

- 采集 ：周期性的从网络上采集免费的ip, 放入数据库中并启动10个进程，进行验证 ，验证成功单独存放。
- 使用： 初步想了两种方式，一种是做成服务，提供api 接口，一种是直连数据库。 

##### 设计

ip代理池程序由四部分组成：

- Schedule : 执行定时任务，每10分钟请求一下ip数据源，并验证ip可用性
- db : 存储数据，数据从网络上取下来，必定要找一个地方存储，也好维护
- collectproxy ： ip数据源， 由快代理，代理66 ，有代理， 西刺代理，代理360 组成。可扩展
- utils :  工具函数(Http请求 ，验证函数)。
- webservice: 提供外部访问接口。

#### 框架图
![框架.png](http://upload-images.jianshu.io/upload_images/2192701-dc01e1e1c4548076.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 流程概述

启动Schedule, 由Scheduler调用collectProxy,去请求网络资源，collectProxy拿到数据后解析，并将解析好的数据返回给scheduler,数据入库，sheduler 验证数据库中已经存在的proxy, 验证成功，放入新表中。 此为周期性任务。
需要接入代理的爬虫，通过访问数据库或者api接口拿代理，如果此时可用代理数量不足，调用下载程序去网络采集新的数据。如果爬虫通过proxy没有成功请求到数据，此ip废弃，从验证成功库中删除，并请求一个新的proxy。考虑了一下，可能做成API的方式扩展性更好一些，直接调用网址就可以了，通用性更强。 

#### 项目目录

![目录.png](http://upload-images.jianshu.io/upload_images/2192701-91f30cc2a1b8ee77.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##### 目录接口说明
- ProxyRefreshSchedule : 调度任务，周期性执行数据源刷新，代理验证，并入库操作。
- CollectFreeProxy:封装网络数据源，调用工具函数下载接口，解析数据，将数据传给任务调度器。
- MongoDBClient : 数据库操作类，封装了，查询，删除，保存等接口
-UtilsFunction :工具函数，数据下载接口，ip验证接口。
-Api : 数据服务接口，封装返回单个proxy,返回多个proxy,查询数据总量等接口

##### 程序效果

调度任务执行效果：

![调度任务运行效果.png](http://upload-images.jianshu.io/upload_images/2192701-aac5453137d9aab7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**数据库截图**

*所有ip库 *

![Paste_Image.png](http://upload-images.jianshu.io/upload_images/2192701-314fa54ae9a00ecc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

*已验证ip库*

![Paste_Image.png](http://upload-images.jianshu.io/upload_images/2192701-62a4026099ba57da.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**api截图**

![Paste_Image.png](http://upload-images.jianshu.io/upload_images/2192701-97b34477496ab505.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用说明：
- 先运行ProxyRefreshSchedule ，等待10 分钟，设定的周期就是10分钟，感觉不合适可以自己修改。之后控制台会打印下载链接和已经验证成功的proxy。
- 运行 api.py 。
- 打开浏览器，输入http://127.0.0.1:5000 。可以查看接口的api。



参考：https://github.com/jhao104/proxy_pool