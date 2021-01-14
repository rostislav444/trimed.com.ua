from django.db import models
from django.utils import timezone 
from django.utils.translation import ugettext, ugettext_lazy as _


# Create your models here.
class Order(models.Model):
    ORDER_STATUS = [
        ('new',        'Новый заказ'),
        ('created',    'Создан, ожидает оплаты'),
        ('payed',      'Оплачен, в обработке'),
        ('prepered',   'Собран, ожидает передачи на доставку'),
        ('at_delivry', 'Передан на доставку'),
        ('delivring',  'Доставляется'),
        ('delivred',   'Доставлен'),
        ('declined',   'Отменен'),
    ]
    PAY_TYPE = [
        ('np',    'Наложеный платежь'),
        ('card',  'Оплата картой на сайте'),
        ('cash',  'Наличными при получении'),
    ]
    status_old =  models.CharField(max_length=255, editable=False, blank=True, null=True, choices=ORDER_STATUS, verbose_name=_("Статус заказа"))
    status =      models.CharField(max_length=255, choices=ORDER_STATUS, verbose_name=_("Статус заказа"))
    pay_type =    models.CharField(max_length=255, choices=PAY_TYPE, verbose_name=_("Способ оплаты"))
    user =        models.ForeignKey('user.CustomUser', blank=True, on_delete=models.SET_NULL, null=True, verbose_name=_("Пользователь"), related_name="orders")
    name =        models.CharField(max_length=50, blank=True, verbose_name=_("Имя"))
    surname =     models.CharField(max_length=50, blank=True, verbose_name=_("Фамилия"))
    patronymic =  models.CharField(max_length=50, blank=True, verbose_name=_("Отчество"))
    phone =       models.CharField(max_length=40, blank=True, verbose_name=_("Номер телефона"))
    email =       models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    created =     models.DateTimeField(blank=True, null=True, verbose_name=_("Время заказа"), default=timezone.now)
    payed =       models.DateTimeField(blank=True, null=True, verbose_name=_("Время оплаты"), default=None)

    class Meta:
        ordering = ['-created']
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def get_total(self):
        total = 0
        for product in self.products.all():
            total += product.total_ua
        return total


class OrderProduct(models.Model):
    parent =    models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Продукт"), related_name='products')
    product =   models.ForeignKey('catalogue.Product', on_delete=models.CASCADE, verbose_name=_("Продукт"))
    quantity =  models.PositiveIntegerField(default=1, verbose_name=_("Количество"))
    price =     models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name=_("Розничная"))
    price_ua =  models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name=_("Розничная, грн."))
    total =     models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name=_("Всего"))
    total_ua =  models.DecimalField(default=0, decimal_places=2, max_digits=200, verbose_name=_("Всего, грн."))

    class Meta:
        verbose_name = _("Товар в заказе")
        verbose_name_plural = _("Товар в заказе")

    def __str__(self):
        return f"{self.product.name}, артикул: {str(self.product.code)}, {str(self.quantity)} шт., всего: {str(int(self.total_ua))}, грн."
   


    def save(self):
        print('save')
        self.price =    self.product.price
        self.price_ua = self.product.price_ua
        self.total =    self.price * self.quantity
        self.total_ua = self.price_ua * self.quantity
        super(OrderProduct, self).save()
    

class OrderDeliveryNP(models.Model):
    parent = models.OneToOneField(Order, on_delete=models.CASCADE)
    city =   models.CharField(max_length=50, blank=True, verbose_name=_("Город"))
    branch = models.CharField(max_length=50, blank=True, verbose_name=_("Номер отделения"))

    class Meta:
        verbose_name = _("Доставка Новой почтой")
        verbose_name_plural = _("Доставка Новой почтой")


    def __str__(self):
        return f'{self.city} {self.branch}'
    

class OrderDeliveryCurier(models.Model):
    parent =     models.OneToOneField(Order, on_delete=models.CASCADE)
    city =       models.CharField(max_length=50, blank=True, verbose_name=_("Город"))
    street =     models.CharField(max_length=50, blank=True, verbose_name=_("Улица"))
    house =      models.CharField(max_length=50, blank=True, verbose_name=_("Дом"))
    appartment = models.CharField(max_length=50, blank=True, verbose_name=_("Квартира"))
    
    class Meta:
        verbose_name = _("Доставка курьером")
        verbose_name_plural = _("Доставка курьером")