# Generated by Django 3.1.1 on 2021-05-09 03:46

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('year', models.IntegerField(blank=True)),
                ('picture', models.TextField(blank=True)),
                ('gender', models.TextField(blank=True)),
                ('american_indian_or_alaska_native', models.BooleanField(blank=True, default=False)),
                ('asian', models.BooleanField(blank=True, default=False)),
                ('black_or_african_american', models.BooleanField(blank=True, default=False)),
                ('hispanic_or_latino', models.BooleanField(blank=True, default=False)),
                ('middle_eastern', models.BooleanField(blank=True, default=False)),
                ('native_hawaiian_or_other_pacific_islander', models.BooleanField(blank=True, default=False)),
                ('white', models.BooleanField(blank=True, default=False)),
                ('other', models.BooleanField(blank=True, default=False)),
                ('major', models.TextField(blank=True)),
                ('minor', models.TextField(blank=True)),
                ('modification', models.TextField(blank=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('role', models.TextField(blank=True)),
                ('home', models.TextField(blank=True)),
                ('quote', models.TextField(blank=True)),
                ('favorite_shoe', models.TextField(blank=True)),
                ('favorite_artist', models.TextField(blank=True)),
                ('favorite_color', models.TextField(blank=True)),
                ('phoneType', models.TextField(blank=True)),
                ('follows', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likers', to='dali_connect.Post'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
