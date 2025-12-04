from django.contrib import admin
from .models import Pagina, Produto, Contato

admin.site.site_header = "eGames - Painel administrativo"
admin.site.site_title = "Painel administrativo"
admin.site.index_title = "Bem-vindo(a) ao painel administrativo"


@admin.register(Pagina)
class PaginaAdmin(admin.ModelAdmin):
    list_display = ('nome_do_site', 'email', 'whatsapp', 'criado_em', 'atualizado_em')
    search_fields = ('nome_do_site', 'email', 'endereco')
    readonly_fields = ('criado_em', 'atualizado_em')
    
    fieldsets = (
        ('Informações do site', {
            'fields': ('nome_do_site', 'logo_do_site')
        }),
        ('Conteúdo', {
            'fields': ('texto_chamada', 'texto_sobre', 'imagem_sobre')
        }),
        ('Contato', {
            'fields': ('endereco', 'email', 'whatsapp')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'criado_em', 'atualizado_em')
    list_filter = ('criado_em', 'atualizado_em')
    search_fields = ('nome', 'descricao')
    readonly_fields = ('criado_em', 'atualizado_em')
    list_editable = ('preco', 'estoque')
    
    fieldsets = (
        ('Informações do produto', {
            'fields': ('nome', 'foto', 'descricao')
        }),
        ('Preço e estoque', {
            'fields': ('preco', 'estoque')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'criado_em')
    list_filter = ('criado_em',)
    search_fields = ('nome', 'email', 'mensagem')
    readonly_fields = ('nome', 'email', 'mensagem', 'criado_em')
    
    fieldsets = (
        ('Informações de contato', {
            'fields': ('nome', 'email')
        }),
        ('Mensagem', {
            'fields': ('mensagem',)
        }),
        ('Data', {
            'fields': ('criado_em',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True
