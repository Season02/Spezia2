# Spezia2
泛用爬虫项目
    
 ## Prerequirement
 ### Database
Table scraping_target    
```
id varchar(255) [ID]    
type varchar(255) [Type]
```    
Table news    
```
identifier varchar(255) [weibo id]    
identifier_re varchar(255) [weibo replay id]
```


 ## Examples
- Wechat    
```
type: wechat    
key: 广电时评           
extra0: https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzI ... webview_type=1  
```  


- Newrank    
```
type: newrank    
key: 广电时评    
extra0: 70894E6FD22DD7A0FA92C5C26CA6A9DD
```


- Weibo    
```
type: weibo    
key: 人民网    
extra0: http://m.weibo.cn/u/2286908003?uid=22 ... aturecode=20000180
```    


- UlWeb    
 ##### Just one page     
```
type: ulweb    
key: 新华网_电影    
extra0: http://ent.news.cn/dy.htm    
extra1: null    
extra2: null    
extra3: (div,[class:con])    
extra4: (li,[class:clearfix])    
extra5: link:a href()=;title:a;img:img data-original()=;date:span    
extra6: title**:title;date:span class=h-time;content**:div id=p-detail;author**:span class=tiyi1
```    
 ##### Multi-pages    
```
type: ulweb    
key: 人民网娱乐频道_文化    
extra0: http://culture.people.com.cn/GB/27296/index.html    
extra1: http://culture.people.com.cn/GB/27296/index2.html    
extra2: http://culture.people.com.cn/GB/27296/index3.html    
extra3: (div,[class:ej_list_box clear])    
extra4: (li,[])    
extra5: link:a href(http://ent.people.com.cn)=;title:a;date:em    
extra6: date:meta content()= name=publishdate;title:h1:div class=clearfix w1000_320 text_title;author:div class=edit clearfix;content**:div class=box_con
```        


- JsWeb    
```
type: jsweb    
key: 网易娱乐_电影    
extra0: http://ent.163.com/special/000381Q1/newsdata_movieidx.js?callback=data_callback    
extra1: http://ent.163.com/special/000381Q1/newsdata_movieidx_02.js?callback=data_callback    
extra2: http://ent.163.com/special/000381Q1/newsdata_movieidx_03.js?callback=data_callback    
extra3: data_callback( )    
extra4: null    
extra5: label:label;title:title;data:time;img:imgurl;keys:*loop keywords->keyname;link:docurl    
extra6: date**:div class=post_time_source;title:h1:div class=post_content_main;content**:div id=endText
```


 ## Directions of use    
 ### Common        
- id: id
- type: ulweb,jsweb,newrank,weibo,wechat,five
- key: kind of direction    
- last_access_date: last access date
- frequency: how many hours per cycle    
- valid: enable(1) disable(0)    
- title: don`t care    
- location_id: area id    
- order_code: order code

 ### Wechat
type: wechat

 ### Weibo
type: weibo

 ### UlWeb
type: ulweb    
extra0: url of first page    
extra1: url of second page(if exist)    
extra2: url of third page(if exist)    
extra3: rule of list container    
    - (div,[class:con])
extra4: rule or list    
    - (li,[class:clearfix])
extra5: rule of list item    
    - link:a href()=;title:a;img:img data-original()=;date:span    
 ##### Example        
      
a list item are(from [wenyi.gmw.cn](http://wenyi.gmw.cn/node_84179.htm)):


source code of it are:


then the ruler will be:
```
link:a href(http://wenyi.gmw.cn/)=;title**:a;date:span class=channel-newsTime
```

extra6: rule of page    
    - title**:title;date:span class=h-time;content**:div id=p-detail;author**:span class=tiyi1


 ### JsWeb
type: jsweb    

extra0,extra1,extra2: request address of 1,2,3 pages

extra3: extra part, needed to delete.two parts seperating by white space.

extra4: handle the decode probled refer the code in project

extra5: seperating by semicolon.And a part was seperating by colon,first is the dic key name,second is json key name if value was incapsulate in multi cap,you can use this garmmar:keywords->keyname and if
 want get all value of key,you need add the prefix '*loop'.

extra6: same as ulweb.

 ### Five    
type: five


 ## Questions or tips    
 ### Extra problems:   
http://ent.163.com/17/0227/15/CE9R3SD5000380D0.html    
Extra data by ruler
```
date**:div class=post_time_source
```
the tag is 
```
<div class="post_time_source">2017-03-17 10:28:45　来源: <a href="#" id="ne_article_source" rel="nofollow" target="_blank">网易娱乐</a></div>
```
but,the result is "网易娱乐".The problem is we extra data using double star "**"..?removed "**", the ruler become "date:div class=post_time_source" then we get the result,is 
```
  2017-03-17 10:28:45　 来源: 网易娱乐  
```
or change the ruler to 

```
date^:div class=post_time_source
```
the result is
```
2017-03-1710:28:45来源:网易娱乐
```


 ### Princile
- Should not get title in the content,because the title are obtained at list.

## 拓展:
#### 自动播放量特征
### 优酷：
#### 搜索页：http://www.soku.com/search_video/q_{0}
#### 获取方式：搜索结果中的标题链接能够进入总览页，其中有总播放数量
优酷不在意播放平台，无论综艺影剧得到的都是总量
无论是否为优酷独播

### 爱奇艺:
#### 搜索页：http://so.iqiyi.com/so/q_{0}
#### 获取方式：
电视剧：
获取数字链接，需要检查进入的是否为爱奇艺网站，不是加入黑名单，采集的是总播放数。
综艺：
获取数字链接，需要检查进入的是否为爱奇艺网站（so.iqiyi 不是），不是则加入黑名单，采集各分集播放量总和

### 腾讯视频:
#### 搜索页：https://v.qq.com/x/search/?q={0}
#### 获取方式：
电视剧：
获取数字链接，需要检查进入的是否为腾讯网站，不是加入黑名单，是的采集的是总播放数。
综艺：
获取数字链接，需要检查进入的是否为爱奇艺网站（so.iqiyi 不是），不是则加入黑名单，采集各分集播放量总和
但是。。。。。。有个更多按钮，这个暂时不考虑

