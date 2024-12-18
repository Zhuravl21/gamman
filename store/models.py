from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField("Категория", max_length=255)
    slug = models.SlugField("URL", max_length=255, unique=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE,
        verbose_name="Родительская категория"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.slug])

class Manufacturer(models.Model):
    name = models.CharField("Производитель", max_length=255)

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
        ordering = ('name',)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField("URL", max_length=255, unique=True)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField("Изображение", upload_to='products/')
    available = models.BooleanField("Доступно", default=True)
    stock = models.PositiveIntegerField("Количество на складе", default=0)
    specifications = models.TextField("Технические характеристики", blank=True)
    instructions = models.FileField("Инструкции", upload_to='instructions/', blank=True)
    certificates = models.FileField("Сертификаты", upload_to='certificates/', blank=True)
    is_special_offer = models.BooleanField("Специальное предложение", default=False)
    manufacturer = models.ForeignKey(
        Manufacturer,
        related_name='products',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Производитель"
    )
    discount = models.DecimalField("Скидка %", max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def get_discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

class Banner(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    subtitle = models.CharField("Подзаголовок", max_length=200, blank=True)
    image = models.ImageField("Изображение", upload_to='banners/')
    link = models.URLField("Ссылка", blank=True, null=True)
    button_text = models.CharField("Текст кнопки", max_length=50, default="Подробнее")
    is_active = models.BooleanField("Активен", default=True)
    order = models.IntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']

class Promotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField("Оценка", default=5)
    comment = models.TextField("Комментарий")
    created = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ('-created',)

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'

class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='subscriptions', on_delete=models.CASCADE)
    created = models.DateTimeField("Дата подписки", auto_now_add=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} subscribed to {self.product.name}'
