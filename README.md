实验性质的“mysite”项目
=====================

- 目的

本人日常在公司做研发项目，是团队的技术领头人。根据项目及客户需求，有少量出差情况。平时的项目管理不符合一个正常软件公司需要具备的框架、条理、逻辑等等，任务比较杂乱而且随机，（反正就是不能用正常的思路去理解这件事，我目前还不具备改变现状的能力。）每到写年终总结时，深受其扰，想不起来做过什么、为什么做、做了多久、有没有加班、有多少出差（还有，出差占用了多少周末）、研发时间在项目中的占比，所以需要一个webapp支持我每天记录自己的工作情况。

另外，也是想在工作之余，给自己找个新的兴趣点。

- 软件环境

	1. ubuntu server 16.04
	2. remarkable 1.87
	3. python3 3.5.2
		包名 本地版本 远端默认安装版本
		1. bottle 0.12.10 0.12.9
		2. bottle-sqlite 0.1.3 无
		3. bottle-cork 0.12.0 无
		4. pycrypto 2.6.1 2.6.1
		5. beaker 1.8.1 无
		6. scrypt 0.8.0 无

- 部署

在 www.pythonanywhere.com 注册了一个免费帐号，用于测试和试用。

- 调试途径

代码在本地计算机编写和调试，在github上托管，同步到pythonanywhere，非常方便。