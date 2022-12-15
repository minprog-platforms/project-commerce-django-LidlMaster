# Generated by Django 4.1.3 on 2022-12-14 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_grouping_category_category_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_Name',
            new_name='categoryName',
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.category'),
        ),
    ]