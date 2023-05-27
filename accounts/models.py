from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from django.contrib.auth.models import AbstractUser
from django.db import models

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
# class User(AbstractUser):
#     class Meta(AbstractUser.Meta):
#         db_table    = 'custom_users'

#     uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     age = models.IntegerField(verbose_name="年齢",default=20)

GENDER_CHOICES = (
    ('0', ''),
    ('1', '男性'),
    ('2', '女性'),
)

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Users must have an user-ID')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_staff(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Stuff must have is_staff=True.')
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Administrator must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Administrator must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    screen_user_id_validator = ASCIIUsernameValidator() # 日本語は使えない
    username = models.CharField(
        _('ユーザーID'),
        max_length=50,
        unique=True,
        help_text=_('入力必須。半角英数字と一部の記号、かつ50字以内'),
        validators=[screen_user_id_validator],
        error_messages={
            'unique': _("そのユーザーIDは既に別のユーザーが使用しています。"),
        },
    )

    email = models.EmailField(_('Emailアドレス'), unique=True)
    # wrong_pw: パスワードを間違えた回数をカウントする
    wrong_pw = models.DecimalField(max_digits=1, decimal_places=0, default= 0)
    # password_lock: パスワードを連続3回間違うと、1時間パスワードを入力できないようにするためのフィールド
    password_lock = models.DateTimeField(blank=True, null=True)
    # certificated_at: メールの本人確認をした時点を保存するためのフィールド
    certificated_at = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    handle_name_validator = UnicodeUsernameValidator() # 日本語を使える
    handle_name = models.CharField(_('ハンドルネーム'),
                                    default='名無しさん',
                                    max_length=30,
                                    validators=[handle_name_validator],
                                    )
    self_introduction = models.CharField(_('プロフィール文'), 
                                        max_length=200, 
                                        null=True, 
                                        blank=True,
                                        )

    icon = models.ImageField(_('icon'), 
                            blank=True, 
                            default     ='default/piyopiyo.png',
                            upload_to   ='uploads/icon/%Y/%m/%d/',
                            height_field='url_icon_height',
                            width_field ='url_icon_width',
                            )
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'
        swappable = 'AUTH_USER_MODEL'
        #abstract = True # 

    def get_absolute_url(self):
        return reverse('snsapp:detail', kwargs={'username': self.username})

    def __str__(self):
        return str(self.id)

    def clean_email(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # @property
    # def is_staff(self):
    #     return self.is_superuser

    # 以下はアイコンのサイズ指定・形式指定
    big_icon = ImageSpecField(
        source="icon",
        processors=[ResizeToFill(1280, 1024)],
        format='JPEG'
    )
    thumbnail_icon = ImageSpecField(
        source='icon',
        processors=[ResizeToFill(250,250)],
        format="JPEG",
        options={'quality': 60}
    )
    middle_icon = ImageSpecField(
        source='icon',
        processors=[ResizeToFill(600, 400)],
        format="JPEG",
        options={'quality': 75}
    )
    small_icon= ImageSpecField(
        source='icon',
        processors=[ResizeToFill(75,75)],
        format="JPEG",
        options={'quality': 50}
    )
    url_icon_height = models.IntegerField(
        editable=False, default=200
    )
    url_icon_width = models.IntegerField(
        editable=False, default=200
    )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(_('生年月日'), null=True, blank=True)
    gender = models.CharField(
        _('性別'), max_length=2, choices=GENDER_CHOICES, blank=True)
    header_pic = models.ImageField(_('header_pic'), blank       =True,     
                                                    default     ='uploads/header_pic/default/default.png',
                                                    upload_to   ='uploads/header_pic/%Y/%m/%d/',
                                                    height_field='url_header_pic_height',
                                                    width_field ='url_header_pic_width',
    )
    class Meta:
        db_table = "profiles"
        verbose_name = _('profile')

    def __str__(self):
        return str(self.user.username)

    # 以下はヘッダー画像のサイズ指定・形式指定
    big_header_pic = ImageSpecField(
        source="header_pic",
        processors=[ResizeToFill(1280, 1024)],
        format='JPEG'
    )
    thumbnail_header_pic = ImageSpecField(
        source='header_pic',
        processors=[ResizeToFill(250,250)],
        format="JPEG",
        options={'quality': 60}
    )
    middle_header_pic = ImageSpecField(
        source='header_pic',
        processors=[ResizeToFill(600, 400)],
        format="JPEG",
        options={'quality': 75}
    )
    small_header_pic = ImageSpecField(
        source='header_pic',
        processors=[ResizeToFill(75,75)],
        format="JPEG",
        options={'quality': 50}
    )
    url_header_pic_height = models.IntegerField(
        editable=False, default=200
    )
    url_header_pic_width = models.IntegerField(
        editable=False, default=200
    )

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """ 新ユーザー作成時に空のprofileも作成する """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    