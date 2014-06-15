from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ws_pedidovenda.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    (r'^lvalidar-usuario/(?P<login>\w+)/(?P<password>\w+)$', 'pedidovenda.views.validar_usuario'),
    (r'^listar-produtos/$', 'pedidovenda.views.listar_produtos'),
    (r'^listar-mesas/$', 'pedidovenda.views.listar_mesas'),
)
