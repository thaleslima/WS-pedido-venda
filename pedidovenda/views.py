from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core import serializers
import json
from django.http import HttpResponse

from pedidovenda.models import Categoria
from pedidovenda.models import Produto
from pedidovenda.models import Pedido
from pedidovenda.models import ItemPedido
from pedidovenda.models import Mesa

from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

# Create your views here.
def listar_produtos(request):
	categoria_list = Categoria.objects.all()
	categorias = []

	for item in categoria_list:
		categoria = {}
		categoria['id'] = item.id
		categoria['descricao'] = item.descricao

		produto_list = Produto.objects.filter(categoria__id=item.id)
		produtos = []
		for item2 in produto_list:
			produto = {}
			produto['id'] = item2.id
			produto['descricao'] = item2.descricao
			produto['valor'] = float(item2.valor)
			produtos.append(produto)

		categoria['produtos'] = produtos
		categorias.append(categoria)

	return HttpResponse(json.dumps(categorias), content_type = "application/json; charset=utf-8")


def listar_mesas(request):
	mesas_list = Mesa.objects.all()
	mesas = []
	for item in mesas_list:
		mesa = {}
		mesa['id'] = item.id
		mesa['descricao'] = item.descricao
		mesa['status'] = item.status
		mesa['tipo'] = item.tipo
		
		mesas.append(mesa)

	return HttpResponse(json.dumps(mesas), content_type = "application/json; charset=utf-8")

def validar_usuario(request, login, password):
	if request.method == 'GET':
		if login == "admin" and password == "123":
			data = {}
			data['id'] = 1
			data['name'] = "Admin"
			data['email'] = "admin@admin.com"
			data['login'] = login
			return HttpResponse(json.dumps(data), content_type = "application/json")

	data = {}
	
	data['status'] = "Fail"
	data['message'] = "Usuario nao cadastrado."
	return HttpResponse(json.dumps(data), content_type = "application/json; charset=utf-8")

@csrf_exempt
def enviar_pedido(request):
	if request.method == 'POST':
		#pedido_data = str(request.body)[2:-1]
		#pedido_data2 = json.loads(pedido_data)





		return HttpResponse(request.body)

	return HttpResponse("no data")
