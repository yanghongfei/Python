- 1. python3 auth.py  #运行
- 2. http://ip/weibo/add  #添加，如果没有登陆提示用户登陆
- 3. 提交内容到数据库
```
MySQL [yanghongfeitest]> select * from weibo;
+--------------------+-------------+----------+
| id                 | username    | content  |
+--------------------+-------------+----------+
| 1538995460.0657806 | yanghongfei | test111  |
| 1538995520.6959584 | test        | test0032 |
| 1538995728.7173202 | test        | test1111 |
+--------------------+-------------+----------+
3 rows in set (0.00 sec)


```