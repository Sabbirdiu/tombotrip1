from django.contrib import admin
from .models import Experience,Supply,Rating,Cartypes,ProductAttribute,Order,Category,Transmission,OrderSupply,Reserve

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'status','create_at']
    list_filter = ['status']
    readonly_fields = ('subject','comment','ip','user','supply','rate','id')  
class OrderAdmin(admin.ModelAdmin):
    # list_display = ['first_name', 'last_name','phone','location','total','status']
    list_filter = ['status']
    readonly_fields = ('user','location','phone','first_name', 'last_name','phone','location','total','start_date','end_date','num_of_traveller')
    can_delete = False

    
admin.site.register(Experience,ArticleAdmin)
admin.site.register(Supply,SupplyAdmin)
admin.site.register(Rating,CommentAdmin) 
admin.site.register(Cartypes)
admin.site.register(Transmission)  
admin.site.register(ProductAttribute) 
admin.site.register(Order,OrderAdmin) 
admin.site.register(OrderSupply)
admin.site.register(Category)
admin.site.register(Reserve)