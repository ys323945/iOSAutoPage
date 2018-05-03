#!/usr/bin/env python
#coding=utf-8 
import os,time
#import commands
import subprocess
import requests
import webbrowser
import time

#上传蒲公英
USER_KEY = "61ded40a68afxxxxxxxfd278acd2"
API_KEY = "a4fe2724dc6d8xxxxxxxx1994eec219e"

def searchIpaPath():
    IpaPath=""
    for i in os.listdir("."):
        if(i.find('.ipa')!=(-1)):
            IpaPath=i
            print '找到的IPA文件:'+IpaPath
            return IpaPath
    return IpaPath

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
    #此处的地址需要换成蒲公英上自己对应的应用地址
    webbrowser.open(r'https://www.pgyer.com/manager/dashboard/app/40c633aa8dc0ba15191632860558825e',new=1,autoraise=True)
    print "\n*************** 更新成功 *********************\n"

def buildIpa():
    start = time.time()
    print "\n*************** IPA包生成中 *********************\n"
     #commands.getoutput('ipa build')  #使用shenzheng打包ipa
    p = subprocess.Popen('ipa build', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line,
    retval = p.wait()

    end = time.time()
    print "--------- 打包耗时:%s秒 ---------"%(end-start)
    print "\n*************** IPA包生成成功，准备上传蒲公英 *********************\n"


if __name__ == '__main__':
    #输入日志格式为 "修改bug" 记得加上双引号，如果有多行可以这么写:
    # "1 修改首页bug  \n  2 修改点击按钮闪退问题 "
    des = input("请输入更新的日志描述:")
    buildIpa()
    IpaPath=searchIpaPath()
    uploadIPA(IpaPath)
    openDownloadUrl()


