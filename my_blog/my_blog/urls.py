"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from os.path import abspath, dirname, join

BASE_DIR = dirname(dirname(abspath(__file__)))
admin_path_file = join(BASE_DIR, "admin_path.txt")
with open(admin_path_file, 'r') as f:
    admin_path = f.readline()
admin_path = admin_path.strip('\n')

urlpatterns = [
    path(admin_path, admin.site.urls),
    path('', include('article.urls', namespace='index')),
    # 新增代码，配置app的url
    # path('article/', include('article.urls', namespace='article')),
    # 用户管理
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
]
