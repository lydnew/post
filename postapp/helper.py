# coding: utf-8

from django.core.cache import cache

from common.keys import PAGE_KEY,READ_COUNT_KEY
from common import rds

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
        rds.zincrby(READ_COUNT_KEY,post_id)
        return read_view(requests)
    return wrap


