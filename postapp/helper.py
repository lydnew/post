# coding: utf-8

from django.core.cache import cache

from common.keys import PAGE_KEY,READ_COUNT_KEY
from common import rds
from postapp.models import Post

'''
    缓存更新
        1.手动更新
        2.删除更新
        3.通过过期时间自动更新
'''

def page_cache(timeout):
    def wrap1(view_func):
        def wrap2(request,*args,**kwargs):
            key = PAGE_KEY % request.get_full_path()
            response = cache.get(key)
            if response is None:
                response = view_func(request,*args,**kwargs)
                cache.set(key,response,timeout )
            return response
        return wrap2
    return wrap1



def read_count(read_view):
    def wrap(requests):
        post_id = int(requests.GET.get('post_id',1))
        rds.zincrby(READ_COUNT_KEY,1,post_id)
        return read_view(requests)
    return wrap


def get_top_n(count):
    ori_data = rds.zrevrange(READ_COUNT_KEY,0,count-1,withscores=True)
    # [(b'3', 24.0), (b'2', 18.0), (b'5', 15.0), (b'38', 10.0), (b'1', 6.0)]
    # [[3, 24], [2, 18], [5, 15], [38, 10], [1, 6]]
    rank_data = [[int(post_id),int(count)] for post_id,count in ori_data]
    post_id_list = [post_id for post_id, _ in rank_data]
    # 方法 1
    # # post_dict = {1: <Post: Post object>,
    # #              2: <Post: Post object>,
    # #              3: <Post: Post object>,
    # #              5: <Post: Post object>,
    # #              38: <Post: Post object>,
    # #              ...}
    # post_dict = Post.objects.in_bulk(post_id_list)
    # post_rank = [[post_dict[pid], count] for pid, count in rank_data]

    # 方法 2
    posts = Post.objects.filter(id__in=post_id_list)
    posts = sorted(posts, key=lambda post: post_id_list.index(post.id))
    post_rank = [[post,rank[1]] for post, rank in zip(posts, rank_data)]

    return post_rank