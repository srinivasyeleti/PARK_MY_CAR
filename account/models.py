from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class AccountManager(BaseUserManager) :
    def create_user(self, email, username, password = None) :
        if not email :
            raise ValueError("please provide a valid email...")
        if not username :
            raise ValueError("please provide a valid username...")

        else :
            user = self.model(
                email = self.normalize_email(email),
                username = username,
            )

            user.save(using = self._db)

            return user

    def create_superuser(self, email, username, password) :
        if not email :
            raise ValueError("please provide a valid email...")
        if not username :
            raise ValueError("please provide a valid username...")

        else :
            superuser = self.model(
                email = self.normalize_email(email),
                username = username,
                password = password,
            )

            superuser.is_admin = True
            superuser.is_staff = True
            superuser.is_superuser= True

            superuser.set_password(password)
            superuser.save(using = self._db)

            return superuser

class Account(AbstractBaseUser) :
    email = models.CharField(max_length=30, unique=True)
    username = models.CharField(max_length=30, unique=True)
    # booked_slot = models.BooleanField(default = False)
    # slot_id = models.CharField(max_length=10, null=True)

    date_joined = models.DateTimeField(verbose_name = "date_joined", auto_now_add = True)
    last_login = models.DateTimeField(verbose_name = "last_login", auto_now = True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)


    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self) :
        return self.username

    
    def has_perm(self, perm, obj = None) :
        return self.is_admin

    def has_module_perms(self, app_label) :
        return True