from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.forms import FormUsuario, FormContato
from app.models import Produto, Pedido, Pagina

def home(request):
    produtos = Produto.objects.filter(estoque__gt=0).values()

    formulario = FormContato(request.POST or None)
    if request.POST and formulario.is_valid():
        formulario.save()
        return redirect('home')

    return render(request, 'index.html', {'produtos': produtos, 'form': formulario})

def login_usuario(request):
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

    return render(request, 'login.html')

def cadastro_usuario(request):
    formulario = FormUsuario(request.POST or None)
    if request.POST and formulario.is_valid():
        formulario.save()
        return redirect('home')

    return render(request, 'cadastro.html', {'form': formulario})

@login_required(login_url='login')
def perfil_usuario(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    total = sum(pedido.total for pedido in pedidos)

    return render(request, 'perfil.html', {'pedidos': pedidos, 'total': total})

@login_required(login_url='login')
def logout_usuario(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def compra(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto)
    if produto.estoque <= 0:
        return redirect('home')

    if request.POST:
        quantidade = int(request.POST.get('quantidade', 1))
        if quantidade >= 1 and produto.estoque - quantidade >= 0:
            total = produto.preco * quantidade
            Pedido.objects.create(
                usuario=request.user,
                produto=produto,
                quantidade=quantidade,
                total=total
            )

            produto.estoque -= quantidade
            produto.save()
            return redirect('perfil')
        else:
            messages.error(request, 'Erro ao realizar o pedido')

    return render(request, 'compra.html', {'produto': produto})
