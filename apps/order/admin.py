from django.contrib import admin
from django.utils.safestring import mark_safe
from apps.order.models import Order, OrderProduct, OrderDeliveryNP, OrderDeliveryCurier




class OrderProductInline(admin.StackedInline):
    def image(self, obj=None):
        try:
            img = mark_safe("""
                <a href={href}>
                    <img 
                        style="border-radius:4px;width:120px; height:120px; object-fit: cover; object-position: center; border: 1px solid #ededed;" 
                        src="{url}" width="{width}" height="{height}"
                    />
                </a>
            """.format(
                    url = obj.product.get_image, 
                    href = obj.product.get_absolute_url(), 
                    width=120, 
                    height=120, 
                ))
            return img
        except: return '-'
    image.short_description = 'Изображение'

    model = OrderProduct
    extra = 0
    
    readonly_fields = ['price', 'price_ua', 'total', 'total_ua', 'image']
    fieldsets = (
        (None, {'fields': ('image','quantity',('price', 'price_ua'), ('total', 'total_ua'))}),
    )

class OrderDeliveryNPInline(admin.StackedInline):
    model = OrderDeliveryNP
    extra = 0

class OrderDeliveryCurierInline(admin.StackedInline):
    model = OrderDeliveryCurier
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def total(self, obj):
        if obj: return int(obj.get_total())
        return 0



    total.short_description = 'Всего'

    inlines = [OrderDeliveryNPInline, OrderDeliveryCurierInline, OrderProductInline]
    readonly_fields = ['total']
    list_display = ['created','status','pay_type','name','surname','patronymic','phone','total','payed']

    