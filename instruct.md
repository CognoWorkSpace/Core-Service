│ db.sqlite3
│ instruct.md
│ manage.py
│  
├───.vscode
│ launch.json
│  
├───app
│ │ admin.py [在 Django 后台提供管理，一般不修改]
│ │ apps.py [不用修改，app 启动类]
│ │ models.py [专门对数据库进行操作]
│ │ tests.py [单元测试，不用修改]
│ │ views.py [经常编写，主要函数]
│ │ **init**.py
│ │
│ └───migrations [不用修改，数据库字段变更]
│ **init**.py
│
└───MyGPT
│ asgi.py
│ settings.py
│ urls.py [url 和函数的对应关系]
│ wsgi.py
│ **init**.py
│
└───**pycache**
settings.cpython-311.pyc
urls.cpython-311.pyc
wsgi.cpython-311.pyc
**init**.cpython-311.pyc
