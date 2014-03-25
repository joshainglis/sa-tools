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


class Supplier(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    created_by = ndb.UserProperty(auto_current_user_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    updated_by = ndb.UserProperty(auto_current_user=True)
    name = ndb.StringProperty(required=True)
    email = EmailProperty(required=False)
    phone = PhoneProperty(required=False)
    website = ndb.TextProperty(required=False)
    notes = ndb.TextProperty(required=False)


class Aid(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    created_by = ndb.UserProperty(auto_current_user_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    updated_by = ndb.UserProperty(auto_current_user=True)
    name = ndb.StringProperty(required=True)
    cost = PriceProperty(required=True)
    installation = PriceProperty(required=False, default=0.0)
    postage = PriceProperty(required=False, default=0.0)
    notes = ndb.TextProperty(required=False)
    supplier = ndb.KeyProperty(kind=Supplier)
    tags = ndb.StringProperty(repeated=True)



