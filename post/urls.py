"""post URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from postapp import views as post_views
from user import views as user_views

urlpatterns = [
    url(r'^$', post_views.post_list),
    url(r'^post/edit/', post_views.edit),
    url(r'^post/create/', post_views.create),
    url(r'^post/read/', post_views.read),
    url(r'^post/list/', post_views.post_list),
    url(r'^post/search/', post_views.search),
    url(r'^post/bulkcreate/', post_views.bulk_create),
    url(r'^post/top10/', post_views.top10),
    url(r'^post/comment/', post_views.comment),
    url(r'^post/tag/', post_views.tag_filter),
    url(r'^post/delete/', post_views.del_post),

    url(r'^user/register/', user_views.register),
    url(r'^user/logout/', user_views.logout),
    url(r'^user/info/', user_views.user_info),
    url(r'^user/login/', user_views.login),
    url(r'^user/del/', user_views.del_user),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)