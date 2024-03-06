from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  CustomUser
from .models import order
from .models import product
from .models import Category

admin.site.register(Category)

class CustomUserAdmin(UserAdmin):
    list_display = ('id','username', 'email', 'phone', 'password', 'is_staff', 'is_active')  # 在列表中顯示的欄位
    search_fields = ('username', 'email', 'phone', 'password')  # 允許在管理後台進行搜索的欄位
    list_filter = ('is_staff', 'is_active')  # 過濾器
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('username', 'email','phone', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

admin.site.register(CustomUser,CustomUserAdmin)


class orderAdmin(admin.ModelAdmin):
    list_display=('id','oId','oDate','oProduct', 'oClient','oCost')
    list_filter=('oDate',)
    search_fields=('oDate',)
    ordering=('id',)

admin.site.register(order,orderAdmin)


class productAdmin(admin.ModelAdmin):
    list_display=('id','pId','pName','pCost',  'pCategory','pManufacture','pLoc', 'pQuantity')
    list_filter=('pName',)
    search_fields=('pName',)
    ordering=('id',)
    
admin.site.register(product,productAdmin)



