from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# you use the @login_required decorator to prevent any non-authenticated user from accessing the view
@login_required
# course_chat_room view.
# The view receives a required course_id parameter that is used to retrieve the course with the given id.
def course_chat_room(request, course_id):
    try:
        # retrieve course  with given id joined by the current user
# You access the courses that the user is enrolled on through the relationship courses_ joined and you retrieve the course with the given id from that subset of courses
        course = request.user.courses_joined.get(id=course_id)
    except:
# If the course with the given id does not exist or the user is not enrolled on it, you return an HttpResponseForbidden response, which translates to an HTTP response with status 403
        # user is not a student of the course or course does not exist
        return HttpResponseForbidden()
# If the course with the given id exists and the user is enrolled on it, you render the chat/room.html template, passing the course object to the template context.
    return render(request, 'chat/room.html', {'course': course})
