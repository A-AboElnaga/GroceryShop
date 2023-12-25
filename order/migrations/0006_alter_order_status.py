# Generated by Django 4.2.8 on 2023-12-18 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_orderline_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(0, 'Fullfield'), (1, 'Unfullfield'), (3, 'Canceled'), (4, 'Refunded')], default=0),
        ),
    ]