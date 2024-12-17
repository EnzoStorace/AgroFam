from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from customer.views import Index, About, OrderConfirmation, FinalizeOrder, Menu, MenuSearch, CartSummary, AddToCart, RemoveFromCart
from customer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('menu', Menu.as_view(), name='menu'),
    path('menu/search', MenuSearch.as_view(), name='menu-search'),
    path('order-finalize/', FinalizeOrder.as_view(), name='finalize_order'),
    path('order-confirmation/<int:order_id>/', OrderConfirmation.as_view(), name='order-confirmation'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('user-register/', views.get_register, name='user-register'),
    path('add-to-cart/<int:item_id>/', AddToCart.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('cart-summary/', CartSummary.as_view(), name='cart-summary'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
