# -*- coding:utf8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from oauth2_provider.models import AccessToken
from horizon.models import model_to_dict
from django.conf import settings

from horizon import main
import datetime
import os


def make_token_expire(request):
    """
    置token过期
    """
    header = request.META
    token = header['HTTP_AUTHORIZATION'].split()[1]
    try:
        _instance = AccessToken.objects.get(token=token)
        _instance.expires = now()
        _instance.save()
    except:
        pass
    return True


class BusinessUserManager(BaseUserManager):
    pass

USER_PICTURE_DIR = settings.PICTURE_DIRS['business']['head_picture']


class BusinessUser(AbstractBaseUser):
    # username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True,
    )
    business_name = models.CharField(u'商户名称', max_length=100, default='')
    food_court_id = models.IntegerField(u'所属美食城', default=0)
    phone = models.CharField(u'手机号', max_length=20, unique=True, db_index=True)
    brand = models.CharField(u'所属品牌', max_length=60, null=False, default='')
    manager = models.CharField(u'经理人姓名', max_length=20, null=False, default='')
    chinese_people_id = models.CharField(u'身份证号码', max_length=25,
                                         null=False, default='')
    stalls_number = models.CharField(u'档口编号', max_length=20,
                                     null=False, default='')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)
    head_picture = models.ImageField(u'头像',
                                     upload_to=USER_PICTURE_DIR,
                                     default=os.path.join(USER_PICTURE_DIR, 'noImage.png'), )

    objects = BusinessUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['business_name']

    class Meta:
        db_table = 'ys_auth_user'
        unique_together = ('business_name', 'food_court_id')


ADVERT_PICTURE_DIR = settings.PICTURE_DIRS['business']['advert']


class AdvertPictureManager(models.Manager):
    def get(self, *args, **kwargs):
        kwargs['status'] = 1
        return super(AdvertPictureManager, self).get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        kwargs['status'] = 1
        return super(AdvertPictureManager, self).filter(*args, **kwargs)


class AdvertPicture(models.Model):
    food_court_id = models.IntegerField(u'美食城ID')
    name = models.CharField(u'图片名称', max_length=60, unique=True, db_index=True)
    image = models.ImageField(u'图片', upload_to=ADVERT_PICTURE_DIR,)

    # 数据状态：1：有效 2：已删除
    status = models.IntegerField(u'数据状态', default=1)
    created = models.DateTimeField(u'创建时间', default=now)
    updated = models.DateTimeField(u'更新时间', auto_now=True)

    objects = AdvertPictureManager()

    class Meta:
        db_table = 'ys_advert_picture'
        ordering = ['-created']

    def __unicode__(self):
        return self.name

    @classmethod
    def get_object(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except Exception as e:
            return e

    @classmethod
    def filter_objects(cls, **kwargs):
        try:
            return cls.objects.filter(**kwargs)
        except Exception as e:
            return e
