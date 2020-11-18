from django import forms
from courses.models import Course

# form for students to enroll on courses
class CourseEnrollForm(forms.Form):
    # course field is for the course on which the user will be enrolled; therefore, it's a ModelChoiceField
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
# a HiddenInput widget because you are not going to show this field tothe user. You are going to use this form in the CourseDetailView view to display a button to enroll
                                    widget=forms.HiddenInput)
