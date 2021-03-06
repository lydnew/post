from math import ceil

from django.shortcuts import render,redirect


from common.keys import POST_KEY,READ_COUNT_KEY
from postapp.models import Post,Comment,Tag
from postapp.helper import page_cache, read_count,get_top_n
from user.helper import login_required, check_permission


@login_required
def bulk_create(request):
    content="""
    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    """
    posts = [Post(title='The Zen of Python-%s'%(i+1),content=content) for i in range(35)]
    print(posts)
    result=Post.objects.bulk_create(posts)
    print(result)
    # Post.save()
    return redirect('/post/list/')


@login_required
@check_permission('create_post')
def create(request):
    if request.method == 'POST':
        title =request.POST.get('title')
        content = request.POST.get('content')
        uid = request.session['uid']
        post = Post.objects.create(title=title,content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        return render(request,'create.html')


@login_required
@check_permission('modify_post')
def edit(request):
    if request.method == 'POST':
        # 取出 post
        post_id = int(request.POST.get('post_id',1))
        post = Post.objects.get(id=post_id)
        # 更新数据
        post.title =request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        # # 修改完成后添加到缓存
        # key = POST_KEY % post_id
        # cache.set(key, post)

        # 更新标签
        tag_names = request.POST.get('tags','')
        tag_names = [t.strip().title() for t in tag_names.split(',') if t.strip()]
        post.update_tags(tag_names)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = int(request.GET.get('post_id',1))
        post = Post.objects.get(id=post_id)
        tag_names = ','.join(t.name for t in post.tags())
        return render(request,'edit.html',{'post':post,'tags':tag_names})


@read_count
@page_cache(3)
def read(request):
    # print(11111,request.path)
    post_id = int(request.GET.get('post_id',1))
    """
    # # 从缓存中获取,  如果能取到直接返回
    # key = POST_KEY % post_id
    # post = cache.get(key)
    # print('get from cache: %s' % post)

    # if post is None:
    #     # 如果缓存中没有，从数据库中获取，同时添加到缓存
    #     post = Post.objects.get(id=post_id)
    #     cache.set(key,post)
    #     print('get from db: %s' % post)
    """
    post = Post.objects.get(id=post_id)

    return render(request,'read.html',{'post':post})


@page_cache(1)
def post_list(request):
    if 'val' not in request.session:
        import random
        request.session['val'] = random.randint(1,1000000)
    page = int(request.GET.get('page',1))
    total = Post.objects.count()
    pages = ceil(total / 5)  # 总页数

    start = (page - 1)*5
    end = start + 5
    posts = Post.objects.all().order_by('-id')[start:end]
    return render(request,'post_list.html',{'posts':posts,'pages':range(1,pages+1)})
    

def search(request):
    keyword = request.POST.get('keyword')
    posts = Post.objects.filter(content__contains=keyword)
    return render(request,'search.html',{'posts':posts})


def top10(request):
    '''
    排名  文章名  阅读量
    '''
    post_rank = get_top_n(10)
    return render(request,'top10.html',{'rank_data':post_rank})


@login_required
@check_permission('comment')
def comment(request):
    if request.method == "POST":
        uid = request.session['uid']
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        Comment.objects.create(uid=uid,post_id=post_id,content=content)
        return redirect('/post/read/?post_id=%s' % post_id)
    return redirect('/')


def tag_filter(request):
    tag_id = request.GET.get('tag_id')
    tag = Tag.objects.get(id=tag_id)
    return render(request, 'search.html', {'posts':tag.posts()})


@login_required
@check_permission('del_post')
def del_post(request):
    post_id = request.GET.get('post_id')
    Post.objects.get(id=post_id).delete()
    return redirect('/')