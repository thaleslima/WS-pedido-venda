from django.contrib import admin

# Register your models here.
from pedidovenda.models import Categoria
from pedidovenda.models import Produto
from pedidovenda.models import Pedido
from pedidovenda.models import ItemPedido
from pedidovenda.models import Mesa

from django.contrib import admin

class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('id', 'descricao')


class ProdutoAdmin(admin.ModelAdmin):
	list_display = ('id', 'descricao', 'valor', 'categoria')

	def get_name(self, obj):
		return obj.categoria.descricao

	get_name.admin_order_field  = 'categoria'  #Allows column order sorting
	get_name.short_description = 'Categoria'  #Renames column head


class MesaAdmin(admin.ModelAdmin):
	list_display = ('id', 'descricao', 'status', 'tipo')


class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'status')


class ItemPedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'quantidade', 'observacao', 'status', 'valorTotal')
	

admin.site.register(Produto,ProdutoAdmin)
admin.site.register(Pedido,PedidoAdmin)
admin.site.register(ItemPedido,ItemPedidoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Mesa, MesaAdmin)