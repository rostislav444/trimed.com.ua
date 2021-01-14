from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.order.models import Order, OrderProduct, OrderDeliveryNP, OrderDeliveryCurier
from apps.catalogue.models import Product
from apps.cart.cart import Cart
from apps.user.models import UserAdressChosen
from apps.core.functions import SendMessage




def send_order_email(request, order):
    current_site = get_current_site(request)
    mail_subject = f'TRIMED | Заказ №{order.pk}'
    message = render_to_string('shop/email/order.html', {
        'order':  order,
        'domain': current_site.domain,
    })
    email = send_mail(
        subject=mail_subject, 
        message='',
        from_email='rostislav444@gmail.com', 
        recipient_list=[order.email], 
        html_message=message, 
        fail_silently=False
    )
    return email



class OrderViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    context = {}

    def api(self, request, delivery=None):
        change_adress = request.data.get('change_adress')
        user = request.user
        if change_adress and user.is_authenticated:
            if hasattr(user, 'adress_chosen'):
                user.adress_chosen.delete()
            adress = UserAdressChosen(
                parent = request.user,
                adress = user.adress.get(pk=int(change_adress))
            )
            adress.save()

        args = {'user' : user}
        if delivery in ['newpost', None]:
            html = render_to_string('shop/order/delivery/delivery__newpost.html', args)
        else:
            html = render_to_string('shop/order/delivery/delivery__curier.html', args)
        return Response({'html' : html})

    def create_order(self, data, user):
        order = Order(
            status = 'new',
            name = data.get('name'),
            surname = data.get('surname'),
            patronymic = data.get('patronymic'),
            phone = data.get('phone'),
            email =  data.get('email'),
            user = user if user.is_authenticated else None,
            pay_type = data.get('pay_type'),
        )
        order.save()
        return order

    
    def data(self, request, delivery=None):
        context = {'delivery' : delivery}
        # order =  Order.objects.first()

        # send_order_email(request, order)
        if request.method == 'POST':
            cart = Cart(request)
            data = request.data
            order = self.create_order(data, request.user)
            for item in cart:
                product = Product.objects.filter(pk=int(item['product_id'])).first()
                order_product = OrderProduct(
                    parent = order,
                    product = product,
                    quantity = int(item['quantity'])
                )
                order_product.save()

            if data['delivery'] == 'newpost':
                delivery_np = OrderDeliveryNP(
                    parent = order,
                    city = data.get('city'),
                    branch = data.get('branch'),
                )
                delivery_np.save()
                
            elif data['delivery'] == 'curier':
                delivery_curier = OrderDeliveryCurier(
                    parent = order,
                    city = data.get('city'),
                    street = data.get('street'),
                    house = data.get('house'),
                    appartment = data.get('appartment'),
                )
                delivery_curier.save()
            cart.clear()
            

            msg = 'ЗАКАЗ' + '\n\n'
            msg += f'{order.name} {order.surname} {order.patronymic}' + '\n'
            msg += f'Телефон: {order.phone}' + '\n\n'
            msg += 'ТОВАРЫ:' + '\n\n'
            msg += '- - - - - - - - - - - - - -' + '\n'
            for product in order.products.all():
                msg += f'{product.product.name} - {product.product.code}, '
                msg += f'{str(product.quantity)} шт. * {str(product.price_ua)} грн.' + '\n'
                msg += '- - - - - - - - - - - - - -' + '\n'
            msg += f'\nВсего: {order.get_total()} грн.'

            SendMessage(str(msg))
            if order.email:
                send_order_email(request, order)
            
            return redirect(reverse('order:success'))
        return render(request, 'shop/order/order.html', context)


def order_success(request):
    return render(request, 'shop/order/order__success.html')