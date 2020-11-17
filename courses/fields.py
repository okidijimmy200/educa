from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# custom OrderField. It inherits from the PositiveIntegerField field provided by Django.
class OrderField(models.PositiveIntegerField):
# OrderField field takes an optional for_fields parameter that allows you to indicate the fields that the order has to be calculated with respect to.
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
# field overrides the pre_save() method of the PositiveIntegerField field, which is executed before saving the field into the database
    def pre_save(self, model_instance, add):
# You check whether a value already exists for this field in the model instance. You use self.attname, which is the attribute name given to the field in the
# model. If the attribute's value is different to None, you calculate the order you should give it as follows
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
# You build a QuerySet to retrieve all objects for the field's model. You retrieve the model class the field belongs to by accessing self.model.
                qs = self.model.objects.all()
                if self.for_fields:
# If there are any field names in the for_fields attribute of the field, you filter the QuerySet by the current value of the model fields in
# for_fields. By doing so, you calculate the order with respect to the given fields
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field)\
                    for field in self.for_fields}
# You retrieve the object with the highest order with last_item =qs.latest(self.attname) from the database. If no object is found, you assume this object is the first one and assign the order 0 to it.
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
# If an object is found, you add 1 to the highest order found.
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
# You assign the calculated order to the field's value in the model instance using setattr() and return it.
            setattr(model_instance, self.attname, value)
            return value
# If the model instance has a value for the current field, you use it instead of calculating it.
        else:
            return super().pre_save(model_instance, add)

'''When you create custom model fields, make them generic. Avoid
hardcoding data that depends on a specific model or field. Your
field should work in any model.'''
