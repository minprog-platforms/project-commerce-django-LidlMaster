# Generated by Django 4.1.3 on 2022-12-08 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_delete_bids_delete_comments_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Listings',
            new_name='Listing',
        ),
    ]