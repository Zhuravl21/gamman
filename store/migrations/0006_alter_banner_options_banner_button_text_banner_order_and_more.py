# Generated by Django 5.1.3 on 2024-12-05 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_category_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='banner',
            name='button_text',
            field=models.CharField(default='Подробнее', max_length=50, verbose_name='Текст кнопки'),
        ),
        migrations.AddField(
            model_name='banner',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Порядок'),
        ),
        migrations.AddField(
            model_name='banner',
            name='subtitle',
            field=models.CharField(blank=True, max_length=200, verbose_name='Подзаголовок'),
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Скидка %'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(upload_to='banners/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Заголовок'),
        ),
    ]
