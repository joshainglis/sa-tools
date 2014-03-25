from bp_content.themes.sa_default.handlers import models
from bp_content.themes.sa_default.handlers.custom_fields import BetterTagListField, SupplierChoice

__author__ = 'coto'
"""
Created on June 10, 2012
@author: peta15
"""

from wtforms import fields, ValidationError
from wtforms import Form
from wtforms import validators
from webapp2_extras.i18n import lazy_gettext as _
from webapp2_extras.i18n import ngettext, gettext
from bp_includes.lib import utils
from custom_validators import AnyOfList


FIELD_MAXLENGTH = 50  # intended to stop maliciously long input
PHONE_MAXLENGTH = 15
TAGS = {'TAG1', 'TAG2', 'TAG3'}

NAME_FIELD_VALIDATORS = [validators.DataRequired(),
                         validators.Length(max=FIELD_MAXLENGTH,
                                           message=_("Field cannot be longer than %(max)d characters.")),
                         validators.regexp(utils.NAME_LASTNAME_REGEXP,
                                           message=_("Name invalid. Use only letters and numbers."))]
EMAIL_FIELD_VALIDATORS = [validators.DataRequired(),
                          validators.Length(min=8, max=FIELD_MAXLENGTH, message=_(
                              "Field must be between %(min)d and %(max)d characters long.")),
                          validators.regexp(utils.EMAIL_REGEXP, message=_('Invalid email address.'))]
PHONE_FIELD_VALIDATORS = [validators.length(max=PHONE_MAXLENGTH,
                                            message=_('Phone invalid. Should be less than %(max)s '
                                                      'character long.'))]
WEBSITE_FIELD_VALIDATORS = [validators.Length(max=FIELD_MAXLENGTH,
                                              message=_('Field cannot be longer than %(max)d characters.'))]
NOTES_FIELD_VALIDATORS = [validators.Length(max=65536)]
PASSWORD_FIELD_VALIDATORS = [validators.DataRequired(),
                             validators.Length(max=FIELD_MAXLENGTH, message=_(
                                 "Field cannot be longer than %(max)d characters."))]
TAG_FIELD_VALIDATORS = [validators.Required(),
                        AnyOfList(TAGS)]
PRICE_FIELD_VALIDATORS = [validators.NumberRange(min=0.0)]


class FormTranslations(object):
    def gettext(self, string):
        return gettext(string)

    def ngettext(self, singular, plural, n):
        return ngettext(singular, plural, n)


class BaseForm(Form):
    def __init__(self, request_handler):
        super(BaseForm, self).__init__(request_handler.request.POST)

    def _get_translations(self):
        return FormTranslations()


class EmailMixin(BaseForm):
    email = fields.TextField(_('Email'), EMAIL_FIELD_VALIDATORS)


# ==== Forms ====

class DeleteAccountForm(BaseForm):
    password = fields.TextField(_('Password'), PASSWORD_FIELD_VALIDATORS, id='l_password')
    pass


class ContactForm(EmailMixin):
    name = fields.TextField(_('Name'), NAME_FIELD_VALIDATORS)
    message = fields.TextAreaField(_('Message'), [validators.Required(), validators.Length(max=65536)])
    pass


class SupplierForm(BaseForm):
    created = fields.HiddenField()
    created_by = fields.HiddenField()
    updated = fields.HiddenField()
    updated_by = fields.HiddenField()
    name = fields.TextField(_('Name'), NAME_FIELD_VALIDATORS)
    email = fields.TextField(_('Email'), EMAIL_FIELD_VALIDATORS)
    phone = fields.TextField(_('Phone'), PHONE_FIELD_VALIDATORS)
    website = fields.TextField(_('Website'), WEBSITE_FIELD_VALIDATORS)
    notes = fields.TextAreaField(_('Message'), NOTES_FIELD_VALIDATORS)
    pass


class AidForm(BaseForm):
    created = fields.HiddenField()
    created_by = fields.HiddenField()
    updated = fields.HiddenField()
    updated_by = fields.HiddenField()
    name = fields.TextField(_('Name'), NAME_FIELD_VALIDATORS)
    cost = fields.FloatField(_('Cost'), [validators.Required()] + PRICE_FIELD_VALIDATORS)
    installation = fields.FloatField(_('Installation'), PRICE_FIELD_VALIDATORS)
    postage = fields.FloatField(_('Postage'), PRICE_FIELD_VALIDATORS)
    notes = fields.TextAreaField(_('Message'), NOTES_FIELD_VALIDATORS)
    supplier = SupplierChoice(_('Supplier'), coerce=int)
    tags = BetterTagListField(_('Tags'), TAG_FIELD_VALIDATORS)
    pass
