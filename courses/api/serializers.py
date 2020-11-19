from rest_framework import serializers
from ..models import Subject
from ..models import Course, Module, Content

# This is the serializer for the Subject model.
class SubjectSerializer(serializers.ModelSerializer):
# The Meta class allows you to specify the model to serialize and the fields to be included for serialization. All model fields will be included if you don't set a fields attribute
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']

# You want to include more information about each module, so you need to serialize Module objects and nest them
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
# add a modules attribute to CourseSerializer to nest the ModuleSerializer serializer. You set many=True to indicate that you are serializing multiple objects.
# The read_only parameter indicates that this field is read-only and should not be included in any input to create or update objects
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview',
                  'created', 'owner', 'modules']


class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']

class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules']
