from django.contrib import admin

# Register your models here.
from .models import *

class TagTublerinline(admin.TabularInline):
    model=Tag

class ProductAdmin(admin.ModelAdmin):
    inlines=[TagTublerinline]

class OrderitemTubleinline(admin.TabularInline):
    model = Orderitem


class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderitemTubleinline]
    list_display = ['firstname','phone','email','paymentid','paid','date']
    search_fields = ['firstname','email','paymentid']

class OrderitemAdmin(admin.ModelAdmin):
    list_display = ['user','product','price','date_added']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'review_desp','ratings']


admin.site.register(Tag)
admin.site.register(Categories)
admin.site.register(Colour)
admin.site.register(Brand)
admin.site.register(review,ReviewAdmin)
admin.site.register(Filter_Price)
admin.site.register(Product,ProductAdmin)
admin.site.register(Contact_us)
admin.site.register(Order,OrderAdmin)
admin.site.register(Orderitem,OrderitemAdmin)
admin.site.register(wishlist)
