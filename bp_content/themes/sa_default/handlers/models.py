# Put here your models or extend User model from bp_includes/models.py
from google.appengine.api.datastore_errors import BadValueError
import re
from bp_includes.models import User
from google.appengine.ext import ndb


class PriceProperty(ndb.FloatProperty):
    def _validate(self, value):
        value = super(PriceProperty, self)._validate(value)
        if value < 0.0:
            raise BadValueError("Price must be a positive number! You entered %s" % value)
        return value


class EmailProperty(ndb.StringProperty):
    EMAIL_REGEX = re.compile(
        r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
        r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")

    def _validate(self, value):
        super(EmailProperty, self)._validate(value)
        if not re.match(self.EMAIL_REGEX, value):
            raise BadValueError("%s is not a valid email address!")


class PhoneProperty(ndb.StringProperty):
    pass


class SAUser(User):
    pass


class HierarchicalTag(ndb.Model):
    name = ndb.StringProperty(required=True)
    parent = ndb.KeyProperty(required=True, kind='HierarchicalTag')


class BaseModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    created_by = ndb.UserProperty(auto_current_user_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    updated_by = ndb.UserProperty(auto_current_user=True)


class Accident(ndb.Model):
    date = ndb.DateProperty()
    location = ndb.StringProperty()
    notes = ndb.TextProperty()


class Injury(ndb.Model):
    date = ndb.DateProperty()
    notes = ndb.TextProperty()


class Address(ndb.Model):
    unit = ndb.StringProperty()
    address1 = ndb.StringProperty()
    address2 = ndb.StringProperty()
    suburb = ndb.StringProperty()
    state = ndb.StringProperty(choices=['QLD', 'NSW', 'VIC', 'WA', 'SA', 'NT', 'ACT'])


class Client(BaseModel):
    name_first = ndb.StringProperty(required=True)
    name_last = ndb.StringProperty(required=True)
    dob = ndb.DateProperty(required=True)
    sex = ndb.StringProperty(required=True, choices=["male", "female"])
    address = ndb.StructuredProperty(Address)
    contact = ndb.StringProperty()


class Supplier(BaseModel):
    name = ndb.StringProperty(required=True)
    email = ndb.TextProperty(required=False)
    phone = PhoneProperty(required=False)
    website = ndb.TextProperty(required=False)
    notes = ndb.TextProperty(required=False)


class Aid(BaseModel):
    name = ndb.StringProperty(required=True)
    cost = PriceProperty(required=True)
    maintenance = PriceProperty(required=False, default=0.0, verbose_name="Yearly Maintenance")
    replacement = ndb.FloatProperty(required=False, default=0.0, verbose_name="Years per replacement")
    installation = PriceProperty(required=False, default=0.0)
    postage = PriceProperty(required=False, default=0.0)
    notes = ndb.TextProperty(required=False)
    supplier = ndb.KeyProperty(kind=Supplier)
    tags = ndb.StringProperty(repeated=True)
    image = ndb.BlobKeyProperty()


class ImageModel(BaseModel):
    filename = ndb.StringProperty()
    extension = ndb.ComputedProperty(lambda self: self.filename.rsplit('.', 1)[1].lower())
    serving_url = ndb.StringProperty(default=None)


class SimplePriceModel(BaseModel):
    model_name = ndb.TextProperty()
    log_model = ndb.BooleanProperty(required=True, default=False)
    intercept = ndb.FloatProperty()
    slope = ndb.FloatProperty()


class PriceModelMixin(object):
    price_models = ndb.KeyProperty(kind=SimplePriceModel, repeated=True)


class CareSupplier(Supplier, PriceModelMixin):
    pass


class GratuitousCare(BaseModel, PriceModelMixin):
    state = ndb.StringProperty(choices=['QLD', 'NSW', 'VIC', 'WA', 'SA', 'NT', 'ACT'],
                               required=True)


class CareInstance(BaseModel):
    customer = ndb.KeyProperty(kind=Client)
    category = ndb.StringProperty(repeated=True)
    supplier = ndb.KeyProperty(kind=CareSupplier)
    price_model = ndb.KeyProperty(kind=SimplePriceModel)
    period = ndb.StringProperty()
    start = ndb.DateProperty(required=True)
    end = ndb.DateProperty(required=True)
    hours = ndb.FloatProperty()
    minutes = ndb.FloatProperty()
    per = ndb.StringProperty(choices=['D', 'W', 'M', 'A', 'TOTAL'])
    notes = ndb.TextProperty()


# class CareSupplierInstance(BaseModel):
#     supplier = ndb.KeyProperty(kind=CareSupplier)
#     care_instances = ndb.StructuredProperty(modelclass=CareInstance, repeated=True, required=True)

# class Care(BaseModel):
#     category = ndb.StringProperty()
#     care = ndb.StructuredProperty(modelclass=CareSupplierInstance, repeated=True, required=True)
#     pass
