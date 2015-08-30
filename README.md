# zookeeper-manager #

zookeeper-manager是一个zookeeper web管理工具

Quick Start
----------
1.install app

`pip install django-zookeeper-manager`


2.add "zookeeper" to your INSTALLED_APPS

INSTALLED_APPS = (
    ...,
    'zookeeper',
)

3.incloud the zookeeper URLconf in your project urls.py

urlpatterns = [
    ...,
    url(r'^zookeeper/', include('zookeeper.urls', namespace='zookeeper')),
]

4.创建数据库(使用session)

`python manage.py migrate`

5.run server

`python manage runserver 0.0.0.0:8080`

7.visit http://localhost:8080/zookeeper/
