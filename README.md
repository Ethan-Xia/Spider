# Spider
学习python语言下的spider。此项目中，主要记录了使用python语言开发的抓取“市长信箱”中信件的爬虫。随着学习的深入，开发出的不同版本放到不同的文件夹中，并对其中的关键进行记录。

*上传后发现，上传到 GitHub 的文件帐户标记是 码云 的帐户。于是在设置中更改了全局配置，将帐户调整为GitHub帐号。现在实验一下，配置是否能起作用。*

## 文件说明
*xyzf_spider_0.py* 爬虫，结合自身项目需要，改编自《Python爬虫开发与项目实战》第6章的基础爬虫。整个爬虫，具有完整且应有的结构。改动其中的解析器，获得index页中的标题和链接列表，最终通过循环保存为html。

未来的改进1：改进网页解析器，抓取index页后，提取其中的详情页链接，并进一步抓取解析详情页。

改进尝试：类似于Scrapy中的解析函数的写法，分别定义两个具有不同功能的parser函数来解析网页。但在Scrapy中，可以通过 *callback* 参数来回调详情页解析函数，从而实现多层级抓取。
在本次尝试中，在网页解析器中同时定义了：*parser* 和 *parser_detail* 函数来实现用parser从index页中提取详情页链接，并在parser_detail中提取数据。但在调用时，并没有通过回调的方式的实现，而是在调试器中直接通过顺序调用来处理。
虽然最终实现了预期效果，但可能并不是一个好的方式。

未来改进2：从外部导入对应模块来完善一个爬虫，且完善相应的回调机制。
