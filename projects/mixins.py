from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Project, Assignment

class ProjectRoleRequiredMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
            
        project_id = kwargs.get('project_id') or kwargs.get('pk')
        if not project_id:
            raise PermissionDenied
            
        project = get_object_or_404(Project, pk=project_id)
        
        try:
            assignment = Assignment.objects.get(user=request.user, project=project)
        except Assignment.DoesNotExist:
            raise PermissionDenied
            
        if self.allowed_roles and assignment.role.name not in self.allowed_roles:
            raise PermissionDenied
            
        return super().dispatch(request, *args, **kwargs)
