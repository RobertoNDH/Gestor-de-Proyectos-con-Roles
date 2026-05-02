from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    pass

class Project(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='assignments')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} en {self.project.name} como {self.role.name if self.role else 'Sin rol'}"

class Task(models.Model):
    STATUS_CHOICES = [
        ('por_hacer', 'Por hacer'),
        ('en_progreso', 'En progreso'),
        ('completado', 'Completado'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='por_hacer')
    due_date = models.DateField()

    def __str__(self):
        return self.title

class Message(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.sender.username} en {self.project.name}"
