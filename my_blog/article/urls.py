from django.urls import path
from . import views

# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    # 首页
    path('', views.index, name='index'),
    # 文章列表
    path('article-list/', views.article_list, name='article_list'),
    # 文章详情
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    # 新建文章
    path('article-create/', views.article_create, name='article_create'),
    # 修改文章
    path('article-update/<int:id>/', views.article_update, name='article_update'),
]
