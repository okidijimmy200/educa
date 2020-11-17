from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module

# Inline formsets are a small abstraction on top of formsets that simplify working with related objects. This function allows
# you to build a model formset dynamically for the Module objects related to a Course object.
ModuleFormSet = inlineformset_factory(Course,
                                      Module,
# fields: The fields that will be included in each form of the formset.
                                      fields=['title',
                                              'description'],
# extra: Allows you to set the number of empty extra forms to display in the formset.
                                      extra=2,
# can_delete: If you set this to True, Django will include a Boolean field for each form that will be rendered as a checkbox input. It allows you to mark the objects that you want to delete.
                                      can_delete=True)
