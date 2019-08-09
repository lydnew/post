from django.shortcuts import render,redirect
from postapp.models import Post

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
    posts = Post.objects.all()
    return render(request,'post_list.html',{'posts':posts})
    

def search(request):
    return render(request,'search.html',{})
