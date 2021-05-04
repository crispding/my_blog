import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ArticePostForm
from .models import ArticlePost


# Create your views here.
def index(request):
    # return HttpResponse("Hello World!")
    search = request.GET.get('search')
    if search:
        article_list = ArticlePost.objects.filter(
            Q(title__icontains=search) | Q(body__icontains=search))
        paginator = Paginator(article_list, 10)
        page = request.GET.get('page')
        articles = paginator.get_page(page)
        context = {
            'articles': articles,
            'article_list_active': 'active',
            'search': search
        }
        return render(request, 'article/list.html', context)
    else:
        # 将 search 参数重置为空
        search = ''
        article_recent = ArticlePost.objects.all()[:4]
        context = {'articles': article_recent, 'index_active': 'active'}
        return render(request, 'index.html', context)


def article_list(request):
    # return HttpResponse("Hello World!")
    search = request.GET.get('search')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    if search:
        article_list = ArticlePost.objects.filter(
            Q(title__icontains=search) | Q(body__icontains=search))
    else:
        # 将 search 参数重置为空
        search = ''
        article_list = ArticlePost.objects.all()

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    paginator = Paginator(article_list, 10)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        'article_list_active': 'active',
        'search': search,
        'tag': tag,
    }
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    article.body = md.convert(article.body)
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    context = {'article': article, 'toc': md.toc}
    return render(request, 'article/detail.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            return redirect("index:index")
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    else:
        article_post_form = ArticePostForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)


@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)

    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    if request.method == "POST":
        article_post_form = ArticePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.excerpt = request.POST['excerpt']
            article.body = request.POST['body']
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            return redirect("index:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    else:
        article_post_form = ArticePostForm()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'tags': ','.join([x for x in article.tags.names()]),
        }
        return render(request, 'article/update.html', context)
