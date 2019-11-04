# get_rds_backup

包含下载全库备份文件 GetRdsBackupFiles.py 及binlog文件 GetRdsBackupLogFiles.py

### 安装依赖包
pip install aliyun-python-sdk-core aliyun-python-sdk-rds wget retrying


### 新建阿里云账号，修改代码中的 AccessKey和SecretKey
授权如下:

{
  "Statement": [
    {
      "Action": "rds:Describe*",
      "Effect": "Allow",
      "Resource": "*"
    }
  ],
  "Version": "1"
}


{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rds:ModifyBackupPolicy"
      ],
      "Resource": "*"
    }
  ]
}

### 使用方法

###### 1.下载全库备份文件
optional arguments:  
  -h, --help        show this help message and exit  
  -i --instanceid   ，必填，如：rm-ufm6xxxxxxxxxx   
  -st --start-time  查看某个时间段的备份文件，此为开始时间，eg:2019-09-10T00:00Z，默认 now()-7 days  
  -et --end-time    同上，此为结束时间，eg:2019-09-10T00:00Z，默认 now()  
  -d --directory    在当前执行目录创建备份目录，默认文件夹名：backup  


示例：
D:\开发\SVN Upload\get_rds_backup>python GetRdsBackupFiles.py -i rm-uf68xxxxxxxxxx -d crm -st 2019-09-10T00:00Z -et 2019-11-03T00:00Z  
100% [......................................................................] 189379082 / 189379082下载文件 D:\开发\SVN Upload\get_rds_backup\crm\hins7510443_data_20191104065245.tar.gz 成功  
  2% [.                                                                     ]   4644864 / 188754998


###### 2.下载binlog文件
optional arguments:  
  -h, --help        show this help message and exit  
  -i --instanceid   InstanceId，必填，如：rm-ufm6xxxxxxxxxx  
  -st --start-time  查看某个时间段的备份日志，此为开始时间，eg:2019-09-10T00:00:00Z，默认 now()-7 days  
  -et --end-time    同上，此为结束时间，eg:2019-09-10T00:00:00Z，默认 now()  
  -d --directory    在当前执行目录创建备份目录，默认文件夹名：backup  


示例：  
D:\开发\SVN Upload\get_rds_backup>python GetRdsBackupLogFiles.py -i rm-uf68xxxxxxxxxx -d crm -st 2019-09-10T00:00:00Z -et 2019-11-03T00:00:00Z  
100% [......................................................................] 174040615 / 174040615下载文件 D:\开发\SVN Upload\get_rds_backup\crm\7510443_mysql-bin.000794 成功  
100% [..........................................................................] 6590223 / 6590223下载文件 D:\开发\SVN Upload\get_rds_backup\crm\7510443_mysql-bin.000793 成功  
100% [..........................................................................] 6649732 / 6649732下载文件 D:\开发\SVN Upload\get_rds_backup\crm\7510443_mysql-bin.000792 成功  
100% [..........................................................................] 6585247 / 6585247下载文件 D:\开发\SVN Upload\get_rds_backup\crm\7510443_mysql-bin.000791 成功  
100% [..........................................................................] 6598934 / 6598934下载文件 D:\开发\SVN Upload\get_rds_backup\crm\7510443_mysql-bin.000790 成功  
100% [..........................................................................] 6716054 / 6716054下载文件 D:\开发\SVN Upload\get_rds_backup\crm\7510443_mysql-bin.000789 成功  
100% [..........................................................................] 6591846 / 6591846下载文件 D:\开发\SVN Upload\get_rds_backup\crm\7510441_mysql-bin.000788 成功  
 33% [.......................                                                 ] 29450240 / 88473876
