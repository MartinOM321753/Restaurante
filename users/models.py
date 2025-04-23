from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from role.models import Role  # Importa el modelo de roles


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role=role, **extra_fields)
        user.set_password(password)  # Usa set_password para manejar el hash
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Asigna el rol de ADMIN automáticamente al superusuario
        admin_role, created = Role.objects.get_or_create(name="ADMIN")
        return self.create_user(email, name, password, role=admin_role, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    startDate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'email'  # Campo usado para autenticación
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.role}"
