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
# from .permissions import IsEnrolled

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


# class CourseViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

#     @action(detail=True,
#             methods=['post'],
#             authentication_classes=[BasicAuthentication],
#             permission_classes=[IsAuthenticated])
#     def enroll(self, request, *args, **kwargs):
#         course = self.get_object()
#         course.students.add(request.user)
#         return Response({'enrolled': True})

#     @action(detail=True,
#             methods=['get'],
#             serializer_class=CourseWithContentsSerializer,
#             authentication_classes=[BasicAuthentication],
#             permission_classes=[IsAuthenticated, IsEnrolled])
#     def contents(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
