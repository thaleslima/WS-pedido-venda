from django.db import models

# Create your models here.
class Mesa(models.Model):
	descricao = models.CharField(max_length=255)
	status = models.IntegerField()
	tipo = models.IntegerField()
	def __unicode__(self):
		return self.descricao


class Categoria(models.Model):
	descricao = models.CharField(max_length=255)

	def __unicode__(self):
		return self.descricao


class Produto(models.Model):
	descricao = models.CharField(max_length=255)
	valor = models.DecimalField(max_digits=5, decimal_places=2)
	categoria = models.ForeignKey(Categoria)

	def __unicode__(self):
		return self.descricao


class Pedido(models.Model):
	status = models.IntegerField()
	mesa = models.ForeignKey(Mesa)

	def __unicode__(self):
		return "Pedido: " + str(self.id)


class ItemPedido(models.Model):
	quantidade = models.IntegerField()
	observacao = models.CharField(max_length=255)
	status = models.IntegerField()
	valorTotal = models.DecimalField(max_digits=5, decimal_places=2)
	pedido = models.ForeignKey(Pedido)
	produto = models.ForeignKey(Produto)

	def __unicode__(self):
		return "Item: " + str(self.id)


class Usuario(models.Model):
	nome = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	login = models.CharField(max_length=255)
	senha = models.CharField(max_length=255)

	def __unicode__(self):
		return self.nome