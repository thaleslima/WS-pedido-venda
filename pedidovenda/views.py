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


def get_commands(request):
	commands = []


	for x in range(1, 30):
		command = {}
		command['id'] = x
		command['name'] = format(x, '02d')

		command['status'] = 1

		if x == 3 or x == 7 or x == 21 or x == 6:
			command['status'] = 2

		commands.append(command)

	return HttpResponse(json.dumps(commands), content_type = "application/json; charset=utf-8")

def login_user(request, login, password):
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

