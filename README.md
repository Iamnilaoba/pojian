# pojian
我的第一个Git数据库

常见面试题：
  1.快速排序
   def quickly(list):
         md=list[0]def quick(L):
   	 if len(L) <= 1: return L
    	return quick([i for i in L[1:] if i < L[0]]) + L[0:1] + quick([j for j in L[1:] if j >= L[0]])
  
虚拟环境：（创建一个全新的python虚拟环境，将环境变量加入pycharm解释器中方便我们使用）
	1.安装：pip install virtualenv 
	2.mkdir myproject：创建一个文件夹用来存放即将要创建的虚拟环境，最好cd到桌面创建
	3.cd myproject/：cd到这个文件夹
	4.virtualenv --no-site-packages venv  #创建一个独立的Python运行环境，命名为venv
	   --no-site-packages 不会把第三方包复制过来,这样子得到一个干净的运行环境
	5.source ven/bin/activate：用source进入该环境（加入系统环境变量后可直接使用‘activate’进入）
	6.deactivate：退出该虚拟环境  
