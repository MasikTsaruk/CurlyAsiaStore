from django.db import models
from django.urls import reverse
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_PRIVATE_KEY


class Category(models.Model):
        name = models.CharField(max_length=200, default='char_field')
        slug = models.SlugField(max_length=200, unique=True, default='slug_field')

        def get_absolute_url(self):
            return reverse('shop:product_list_by_category', args=[self.slug])

        class Meta:
            ordering = ['name']
            indexes = [models.Index(fields=['name']), ]
            verbose_name = 'category'
            verbose_name_plural = 'categories'

        def __str__(self):
            return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    class Meta:
        ordering = ['name']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='usd'
        )
        return stripe_product_price

    indexes = [
        models.Index(fields=['id', 'slug']),
        models.Index(fields=['name']),
        models.Index(fields=['-created']),
    ]

    def __str__(self):
        return self.name
