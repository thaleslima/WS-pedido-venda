from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ws_pedidovenda.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    (r'^login-user/(?P<login>\w+)/(?P<password>\w+)$', 'pedidovenda.views.login_user'),
    (r'^listar-produtos/$', 'pedidovenda.views.listar_produtos'),
    (r'^get-commands/$', 'pedidovenda.views.get_commands'),
)
