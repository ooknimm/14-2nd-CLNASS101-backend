# Generated by Django 3.1.3 on 2021-01-13 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kit', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'apply_channels',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('discount_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_kit_free', models.BooleanField(default=False)),
                ('expire_date', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product')),
                ('sub_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.subcategory')),
            ],
            options={
                'db_table': 'coupons',
            },
        ),
        migrations.CreateModel(
            name='ProductLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'db_table': 'product_likes',
            },
        ),
        migrations.CreateModel(
            name='RecentlyView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'db_table': 'recently_views',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('nick_name', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=200, null=True)),
                ('phone_number', models.CharField(max_length=50)),
                ('is_creator', models.BooleanField(default=False, null=True)),
                ('profile_image', models.URLField(max_length=1000, null=True)),
                ('is_benefit', models.BooleanField(default=False)),
                ('point', models.IntegerField(default=0)),
                ('etc_channel', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('application_channel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.applychannel')),
                ('community_like', models.ManyToManyField(related_name='community_like_user', through='product.CommunityLike', to='product.Community')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user')),
            ],
            options={
                'db_table': 'users_products',
            },
        ),
        migrations.CreateModel(
            name='UserCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'users_coupons',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='coupon',
            field=models.ManyToManyField(through='user.UserCoupon', to='user.Coupon'),
        ),
        migrations.AddField(
            model_name='user',
            name='kit_like',
            field=models.ManyToManyField(through='kit.KitLike', to='kit.Kit'),
        ),
        migrations.AddField(
            model_name='user',
            name='product_like',
            field=models.ManyToManyField(related_name='product_like_user', through='user.ProductLike', to='product.Product'),
        ),
        migrations.AddField(
            model_name='user',
            name='recently_view',
            field=models.ManyToManyField(related_name='product_view_user', through='user.RecentlyView', to='product.Product'),
        ),
        migrations.AddField(
            model_name='user',
            name='recommend',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_product',
            field=models.ManyToManyField(related_name='product_buy_user', through='user.UserProduct', to='product.Product'),
        ),
        migrations.AddField(
            model_name='recentlyview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AddField(
            model_name='productlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]
