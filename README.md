# 本地运行

启动`launcher.py` 或 `wsgi.py`,访问 `http://localhost:8080`

# 服务器运行

### 1 上传代码

使用`PyCharm`的`deploy`功能或直接用`sftp`上传代码到服务器目录`/opt/assistant/`


按照依赖模块

```
# pip install -r requirements.txt
```

### 2 使用Gunicorn启动Web服务

拷贝或链接  `deploy/supervisor.conf` 到 `/etc/supervisor/conf.d/`

```
ln -s /opt/assistant/deploy/supervisor.conf /etc/supervisor/conf.d/assistant.conf
```
 
重新加载`supervisorctl `

```
# supervisorctl reload  
# supervisorctl start assistant  
# supervisorctl status
```


### 3 配置和启动Nginx

拷贝或链接 `deploy/nginx.conf`到`/etc/nginx/sites-enabled`

`ln -s /opt/assistant/deploy/nginx.conf  /etc/nginx/sites-enabled/assistant`

重新启动

```
# service nginx restart
```

### 4 验证

```
http://服务器地址
```


## 参考资料

[https://github.com/defshine/flaskblog](https://github.com/defshine/flaskblog)

