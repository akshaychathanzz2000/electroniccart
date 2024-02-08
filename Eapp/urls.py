from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
path('',views.index,name='home'),
path('product/',views.product,name='product'),
path('products/<int:id>',views.singleproduct,name='singleproduct'),
path('search/',views.search,name='search'),
path('contact/',views.contact,name='contact'),
path('signup/',views.register,name='signup'),
path('login/',views.signin,name='login'),
path('signout/',views.signout,name='signout'),
path('checkout/',views.checkout,name='checkout'),
path('placeorder/',views.placeorder,name='placeorder'),
path('success/',views.success,name='success'),
path('yourorder/',views.yourorder,name='yourorder'),
path('about/',views.about,name='about'),
path('review_page/<int:id>/',views.review_page,name='review_page'),
path('product_review/<int:id>',views.product_reviews,name='product_review'),
path('wishlist/',views.wishlist,name='wishlist'),
# path('wishlistadd/<int:id>/',views.wishlistadd,name='wishlistadd'),
path('update/',views.update,name='update'),




path('cart_add/<int:id>/', views.cart_add, name='cart_add'),
path('item_clear/<int:id>/', views.item_clear, name='item_clear'),
path('item_increment/<int:id>/',views.item_increment, name='item_increment'),
path('item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
path('cart_clear/', views.cart_clear, name='cart_clear'),
path('cart-detail/',views.cart_detail,name='cart_detail'),










]
