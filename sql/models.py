import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

# カスタムユーザクラスを定義
class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    class Role(models.IntegerChoices):
        MANAGEMENT = 0
        GENERAL = 1
        PART_TIME = 2

    # 不要なフィールドはNoneにすることができる
    first_name = None
    last_name = None
    date_joined = None
    groups = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_number = models.CharField(
        unique=True,
        validators=[RegexValidator(r'^[0-9]{8}$')],
        max_length=8,
        # 管理者のログイン画面で社員番号と表示される
        verbose_name="社員番号",
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(max_length=254, unique=True)
    role = models.PositiveIntegerField(choices=Role.choices, default=Role.PART_TIME)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # デフォルトはusernameだが今回は社員番号を指定
    USERNAME_FIELD = "employee_number"
    # uniqueのemailとusernameを指定
    REQUIRED_FIELDS = ["email","username"]

    class Meta:
        ordering = ["employee_number"]
        db_table = "User"

    def __str__(self):
        return self.username


class Student(models.Model):
    class Grade(models.IntegerChoices):
        First = 0
        Second = 1
        Third = 2

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    height = models.DecimalField(max_digits=4, decimal_places=1)
    weight = models.DecimalField(max_digits=3, decimal_places=1)
    grade = models.PositiveIntegerField(choices=Grade.choices, default=Grade.First)
    birthday = models.DateField()
    club = models.ForeignKey("Club", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_updated_by')


class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_created_by')


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    selling_price = models.PositiveIntegerField(default=0)
    cost_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_updated_by')
