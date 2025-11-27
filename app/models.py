from django.db import models
from django.contrib.auth.models import User

class Pagina(models.Model):
    nome_do_site = models.CharField(max_length=200, verbose_name="Nome do site")
    logo_do_site = models.ImageField(upload_to='logos/', verbose_name="Logo do site")
    texto_chamada = models.TextField(verbose_name="Texto de chamada")
    texto_sobre = models.TextField(verbose_name="Texto do sobre")
    imagem_sobre = models.ImageField(upload_to='sobre/', verbose_name="Imagem do sobre")
    endereco = models.CharField(max_length=300, verbose_name="Endereço")
    email = models.EmailField(verbose_name="E-mail")
    whatsapp = models.CharField(max_length=20, verbose_name="WhatsApp")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Página"
        verbose_name_plural = "Páginas"
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome_do_site


class Produto(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    estoque = models.IntegerField(default=0, verbose_name="Estoque")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    descricao = models.TextField(verbose_name="Descrição")
    foto = models.ImageField(upload_to='produtos/', verbose_name="Foto")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    mensagem = models.TextField(verbose_name="Mensagem")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.nome} - {self.email}"


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    quantidade = models.IntegerField(default=1, verbose_name="Quantidade")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data']

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username} - {self.produto.nome}"