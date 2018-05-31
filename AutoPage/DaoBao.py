#!/usr/bin/env python
#coding=utf-8 
import os
import commands
import requests
import webbrowser

#使用注意事项:该脚本基于python2.7

#需要手动配置以下6个小项

#1.将工程的编译设备选成 Gemeric iOS Device， 然后command + B编译

#2.这里是 Xcode 项目下，经过编译之后的 Products 的 App 的路径可以直接拖进来。
appFileFullPath = '/Users/linyi/Library/Developer/Xcode/DerivedData/nbiot-1st-bodspekapzgqzmdvwmvnboyxynkx/Build/Products/Debug-iphoneos/nbiot-1st.app'

#3.这里是自动打包之后的 ipa 文件路径，可以在桌面新建一个文件夹，命名为 Payload，同上，可以直接拖
PayLoadPath = '/Users/linyi/Desktop/Payload'

#4.这是是自动打包的流程，可以在桌面新建一个文件夹 命名为 ProgramBag
packBagPath = '/Users/linyi/Desktop/ProgramBag'

#5.将此处打开的链接改为蒲公英对应app的链接
openUrl = 'https://www.pgyer.com/manager/dashboard/app/9f840e4a73529fa4e099c46075707db5'

#6.上传蒲公英的KEY
USER_KEY = "9644dd968***********a7c27227ad8"
API_KEY = "9d0e1b***********5351b19f2f41352"

#7.打开命令行终端，输入 python，然后空格，然后把这个本文件拖进去，回车。

'''
    错误排查
    1.如果提示，ImportError: No module named requests
    那么请安装requests 模块 sudo easy_install -U requests
    
    2.如果提示 File "<string>", line 1, in <module>
    NameError: name '修复首页bug' is not defined
    输入的时候注意以字符串的形式输入就好，如 "修复了首页的bug" 记得加上英文双引号!
'''

#上传蒲公英
def uploadIPA(IPAPath):
    if(IPAPath==''):
        print "\n*************** 没有找到对应上传的IPA包 *********************\n"
        return
    else:
        print "\n***************开始上传到蒲公英*********************\n"
        url='http://www.pgyer.com/apiv1/app/upload'
        data={
            'uKey':USER_KEY,
            '_api_key':API_KEY,
            'installType':'2',
            'password':'',
            'updateDescription':des
        }
        files={'file':open(IPAPath,'rb')}
        r=requests.post(url,data=data,files=files)

def openDownloadUrl():
    webbrowser.open(openUrl,new=1,autoraise=True)
    print "\n*************** 更新成功 *********************\n"


#创建PayLoad文件夹
def mkdir(PayLoadPath):
    isExists = os.path.exists(PayLoadPath)
    if not isExists:
        os.makedirs(PayLoadPath)
        print PayLoadPath + '创建成功'
        return True
    else:
        print PayLoadPath + '目录已经存在'
        return False


#编译打包流程
def bulidIPA():
    #打包之前先删除packBagPath下的文件夹
    commands.getoutput('rm -rf %s'%packBagPath)
    #创建PayLoad文件夹
    mkdir(PayLoadPath)
    #将app拷贝到PayLoadPath路径下
    commands.getoutput('cp -r %s %s'%(appFileFullPath,PayLoadPath))
    #在桌面上创建packBagPath的文件夹
    commands.getoutput('mkdir -p %s'%packBagPath)
    #将PayLoadPath文件夹拷贝到packBagPath文件夹下
    commands.getoutput('cp -r %s %s'%(PayLoadPath,packBagPath))
    #删除桌面的PayLoadPath文件夹
    commands.getoutput('rm -rf %s'%(PayLoadPath))
    #切换到当前目录
    os.chdir(packBagPath)
    #压缩packBagPath文件夹下的PayLoadPath文件夹夹
    commands.getoutput('zip -r ./Payload.zip .')
    print "\n*************** 打包成功 *********************\n"
    #将zip文件改名为ipa
    commands.getoutput('mv Payload.zip Payload.ipa')
    #删除payLoad文件夹
    commands.getoutput('rm -rf ./Payload')

if __name__ == '__main__':
    des = input("请输入更新的日志描述:注意，日志需要用英文的双引号括起来。 ")
    bulidIPA()
    uploadIPA('%s/Payload.ipa'%packBagPath)
    openDownloadUrl()
