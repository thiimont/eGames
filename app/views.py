from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.forms import FormUsuario, FormContato
from app.models import Produto, Pedido, Pagina

def home(request):
    informacoes = Pagina.objects.first()
    produtos = Produto.objects.filter(estoque__gt=0).values()

    formulario = FormContato(request.POST or None)
    if request.POST and formulario.is_valid():
        formulario.save()
        return redirect('home')

    return render(request, 'index.html', {'info': informacoes, 'produtos': produtos, 'form': formulario})

def login_usuario(request):
    informacoes = Pagina.objects.first()
    if request.POST:
        nome = request.POST.get('username')
        senha = request.POST.get('password')
        usuario = authenticate(request, username=nome, password=senha)

        if usuario is not None:
            if usuario.is_active:
                login(request, usuario)
                return redirect('perfil')
            else:
                messages.error(request, 'Este usuário não está ativo')
        else:
            messages.error(request, 'Usuário ou senha incorretos')

    return render(request, 'login.html', {'info': informacoes})

def cadastro_usuario(request):
    informacoes = Pagina.objects.first()
    formulario = FormUsuario(request.POST or None)
    if request.POST and formulario.is_valid():
        formulario.save()
        return redirect('home')

    return render(request, 'cadastro.html', {'info': informacoes, 'form': formulario})

@login_required(login_url='login')
def perfil_usuario(request):
    informacoes = Pagina.objects.first()
    pedidos = Pedido.objects.filter(usuario=request.user)
    total = sum(pedido.total for pedido in pedidos)

    return render(request, 'perfil.html', {'info': informacoes, 'pedidos': pedidos, 'total': total})

@login_required(login_url='login')
def logout_usuario(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def compra(request, id_produto):
    informacoes = Pagina.objects.first()
    produto = get_object_or_404(Produto, id=id_produto)
    if produto.estoque <= 0:
        return redirect('home')

    if request.POST:
        quantidade = int(request.POST.get('quantidade', 1))
        if quantidade >= 1:
            total = produto.preco * quantidade
            Pedido.objects.create(
                usuario=request.user,
                produto=produto,
                quantidade=quantidade,
                total=total
            )

            produto.estoque -= quantidade
            produto.save()
            messages.success(request, 'Pedido realizado com sucesso!')
            return redirect('perfil')
        else:
            messages.error(request, 'Erro ao realizar o pedido')

    return render(request, 'compra.html', {'info': informacoes, 'produto': produto})