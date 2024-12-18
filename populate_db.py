import os
import django
import random
from decimal import Decimal
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamman.settings')
django.setup()

from store.models import Category, Manufacturer, Product
from django.contrib.auth.models import User

# Создание категорий медицинского оборудования
categories = [
    'Диагностическое оборудование',
    'Хирургическое оборудование',
    'Ортопедические изделия',
    'Лабораторное оборудование',
    'Реабилитационные устройства',
    'Стоматологическое оборудование',
    'Кардиологическое оборудование',
    'Оборудование для интенсивной терапии',
    'Эндоскопическое оборудование',
    'Физиотерапевтическое оборудование'
]

for cat_name in categories:
    Category.objects.get_or_create(name=cat_name, slug=slugify(cat_name))

# Создание производителей медицинского оборудования
manufacturers = [
    'Medtronic',
    'Siemens Healthineers',
    'GE Healthcare',
    'Philips Healthcare',
    'Johnson & Johnson Medical Devices',
    'Boston Scientific',
    'Abbott Laboratories',
    'Baxter International',
    'B. Braun Melsungen',
    'Smith & Nephew'
]

for man_name in manufacturers:
    Manufacturer.objects.get_or_create(name=man_name)

# Список продуктов медицинского оборудования
products = [
    {
        'name': 'Аппарат УЗИ GE Vivid S60N',
        'category': 'Диагностическое оборудование',
        'manufacturer': 'GE Healthcare',
        'price': Decimal('1500000.00'),
        'description': 'Современный ультразвуковой аппарат для кардиологии.'
    },
    {
        'name': 'МРТ-сканер Siemens Magnetom Aera',
        'category': 'Диагностическое оборудование',
        'manufacturer': 'Siemens Healthineers',
        'price': Decimal('45000000.00'),
        'description': 'Высокопольный МРТ-сканер с напряженностью магнитного поля 1,5 Тл.'
    },
    # Добавьте больше продуктов здесь...
]

# Генерация дополнительных продуктов
additional_products = []

for i in range(1, 51):  # Добавим 50 дополнительных продуктов
    category = random.choice(categories)
    manufacturer = random.choice(manufacturers)
    name = f'{category} Продукт {i}'
    product = {
        'name': name,
        'category': category,
        'manufacturer': manufacturer,
        'price': Decimal(random.randint(500000, 5000000)),
        'description': f'Описание для {name}. Высококачественное медицинское оборудование.'
    }
    additional_products.append(product)

# Объединяем списки продуктов
products.extend(additional_products)

# Создание продуктов
for item in products:
    category = Category.objects.get(name=item['category'])
    manufacturer = Manufacturer.objects.get(name=item['manufacturer'])
    product, created = Product.objects.get_or_create(
        name=item['name'],
        slug=slugify(item['name']),
        defaults={
            'description': item['description'],
            'price': item['price'],
            'category': category,
            'manufacturer': manufacturer,
            'available': True,
            'stock': random.randint(1, 50),
            'is_special_offer': random.choice([True, False])
        }
    )
    # Вы можете добавить изображение по умолчанию, если необходимо

print("База данных успешно заполнена медицинским оборудованием!")
