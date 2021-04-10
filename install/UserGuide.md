## 一. 源代码处理工具使用
### 1. 打包应用程序
- ~/anaconda3/bin/python3 setup.py build   --> exe 目录中有应用程序
- ~/anaconda3/bin/python3 setup.py clean

### 2. 打包动态库
- ~/anaconda3/bin/python3 py2so.py dirname --> dirname/build 中用源代码替换编译出来的so
- ./release.sh --> ./mech-II/release/ mech-II的加密

### 3. 去注释
- ~/anaconda3/bin/python3 uncomment.py --> 直接替换ini中配置的目录和文件



