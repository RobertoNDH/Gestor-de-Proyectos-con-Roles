from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, Project, Assignment, Task, Message

admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Project)
admin.site.register(Assignment)
admin.site.register(Task)
admin.site.register(Message)
