### 事件提醒
#### 表结构

```mysql
CREATE TABLE `event_reminder` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
   `name` varchar(255) not null,
   `content` varchar(255) not null,
   `email` varchar(255) not null,
   `advance_at` int(255) not null,
   `expire_at` datetime not null DEFAULT CURRENT_TIMESTAMP,
   `create_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   `update_at`  timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

#修改字符集
 ALTER TABLE `event` CHANGE `advance_time` `advance_time` VARCHAR(255) CHARACTER SET utf8 NOT NULL;
 
 #SQL插入示例：
 insert into event_reminder(name,content,email,advance_at,expire_at) VALUES('测试呀','这是一条测试语句呀','yanghongfei@shinezone.com','10','2018-01-01');

```

#### API接口
- URL: http://172.16.0.101:8888/event
- 工具： Postman
- 支持：GET/POST/PUT/DELETE

示例：
```python
# Body内容,根据name判断
{
    "name": "Ec2",   #名字
    "content": "服务器到期提醒",  #内容备注
    "email": "yanghongfei@qq.com, group@qq.com", #Email通知
    "advance_at": "100",  #提前多少天
    "expire_at": "2018-11-30"  #到期时间
}
```

#### 守护进程
- Supervisor安装
```bash
$ sudo pip install supervisor 
$ sudo echo_supervisord_conf > /etc/supervisord.conf
$ mkdir -p /etc/supervisor/conf.d
```
- 创建守护文件
```bash
cat > /etc/supervisor/conf.d/event_reminder.conf <<EOF
[program:event_reminder]
directory=/opt/Python/TimedTask
command=python3 /opt/Python/TimedTask/event_task.py
autorestart=true
autostart=true
logfile=/tmp/event_tasks.log
EOF
```
- 修改配置文件  

```bash
$ tail -n 3 /etc/supervisord.conf 

[include]
files = /etc/supervisor/conf.d/*.conf
```
- 启动
```bash
$ supervisord
$ supervisorctl 
event_reminder                   RUNNING   pid 12659, uptime 2:58:43
```


