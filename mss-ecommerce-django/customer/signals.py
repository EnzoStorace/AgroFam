# seu_app/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.files import File
from ecommerce_agricultura.settings import MEDIA_ROOT
from PIL import Image
from io import BytesIO
import decimal
import random
import os

from .models import Category, Seller, MenuItem, OrderModel, OrderItem


@receiver(post_migrate)
def populate_initial_data(sender, **kwargs):
    if sender.name != 'customer':
        return  

    if Category.objects.exists():
        print("Dados já populados. Nenhuma ação necessária.")
        return


    nomes_categorias = ['Frutas', 'Verduras', 'Legumes', 'Outros']
    categorias = []
    for nome in nomes_categorias:
        categoria, criada = Category.objects.get_or_create(name=nome)
        categorias.append(categoria)
    print("categorias criadas.")

    
    nomes_vendedores = ['João', 'José', 'Joaquim', 'Joana', 'Jó']
    vendedores = []
    for nome in nomes_vendedores:
        vendedor, criado = Seller.objects.get_or_create(name=nome)
        vendedores.append(vendedor)
    print("5 vendedores criados.")

    
    nomes_itens = ['Batata', 'Maçã', 'Pepino', 'Cebola', 'Banana']
    descricoes = [
        'Bom de fritar',
        'Dá pra fazer uma torta',
        'Pepino',
        'Cebola empanada é bom',
        'Bananas maduras na medida certa'
    ]
    precos = [
        decimal.Decimal('9.99'),
        decimal.Decimal('14.99'),
        decimal.Decimal('7.50'),
        decimal.Decimal('12.00'),
        decimal.Decimal('5.25')
    ]
    menu_items = []
    for i in range(5):
        nome_item = nomes_itens[i]
        descricao_item = descricoes[i]
        preco_item = precos[i]
        
        nome_imagem = f"{nome_item}.webp"
        caminho_imagem = os.path.join(MEDIA_ROOT, 'menu_images', nome_imagem)
        
        if not os.path.isfile(caminho_imagem):
            print(f"Imagem não encontrada para {nome_item}: {caminho_imagem}. Pulando este item.")
            continue  # Pula a criação deste MenuItem se a imagem não existir

        with open(caminho_imagem, 'rb') as img_file:
            django_file = File(img_file, name=nome_imagem)
            item, criado = MenuItem.objects.get_or_create(
                name=nome_item,
                defaults={
                    'description': descricao_item,
                    'price': preco_item,
                    'image': django_file,
                }
            )
        
        item.category.set(random.sample(categorias, k=2))
        item.seller.set(random.sample(vendedores, k=2))
        menu_items.append(item)
    print("5 itens de menu criados.")

    
    for i in range(5):
        pedido = OrderModel.objects.create(
            price=0,  
            is_paid=random.choice([True, False]),
            address=f'Endereço {i+1}'
        )
        total = decimal.Decimal('0.00')
        num_itens = random.randint(1, 3)
        for _ in range(num_itens):
            item_escolhido = random.choice(menu_items)
            quantidade = random.randint(1, 5)
            OrderItem.objects.create(
                order=pedido,
                item=item_escolhido,
                quantity=quantidade
            )
            total += item_escolhido.price * quantidade
        pedido.price = total
        pedido.save()
    print("5 pedidos criados com itens de pedido.")

    print("Banco de dados populado com dados de exemplo.")
