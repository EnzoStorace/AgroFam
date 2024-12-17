from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import MenuItem, OrderModel, OrderItem
from .forms import UserRegisterForm


# Página Inicial
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
 
   
# Sobre nós    
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')
   
   
# Login 
def login_user(request):
    if request.method == ("POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Você foi conectado à sua conta."))
            return redirect('index')
        else:
            messages.success(request, ("Houve um erro, tente novamente"))
            return redirect('login')
            
    else:
        return render(request, 'customer/login.html', {})
    
    
# Logout
def logout_user(request):
    logout(request)
    messages.success(request, ("Você foi desconectado de sua conta."))
    return redirect('index')
    
    
def get_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()

        return render(request, 'customer/user-register.html', {'form': form})


# Produtos    
class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()
        
        context = {
            'menu_items': menu_items
        }
        
        return render(request, 'customer/menu.html', context)


# Buscar produtos por qualquer atributo
class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query) |
            Q(seller__name__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)
    
    
# Adiciona um ou mais do memso item no carrinho    
class AddToCart(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(MenuItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))

        # Inicia o carrinho na sessão se ainda não existe
        cart = request.session.get('cart', {})

        # Verifica se o item já está no carrinho
        found = False
        for key, item_data in cart.items():
            if item_data['item_id'] == item_id:
                # Se o produto já existe, atualiza a quantidade
                item_data['quantity'] += quantity
                found = True
                break

        if not found:
            # Se o produto não está no carrinho, adiciona uma nova entrada
            unique_key = get_random_string(8)
            cart[unique_key] = {
                'item_id': item_id,
                'quantity': quantity,
                'name': item.name,
                'price': str(item.price),
            }

        # Salva o carrinho atualizado na sessão
        request.session['cart'] = cart

        return redirect('menu')
    
    
# Remove uma unidade de item do carrinho por vez   
class RemoveFromCart(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')  # Obtém o ID do item a ser removido
        if not item_id:
            return redirect('cart-summary')

        # Recupera o carrinho da sessão
        cart = request.session.get('cart', {})

        # Procura o item no carrinho
        for key, item_data in cart.items():
            if item_data['item_id'] == item_id:
                # Verifica se a quantidade é maior que 1
                if item_data['quantity'] > 1:
                    # Subtrai 1 da quantidade do produto no carrinho
                    item_data['quantity'] -= 1
                else:
                    # Se a quantidade for 1, remove o item do carrinho completamente
                    del cart[key]
                break

        # Atualiza o carrinho na sessão
        request.session['cart'] = cart

        return redirect('cart-summary')
    
    
# Carrinho de compras    
class CartSummary(View):
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        items = []
        total_price = 0

        for key, item_data in cart.items():
            menu_item = MenuItem.objects.get(id=item_data['item_id'])
            quantity = item_data['quantity']
            subtotal = menu_item.price * quantity
            total_price += subtotal

            items.append({
                'key': key,
                'item': menu_item,
                'quantity': quantity,
                'subtotal': subtotal
            })

        context = {
            'items': items,
            'total_price': total_price
        }

        return render(request, 'customer/cart-summary.html', context)
    
    
# Finalizar pedido
class FinalizeOrder(View):
    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        address = request.POST.get('address')

        if not address:
            return HttpResponseBadRequest('Endereço é obrigatório.')

        # Criar o pedido
        order = OrderModel.objects.create(price=0, address=address)

        # Adicionar itens ao pedido
        total_price = 0
        for key, item_data in cart.items():
            menu_item = MenuItem.objects.get(id=item_data['item_id'])
            quantity = item_data['quantity']
            # Criar o Item de Pedido (OrderItem)
            order_item = OrderItem.objects.create(order=order, item=menu_item, quantity=quantity)
            total_price += order_item.subtotal

        order.price = total_price
        order.save()

        # Limpar o carrinho da sessão
        del request.session['cart']

        return redirect('order-confirmation', order_id=order.id)
    
    
# Pedido confirmado
class OrderConfirmation(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = OrderModel.objects.get(id=order_id)

        order_items = OrderItem.objects.filter(order=order)

        context = {
            'order': order,
            'order_items': order_items,
        }

        return render(request, 'customer/order-confirmation.html', context)
    



    