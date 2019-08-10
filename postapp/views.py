from math import ceil

from django.shortcuts import render,redirect

from postapp.models import Post


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

def create(request):
    if request.method == 'POST':
        title =request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title,content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        return render(request,'create.html')


def edit(request):
    if request.method == 'POST':
        # 取出 post
        post_id = int(request.GET.get('post_id',1))
        post = Post.objects.get(id=post_id)
        # 更新数据
        post.title =request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = int(request.GET.get('post_id',1))
        post = Post.objects.get(id=post_id)
        return render(request,'edit.html',{'post':post})
    
    
def read(request):
    post_id = int(request.GET.get('post_id',1))
    post = Post.objects.get(id=post_id)
    return render(request,'read.html',{'post':post})
    

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
