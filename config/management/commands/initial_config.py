from django.core.management.base import BaseCommand
from role.models import Role
from users.models import User

class Command(BaseCommand):
    help = 'Crea roles y usuarios por defecto'

    def handle(self, *args, **kwargs):
        roles = ['ADMIN', 'RESTAURANT_OWNER', 'USER']
        created_roles = {}

        for role_name in roles:
            role, created = Role.objects.get_or_create(name=role_name)
            created_roles[role_name] = role
            if created:
                self.stdout.write(self.style.SUCCESS(f'Rol "{role_name}" creado.'))
            else:
                self.stdout.write(f'Rol "{role_name}" ya existe.')

        # Crear usuario administrador
        admin_email = 'admin@correo.com'
        admin_password = '1234'
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                name='Administrador',
                password=admin_password
            )
            self.stdout.write(self.style.SUCCESS('Usuario administrador creado.'))
        else:
            self.stdout.write('Usuario administrador ya existe.')

        # Crear usuario normal
        user_email = 'user@correo.com'
        user_password = '1234'
        if not User.objects.filter(email=user_email).exists():
            User.objects.create_user(
                email=user_email,
                name='Usuario Normal',
                password=user_password,
                role=created_roles['USER']
            )
            self.stdout.write(self.style.SUCCESS('Usuario normal creado.'))
        else:
            self.stdout.write('Usuario normal ya existe.')

        # Mostrar accesos al final
        self.stdout.write(self.style.WARNING('\n---- ACCESOS GENERADOS ----'))
        self.stdout.write(self.style.WARNING(f'Admin:\n  Email: {admin_email}\n  Contraseña: {admin_password}'))
        self.stdout.write(self.style.WARNING(f'Usuario:\n  Email: {user_email}\n  Contraseña: {user_password}'))
