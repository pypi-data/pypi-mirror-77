from distutils.core import setup
setup(
    name='trafalgar',  #对外我们模块的名字
    version='1.0',  # 版本号
    description='这是第一个对外发布的模块，测试哦', # 描述
    author='sihuake',  # 作者
    author_email='sihuake@163.com',
    py_modules=['trafalgar.demo1','trafalgar.demo2']  #要发布的模块
)
