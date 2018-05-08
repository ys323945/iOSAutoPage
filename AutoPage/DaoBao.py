#!/usr/bin/env python
#coding=utf-8 
import os
import commands
import requests
import webbrowser

'''
使用注意事项:该脚本基于python2.7
1、将工程的编译设备选成 Gemeric iOS Device
2、command + B编译
3、执行脚本文件

'''

appFileFullPath = '/Users/Qinz/Library/Developer/Xcode/DerivedData/DDDS-bcghxucdqelptddawpsfmvjtoefm/Build/Products/Debug-iphoneos/DDDS.app'
PayLoadPath = '/Users/Qinz/Desktop/Payload'
packBagPath = '/Users/Qinz/Desktop/ProgramBag'

#将此处打开的链接改为蒲公英对应app的链接
openUrl = 'https://www.pgyer.com/manager/dashboard/app/40c633aa8dc0ba15191632860558825e'

#上传蒲公英
USER_KEY = "61ded40a6xxxxxxxxxx2e9fd278acd2"
API_KEY = "a4fe2724dc6xxxxxxxxxf1994eec219e"

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
    des = input("请输入更新的日志描述:")
    bulidIPA()
    uploadIPA('%s/Payload.ipa'%packBagPath)
    openDownloadUrl()


    



    

