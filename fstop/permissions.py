from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a Client to access it.
    A client is owned by the user who created it.
    """
    
    def has_object_permission(self, request, view, obj):
        # For Client objects, check if the user owns the client
        return obj.user == request.user


class IsClientOwnerViaProject(permissions.BasePermission):
    """
    Custom permission to check that the user owns the client that this object's project is linked to.
    This permission is used for Project, Booking, and Gallery objects.
    
    Authorization chain:
    - Project → Project.client.user
    - Booking → Booking.project.client.user
    - Gallery → Gallery.project.client.user
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if the object has a 'project' attribute (Booking or Gallery)
        if hasattr(obj, 'project'):
            # Follow the chain: Booking/Gallery → Project → Client → User
            return obj.project.client.user == request.user
        # Check if the object is a Project (has 'client' attribute)
        elif hasattr(obj, 'client'):
            # Follow the chain: Project → Client → User
            return obj.client.user == request.user
        # Deny access if structure doesn't match expected pattern
        return False
