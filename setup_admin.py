import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_manager.settings')
django.setup()

from projects.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'usuario123')
    print("Superusuario 'admin' creado exitosamente.")
else:
    print("El superusuario 'admin' ya existe.")
