```python
用户登陆：
http://172.16.0.101:8000/

用户注销：
http://172.16.0.101:8000/logout?logout=1

class LogoutHandler(BaseHandler):
    """get方式"""
    def get(self, *args, **kwargs):
        if (self.get_argument('logout', None)):
            self.clear_cookie('username')
            self.redirect('/')

# Post方式  index.html
<form action="/logout?logout=1" method="post">
    <input type="submit" value="Log out"></br>

class LogoutHandler(BaseHandler):
    def post(self):
        if (self.get_argument('logout', None)):
            self.clear_cookie('username')
        self.redirect('/')

```
