#!/usr/bin/env python
# -*- coding: utf-8 -*-


# @Author  : YuLuo
"""
杀死已运行python进程脚本
"""

import sys,os

def kill_process(name):
    cmd = "ps -ef |grep {}".format(name)
    popen = os.popen(cmd)
    lines = popen.readlines()
    if len(lines) == 0 :
        print('no process {}'.format(name))
        return
    else:
        for line in lines:
           col= line.split()
           pid = col[1]
           cmd = "kill -9 {}".format(int(pid))
           rc = os.system(cmd)
           if(rc ==0):
                print("exec {} success!!".format(cmd))
           else:
                print("exec {} fail!!".format(cmd))
        return

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('input the process name which you want to kill ')
    else:
        name = sys.argv[1]
    kill_process(name)