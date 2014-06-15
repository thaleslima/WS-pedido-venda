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
		pedido_data = str(request.body)[2:-1]
		pedido_data2 = json.loads(pedido_data)

		mesa = Mesa.objects.get(id = pedido_data2['idMesa'])
		mesa.status = 2
		mesa.save()

		pedido = Pedido(status = 1, mesa = mesa)
		pedido.save()

		for item in pedido_data2['itensPedido']:
			produto = Produto.objects.get(id = item['produto']['id'])
			itemPedido = ItemPedido(quantidade = item['quantidade'], observacao = item['observacao'], status = 2, valorTotal = item['valorTotal'], pedido = pedido, produto = produto)
			itemPedido.save()

		return HttpResponse(json.dumps(retornar_pedido_completo(mesa.id)), content_type = "application/json")
	return HttpResponse("no data")


@csrf_exempt
def adicionar_item_pedido(request):
	if request.method == 'POST':
		pedido_data = str(request.body)[2:-1]
		pedido_data2 = json.loads(pedido_data)

		pedido = Pedido.objects.get(id = pedido_data2['numero'])

		for item in pedido_data2['itensPedido']:
			produto = Produto.objects.get(id = item['produto']['id'])
			itemPedido = ItemPedido(quantidade = item['quantidade'], observacao = item['observacao'], status = 2, valorTotal = item['valorTotal'], pedido = pedido, produto = produto)
			itemPedido.save()

		return HttpResponse(json.dumps(retornar_pedido_completo(mesa.id)), content_type = "application/json")
	return HttpResponse("no data")


def listar_pedido_mesa(request, id_mesa):
	return HttpResponse(json.dumps(retornar_pedido_completo(id_mesa)), content_type = "application/json")


def retornar_pedido_completo(id_mesa):
	mesa = Mesa.objects.get(id=id_mesa)
	pedido = Pedido.objects.get(mesa = mesa)

	pedido_response = {}
	pedido_response['numero'] = pedido.id
	pedido_response['status'] = pedido.status
	pedido_response['idMesa'] = mesa.id

	itensPedido = []

	itemPedido_list = ItemPedido.objects.filter(pedido=pedido)
	for item in itemPedido_list:
		itemPedido_response = {}
		itemPedido_response['quantidade'] = item.quantidade
		itemPedido_response['observacao'] = item.observacao
		itemPedido_response['status'] = item.status
		itemPedido_response['valorTotal'] = float(item.valorTotal)
		itemPedido_response['produto'] = {}
		itemPedido_response['produto']['id'] = item.produto.id
		itemPedido_response['produto']['descricao'] = item.produto.descricao
		itemPedido_response['produto']['valor'] = float(item.produto.valor)
		itemPedido_response['produto']['idCategoria'] = item.produto.categoria.id

		itensPedido.append(itemPedido_response)
	pedido_response['itensPedido'] = itensPedido

	return pedido_response