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
from pedidovenda.models import Usuario

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

@csrf_exempt
def validar_usuario(request):
	if request.method == 'POST':
		usuario_data = str(request.body)[2:-1]
		usuario_data2 = json.loads(usuario_data)

		data = {}

		try:
			usuario = Usuario.objects.get(login = usuario_data2['login'])

			if usuario.senha == usuario_data2['senha']:
				data['id'] = usuario.id
				data['nome'] = usuario.nome
				data['email'] = usuario.email
				data['login'] = usuario.login

				data['sucesso'] = True
				data['mensagem'] = ""
			else:
				data['sucesso'] = False
				data['mensagem'] = "A senha informada nao e valida. Verifique e tente novamente."
			

		except Exception:
			data['sucesso'] = False
			data['mensagem'] = "Usuario nao encontrado. Verifique e tente novamente."

		
		return HttpResponse(json.dumps(data), content_type = "application/json")	
	
	return HttpResponse()


@csrf_exempt
def enviar_pedido(request):
	if request.method == 'POST':
		pedido_data = str(request.body)[2:-1]
		pedido_data2 = json.loads(pedido_data)

		mesa = Mesa.objects.get(id = pedido_data2['idMesa'])
		mesa.status = 2
		mesa.save()

		pedido = Pedido(status = 1, mesa = mesa, valorTotal = pedido_data2['valorTotal'], codigoAtendente = pedido_data2['codigoAtendente'])
		pedido.save()

		for item in pedido_data2['itensPedido']:
			produto = Produto.objects.get(id = item['produto']['id'])
			itemPedido = ItemPedido(quantidade = item['quantidade'], observacao = item['observacao'], status = 1, valorUnit = item['valorUnit'], valorTotalItem = item['valorTotalItem'], pedido = pedido, produto = produto)
			itemPedido.save()

		return HttpResponse(json.dumps(retornar_pedido_completo(mesa.id)), content_type = "application/json")
	return HttpResponse("no data")


@csrf_exempt
def abrir_mesa(request):
	if request.method == 'POST':
		mesa_data = str(request.body)[2:-1]
		mesa_data = json.loads(mesa_data)

		mesa_data['status'] = 2

		mesa = Mesa.objects.get(id = mesa_data['id'])
		mesa.status = 2
		mesa.save()

		return HttpResponse(json.dumps(mesa_data), content_type = "application/json")
	return HttpResponse("no data")


@csrf_exempt
def fechar_pedido(request):
	if request.method == 'POST':
		pedido_data = str(request.body)[2:-1]
		pedido_data2 = json.loads(pedido_data)

		mesa = Mesa.objects.get(id = pedido_data2['idMesa'])
		mesa.status = 1
		mesa.save()

		try:
			pedido = Pedido.objects.get(id = pedido_data2['numero'])
			pedido.status = 2
			pedido.save()
		except Exception:
			pass

		pedido_response = {}
		pedido_response['status'] = "OK"

		return HttpResponse(json.dumps(pedido_response), content_type = "application/json")
	return HttpResponse("no data")


@csrf_exempt
def adicionar_item_pedido(request):
	if request.method == 'POST':
		pedido_data = str(request.body)[2:-1]
		pedido_data2 = json.loads(pedido_data)

		mesa = Mesa.objects.get(id = pedido_data2['idMesa'])
		pedido = Pedido.objects.get(id = pedido_data2['numero'])

		for item in pedido_data2['itensPedido']:
			if item['status'] == 0:
				produto = Produto.objects.get(id = item['produto']['id'])
				itemPedido = ItemPedido(quantidade = item['quantidade'], observacao = item['observacao'], status = 1, valorUnit = item['valorUnit'], valorTotalItem = item['valorTotalItem'], pedido = pedido, produto = produto)
				itemPedido.save()

		return HttpResponse(json.dumps(retornar_pedido_completo(mesa.id)), content_type = "application/json")
	return HttpResponse("no data")


def listar_pedido_mesa(request, id_mesa):
	return HttpResponse(json.dumps(retornar_pedido_completo(id_mesa)), content_type = "application/json")


def retornar_pedido_completo(id_mesa):
	mesa = Mesa.objects.get(id=id_mesa)
	listPedido = Pedido.objects.filter(mesa = mesa, status = 1)

	pedido_response = {}

	for pedido in listPedido:
		pedido_response['numero'] = pedido.id
		pedido_response['status'] = pedido.status
		pedido_response['idMesa'] = mesa.id
		pedido_response['valorTotal'] = float(pedido.valorTotal)
		pedido_response['codigoAtendente'] = pedido.codigoAtendente

		itensPedido = []

		itemPedido_list = ItemPedido.objects.filter(pedido=pedido)
		for item in itemPedido_list:
			itemPedido_response = {}
			itemPedido_response['quantidade'] = item.quantidade
			itemPedido_response['observacao'] = item.observacao
			itemPedido_response['status'] = item.status
			itemPedido_response['valorUnit'] = float(item.valorUnit)
			itemPedido_response['valorTotalItem'] = float(item.valorTotalItem)
			itemPedido_response['produto'] = {}
			itemPedido_response['produto']['id'] = item.produto.id
			itemPedido_response['produto']['descricao'] = item.produto.descricao
			itemPedido_response['produto']['valor'] = float(item.produto.valor)
			itemPedido_response['produto']['idCategoria'] = item.produto.categoria.id

			itensPedido.append(itemPedido_response)
		pedido_response['itensPedido'] = itensPedido

	table_response = {}
	table_response = {}
	table_response['id'] = mesa.id
	table_response['descricao'] = mesa.descricao
	table_response['status'] = mesa.status
	table_response['tipo'] = mesa.tipo
	table_response['pedido'] = pedido_response

	return table_response