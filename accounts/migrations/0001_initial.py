# Generated by Django 4.2.1 on 2023-05-27 09:23

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(error_messages={'unique': 'そのユーザーIDは既に別のユーザーが使用しています。'}, help_text='入力必須。半角英数字と一部の記号、かつ50字以内', max_length=50, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='ユーザーID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Emailアドレス')),
                ('wrong_pw', models.DecimalField(decimal_places=0, default=0, max_digits=1)),
                ('password_lock', models.DateTimeField(blank=True, null=True)),
                ('certificated_at', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('handle_name', models.CharField(default='名無しさん', max_length=30, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='ハンドルネーム')),
                ('self_introduction', models.CharField(blank=True, max_length=200, null=True, verbose_name='プロフィール文')),
                ('icon', models.ImageField(blank=True, default='default/piyopiyo.png', height_field='url_icon_height', upload_to='uploads/icon/%Y/%m/%d/', verbose_name='icon', width_field='url_icon_width')),
                ('url_icon_height', models.IntegerField(default=200, editable=False)),
                ('url_icon_width', models.IntegerField(default=200, editable=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'users',
                'swappable': 'AUTH_USER_MODEL',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='生年月日')),
                ('gender', models.CharField(blank=True, choices=[('0', ''), ('1', '男性'), ('2', '女性')], max_length=2, verbose_name='性別')),
                ('header_pic', models.ImageField(blank=True, default='uploads/header_pic/default/default.png', height_field='url_header_pic_height', upload_to='uploads/header_pic/%Y/%m/%d/', verbose_name='header_pic', width_field='url_header_pic_width')),
                ('url_header_pic_height', models.IntegerField(default=200, editable=False)),
                ('url_header_pic_width', models.IntegerField(default=200, editable=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'db_table': 'profiles',
            },
        ),
    ]
