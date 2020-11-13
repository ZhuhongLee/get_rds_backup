#!/usr/bin/env python
# coding=utf-8

import re
import os
import wget
import argparse
import schedule
import time
import math
from datetime import datetime, date, timedelta
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkrds.request.v20140815.DescribeBackupsRequest import DescribeBackupsRequest
from retrying import retry


def parse_args(AccessKeyId, AccessKeySecret):
    # 定义默认起止时间
    start_time = (date.today() + timedelta(days=-7)).strftime("%Y-%m-%dT00:00Z")
    end_time = datetime.now().strftime("%Y-%m-%dT%H:%MZ")

    # 解析入参
    parser = argparse.ArgumentParser(usage='%(prog)s [options]')
    parser.add_argument('-i', metavar='--instanceid', help='DB InstanceId')
    parser.add_argument('-st', default=start_time, metavar='--start-time', help='Backup Start Time. eg:2019-09-10T00:00Z')
    parser.add_argument('-et', default=end_time, metavar='--end-time', help='Backup End Time. eg:2019-09-10T00:00Z')
    parser.add_argument('-d', default='backup', metavar='--directory', help='create dir if not exists on current dir,default dirname=backup ')
    args = parser.parse_args()
    if args.i and args.st and args.et and args.d:
        downbakupfile(AccessKeyId, AccessKeySecret, args)
    else:
        print("请输入DB实例参数，eg: -i rm-uf68xxxxxxxxxx")


@retry
def downbakupfile(AccessKeyId, AccessKeySecret, args):
    client = AcsClient(AccessKeyId, AccessKeySecret, 'cn-shanghai', timeout=600)
    start_time = args.st
    end_time = args.et

    request = DescribeBackupsRequest()
    request.set_accept_format('json')

    request.set_DBInstanceId(args.i)

    # 新建目录并下载备份文件
    if os.path.exists(args.d):
        pass
    else:
        os.mkdir(args.d)

    # 获取备份总数及每页显示数，计算页数
    request.set_StartTime(start_time)
    request.set_EndTime(end_time)
    response = client.do_action_with_exception(request)
    pages = math.ceil(eval(str(response, encoding='utf-8'))['TotalRecordCount'] / eval(str(response, encoding='utf-8'))['PageRecordCount'])

    for page in range(1, pages + 1):
        request.set_PageNumber(page)
        response = client.do_action_with_exception(request)
        backupdetail = eval(str(response, encoding='utf-8'))['Items']['Backup']

        for i in range(len(backupdetail)):
            bakfile_url = backupdetail[i]['BackupDownloadURL']  # 外网下载地址
            # bakfile_url = backupdetail[i]['BackupIntranetDownloadURL']   # 内网下载地址
            re_result = wget.filename_from_url(bakfile_url)
            bakfile = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), args.d),re_result)
            if os.path.exists(bakfile):
                pass
            else:
                wget.download(bakfile_url, out=bakfile)
                print('下载文件 %s 成功' % bakfile)

    deletefile(args.d)


## 默认删除30天之前的文件
def deletefile(dir):
    path = os.path.join(os.getcwd(), dir)
    for eachfile in os.listdir(path):
        filename = os.path.join(path, eachfile)
        if os.path.isfile(filename):
            lastmodifytime = os.stat(filename).st_mtime
            endfiletime = time.time() - 3600 * 24 * 30
            if endfiletime > lastmodifytime:
                os.remove(filename)
                print("删除文件 %s 成功" % filename)
        elif os.path.isdir(filename):  # 如果是目录则递归调用当前函数
            deletefile(filename)


def main():
    AccessKeyId = 'xxxxxxxxxxxxxxxxxxxx'
    AccessKeySecret = 'xxxxxxxxxxxxxxxxxxxx'
    parse_args(AccessKeyId, AccessKeySecret)


if __name__ == '__main__':
    # main()
    schedule.every(30).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(600)
