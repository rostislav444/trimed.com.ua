# DAJNGO
from django.db import models
from django.db.models.signals import pre_init
from django.utils.translation import get_language
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext, ugettext_lazy as _
# APPS
from apps.core.models import Translation
from project import settings
# OTHER
# from googletrans import Translator
import urllib.request
import urllib.parse


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_manager = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    GENDER = (
        ('male', _('М')),
        ('female', _('Ж')),
    )
    # CONTACTS
    email =           models.EmailField(blank=False, unique=True, max_length=500, verbose_name=_("E-mail"))
    email_confirmed = models.BooleanField(default=False)
    phone =           models.CharField(max_length=40, blank=True, null=True, verbose_name=_("Телефон"))
    phone_confirmed = models.BooleanField(default=False)
    # PERSONAL INFO
    name =            models.CharField(max_length=50, blank=True, editable=True, verbose_name=_("Имя"))
    surname =         models.CharField(max_length=50, blank=True, editable=True, verbose_name=_("Фамилия"))
    patronymic =      models.CharField(max_length=50, blank=True, editable=True, verbose_name=_("Отчество"))
    gender =          models.CharField(choices=GENDER, max_length=40, blank=True, null=True, verbose_name=_("Пол"))
    language =        models.ForeignKey('core.Languages', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Язык"))
    city =            models.CharField(max_length=500, blank=True)
    # PASSWORD
    password =        models.CharField(max_length=500, blank=True)
    # PERMISION
    is_admin =        models.BooleanField(default=False)  
    is_active =       models.BooleanField(default=False)
    was_active =      models.BooleanField(default=False)
    is_manager =      models.BooleanField(default=False)
    is_client =       models.BooleanField(default=False)
    corporate =       models.BooleanField(default=False)
        
    # DATETIME
    birthday =        models.DateTimeField(null=True, blank=True, verbose_name=_("День рождения"))
    created =         models.DateTimeField(default=now)

    objects = CustomUserManager()
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-created']
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    
    def save(self, *args, **kwargs):
        super(CustomUser, self).save()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def is_staff(self):
        return self.is_admin

    def adress_list(self):
        
        return user



class Wishlist(models.Model):
    user =    models.ForeignKey(CustomUser,          on_delete=models.CASCADE, verbose_name=_("Пользователь"), related_name='products')
    product = models.ForeignKey('catalogue.Product', on_delete=models.CASCADE, verbose_name=_("Товар"))
    date =    models.DateTimeField(default=now)

    class Meta:
        ordering = ['-date']
        unique_together = [['user', 'product']]

    def __str__(self):
        return ''




class UserAdress(models.Model):
    parent =     models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="adress")
    city =       models.CharField(max_length=500, verbose_name=_("Город"))
    street =     models.CharField(max_length=500, verbose_name=_("Улица"))
    house =      models.CharField(max_length=500, verbose_name=_("Дом"))
    appartment = models.CharField(max_length=500, verbose_name=_("Квартира / Офис"))

    def __str__(self):
        return f'г. {self.city}, ул. {self.street} {self.house}, кв. {self.appartment}'

    def save(self):
        super(UserAdress, self).save()
        if not hasattr(self.parent, 'adress_chosen'):
            chosen = UserAdressChosen(parent = self.parent, adress=self)
            chosen.save()


class UserAdressChosen(models.Model):
    parent =     models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='adress_chosen')
    adress =     models.ForeignKey(UserAdress, on_delete=models.CASCADE)



class UserNP(models.Model):
    parent =     models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="np")
    city =       models.CharField(max_length=500)
    branch =     models.CharField(max_length=500)

    def __str__(self):
        return ' '.join([self.city, self.branch])

class UserNPChosen(models.Model):
    parent =     models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="np_chosen")
    adress =     models.ForeignKey(UserNP, on_delete=models.CASCADE)


class UserCompany(models.Model):
    parent =   models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="company")
    name =     models.CharField(max_length=500, blank=True, editable=True, verbose_name=_("Название"))
    code =     models.CharField(max_length=500, blank=True, editable=True, verbose_name=_("ЕДРПОУ"))
    email =    models.EmailField(blank=False, unique=True, max_length=500, verbose_name=_("Корпоративный E-mail"))
    iban =     models.CharField(max_length=500, blank=True, editable=True, verbose_name=_("Номер счета (IBAN)"))
    director = models.CharField(max_length=500, blank=True, editable=True, verbose_name=_("ФИО Директора"))
    adress =   models.CharField(max_length=500, blank=True, editable=True, verbose_name=_("Юридический адрес"))



class UserSubscripton(models.Model):
    parent =   models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="subscription")
    category = models.ManyToManyField('catalogue.Category', related_name="subscription")

    def __str__(self):
        return ', '.join([category.name for category in self.category.all()])

    class Meta:
        verbose_name = _('Подписка на категории')
        verbose_name_plural = _('Подписка на категории')
