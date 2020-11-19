from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer, CourseWithContentsSerializer
from .permissions import IsEnrolled

# generic ListAPIView
class SubjectListView(generics.ListAPIView):
    # queryset: The base QuerySet to use to retrieve objects
    queryset = Subject.objects.all()
    # serializer_class: The class to serialize objects
    serializer_class = SubjectSerializer

# generic RetriveAPIView
class SubjectDetailView(generics.RetrieveAPIView):
# pk URL parameter for the detail view to retrieve the object for the given primary key.
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

# CourseEnrollView view handles user enrollment on courses
class CourseEnrollView(APIView): #You create a custom view that subclasses APIView.
# Users will be identified by the credentials set in the Authorization header of the HTTP request
    authentication_classes = (BasicAuthentication,)
# You include the IsAuthenticated permission. This will prevent anonymous users from accessing the view.
    permission_classes = (IsAuthenticated,)
# You define a post() method for POST actions. No other HTTP method will be allowed for this view
    def post(self, request, pk, format=None):
# You expect a pk URL parameter containing the ID of a course. You retrieve the course by the given pk parameter and raise a 404 exception if it's not found
        course = get_object_or_404(Course, pk=pk)
        # You add the current user to the students many-to-many relationship of the Course object and return a successful response.
        course.students.add(request.user)
        return Response({'enrolled': True})

# You subclass ReadOnlyModelViewSet, which provides the read-only actions list() and retrieve() to both list objects, or retrieves a single object
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
# add a custom enroll() method that represents an additional action for this viewset.
# use the action decorator of the framework with the parameter detail=True to specify that this is an action to be performed on a single object
    @action(detail=True,
# The decorator allows you to add custom attributes for the action. You specify that only the post() method is allowed for this view and set the authentication and permission classes
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
# use self.get_object() to retrieve the Course object
        course = self.get_object()
# add the current user to the students many-to-many relationship and return a custom success response
        course.students.add(request.user)
        return Response({'enrolled': True})
# a view that mimics the behavior of the retrieve() action, but includes the course contents
# You use the action decorator with the parameter detail=True to specify an action that is performed on a single object
    @action(detail=True,
            # You specify that only the GET method is allowed for this action
            methods=['get'],
# You use the new CourseWithContentsSerializer serializer class that includes rendered course contents
            serializer_class=CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
# You use both IsAuthenticated and your custom IsEnrolled permissions. By doing so, you make sure that only users enrolled on the course are able to access its contents
            permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        # use the existing retrieve() action to return the Course object
        return self.retrieve(request, *args, **kwargs)
