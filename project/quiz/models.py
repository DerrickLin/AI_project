from django.db import models
import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

#商品類別
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


#顧客資訊
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=10, blank=True, null=True)

    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # 新增的 is_staff 欄位

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class YourModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # 其他模型字段和方法

    class Meta:
        app_label = 'quiz'
        
        
#商品資訊        
class product(models.Model):
    pId=models.CharField(max_length=10,null=False)
    pName=models.CharField(max_length=20,null=False)
    pImage = models.ImageField(upload_to='uploads/product/', blank=True)
    pCost=models.PositiveIntegerField(blank=False)
    pCategory=models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    pManufacture=models.CharField(max_length=20,null=False)
    pLoc=models.CharField(max_length=20, blank=True)
    pQuantity=models.PositiveIntegerField(blank=False)
    
    def __str__(self):
        return self.pName
    
    
# 訂單資訊   
class order(models.Model):
    oId=models.CharField(max_length=10,null=False)
    oDate=models.DateTimeField(default=datetime.datetime.today)
    #oProduct=models.CharField(max_length=200, null=False, default=None)
    oProduct=models.ManyToManyField(product)
    oClient=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    oCost=models.PositiveIntegerField(blank=False)
    order_quantity = models.IntegerField(default=1)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f"Order #{self.oId}"


class Feedback(models.Model):
    feedback_content = models.TextField(max_length=300, blank=True)
    write_date = models.DateTimeField(default=datetime.datetime.today)
    who_write = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.feedback_content