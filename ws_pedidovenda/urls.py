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
    (r'^enviar-pedido/$', 'pedidovenda.views.enviar_pedido'),

    (r'^enviar-pedido/$', 'pedidovenda.views.enviar_pedido'),
	(r'^adicionar-item-pedido/$', 'pedidovenda.views.adicionar_item_pedido'),
	(r'^listar-pedido-mesa/(?P<id_mesa>\w+)$', 'pedidovenda.views.listar_pedido_mesa'),

)
