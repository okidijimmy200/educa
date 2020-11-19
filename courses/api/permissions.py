from rest_framework.permissions import BasePermission

# subclass the BasePermission class
class IsEnrolled(BasePermission):
    # override the has_object_ permission().
    def has_object_permission(self, request, view, obj):
# check that the user performing the request is present in the students relationship of the Course object
        return obj.students.filter(id=request.user.id).exists()
