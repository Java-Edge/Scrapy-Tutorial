# Python分布式爬虫打造搜索引擎
未来是什么时代？是数据时代！数据分析服务、互联网金融，数据建模、自然语言处理、医疗病例分析……越来越多的工作会基于数据来做，而爬虫正是快速获取数据最重要的方式，相比其它语言，Python爬虫更简单、高效

#### 单机爬虫（Scrapy）到分布式爬虫（Scrapy-Redis）的完美实战

### 说真的，你再也没有理由学不会爬虫了

![](https://upload-images.jianshu.io/upload_images/16782311-555251c239b2848a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

从0讲解爬虫基本原理，对爬虫中所需要用到的知识点进行梳理，从搭建开发环境、设计数据库开始，通过爬取三个知名网站的真实数据，带你由浅入深的掌握Scrapy原理、各模块使用、组件开发，Scrapy的进阶开发以及反爬虫的策略

彻底掌握Scrapy之后，带你基于Scrapy、Redis、elasticsearch和django打造一个完整的搜索引擎网站

![](https://upload-images.jianshu.io/upload_images/16782311-15fcfcb29a5f9315.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 我们的目标：分布式爬虫Scrapy-Redis搭建搜索引擎

![](https://upload-images.jianshu.io/upload_images/16782311-9cee9a6dc4a8834b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 由浅入深掌握Scrapy
## 爬虫开发环境搭建及基础知识
#### 基于Mac OS
整个开发过程中还会讲到很多爬虫开发的知识， 这些知识不管是对Web系统的理解还是面试都是非常重要的知识点，包括正则表达式、url去重的策略、深度优先和广度优先遍历算法及实现、session和cookie的区别以及如何通过多种方式去实现模拟登录

## Scrapy爬虫搭建及单机爬虫实战案例
### 爬取技术社区文章
掌握：xpath， css选择器 / items设计 / pipeline，twisted保存数据到mysql
### 爬取问答网站
掌握：session和cookie原理 / scrapy FormRequest和requests模拟知乎登录 item loader方式提取数据
### 爬取招聘网站
掌握：link extractor  / Scrapy Rule提取url  / CrawlSpider爬取全站

# Scrapy进阶
## 突破反爬机制
Scrapy原理

ip代理 、user-agent随机切换

云打码实现验证码识别

## Scrapy进阶
selenium和phantomjs动态网站爬取

Scrapy telnet、Web service

Scrapy信号和核心api

## Scrapy-Redis分布式爬虫
Redis

Scrapy-Redis源码分析

Redis-bloomfilter集成到Scrapy-Redis

# 搭建搜索引擎
- 数据解析和入库

- Scrapy-Redis分布式爬虫开发

- 数据保存到elasticsearch

- 通过django搭建搜索引擎

# 环境参数
- 技术语言 
python3.5 

- 框架 
scrapy1.3 elasticsearch5 

- 框架 
django1.11 redis 

- 开发系统
mac 

- 数据库 
mysql5.7 redis 

- IDE 
pycharm 

- 工具 
virtualenv navicat