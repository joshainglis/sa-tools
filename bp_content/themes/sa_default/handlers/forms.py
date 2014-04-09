from bp_content.themes.sa_default.handlers import models
from bp_content.themes.sa_default.handlers.custom_fields import BetterTagListField, SupplierChoice, ClientChoice

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
EMAIL_FIELD_VALIDATORS = [validators.Length(min=0, max=FIELD_MAXLENGTH, message=_(
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

CARE_TYPE_CHOICES = [('Transfers', 'Transfers'),
                     ('Showering', 'Showering'),
                     ('Dressing', 'Dressing'),
                     ('Personal Care', 'Personal Care'),
                     ('Shopping', 'Shopping'),
                     ('Meal Preparation', 'Meal Preparation'),
                     ('Domestic Cleaning', 'Domestic Cleaning'),
                     ('Laundry', 'Laundry'),
                     ('Ironing', 'Ironing'),
                     ('Rubbish Removal', 'Rubbish Removal'),
                     ('Mail and Newspaper Collection', 'Mail and Newspaper Collection'),
                     ('Transportation', 'Transportation'),
                     ('Personal Support', 'Personal Support'),
                     ('Lawn Mowing', 'Lawn Mowing'),
                     ('Gardening', 'Gardening'),
                     ('Vehicle Cleaning', 'Vehicle Cleaning')]

class FormTranslations(object):
    def gettext(self, string):
        return gettext(string)

    def ngettext(self, singular, plural, n):
        return ngettext(singular, plural, n)


class BaseForm(Form):
    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        try:
            formdata = formdata.request.POST
        except AttributeError:
            pass
        super(BaseForm, self).__init__(formdata=formdata, obj=obj, prefix=prefix, **kwargs)

    def _get_translations(self):
        return FormTranslations()


class CreationDetailsMixin(object):
    created = fields.HiddenField()
    created_by = fields.HiddenField()
    updated = fields.HiddenField()
    updated_by = fields.HiddenField()


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


class SupplierForm(BaseForm, CreationDetailsMixin):
    name = fields.TextField(_('Name'), NAME_FIELD_VALIDATORS)
    email = fields.TextField(_('Email'), EMAIL_FIELD_VALIDATORS)
    phone = fields.TextField(_('Phone'), PHONE_FIELD_VALIDATORS)
    website = fields.TextField(_('Website'), WEBSITE_FIELD_VALIDATORS)
    notes = fields.TextAreaField(_('Message'), NOTES_FIELD_VALIDATORS)
    pass


class AidForm(BaseForm, CreationDetailsMixin):
    name = fields.TextField(_('Name'), NAME_FIELD_VALIDATORS)
    cost = fields.FloatField(_('Cost'), [validators.Required()] + PRICE_FIELD_VALIDATORS)
    maintenance = fields.FloatField(_('Yearly Maintenance'), PRICE_FIELD_VALIDATORS)
    replacement = fields.FloatField(_('Replacement'), PRICE_FIELD_VALIDATORS)
    installation = fields.FloatField(_('Installation'), PRICE_FIELD_VALIDATORS)
    postage = fields.FloatField(_('Postage'), PRICE_FIELD_VALIDATORS)
    notes = fields.TextAreaField(_('Message'), NOTES_FIELD_VALIDATORS)
    supplier = SupplierChoice(_('Supplier'), coerce=int)
    tags = BetterTagListField(_('Tags'), TAG_FIELD_VALIDATORS)
    pass


class AddressForm(BaseForm):
    unit = fields.TextField(label=_('Unit'))
    address_1 = fields.TextField(label=_('Unit'))
    address_2 = fields.TextField(label=_('Unit'))
    suburb = fields.TextField(label=_('Unit'))
    state = fields.SelectField(label=_('State'), choices=[('QLD', 'QLD'), 
                                                          ('NSW', 'NSW'), 
                                                          ('VIC', 'VIC'), 
                                                          ('WA', 'WA'), 
                                                          ('SA', 'SA'), 
                                                          ('NT', 'NT'), 
                                                          ('ACT', 'ACT')], default='QLD')


class ClientForm(BaseForm):
    name_first = fields.TextField(label=_('First Name'))
    name_last = fields.TextField(label=_('Last Name'))
    dob = fields.DateField(label=_("Date of Birth"))
    sex = fields.SelectField(label=_('Sex'), choices=[('male', _("Male")),
                                                      ('female', _('Female'))])
    address = fields.FormField(AddressForm)


class CareInstanceForm(BaseForm):
    date_start = fields.DateField(label=_('Start'))
    date_end = fields.DateField(label=_('End'))
    hours = fields.FloatField(label=_('Hours'))
    minutes = fields.FloatField(label=_('Minutes'))
    frequency = fields.SelectField(label=_('Per'), choices=[('D', 'Day'),
                                                            ('W', 'Week'),
                                                            ('F', 'Fortnight'),
                                                            ('M', 'Month'),
                                                            ('Y', 'Year'),
                                                            ('TOTAL', 'TOTAL')])


class CareTypeForm(BaseForm):
    care_type = fields.SelectField(label=_('Care Type'), choices=CARE_TYPE_CHOICES + [('other', 'other')],
                                   default='other')
    care_type_other = fields.TextField(label=_('Other Care Type'))


class CareSupplierForm(BaseForm):
    supplier = fields.SelectField(label=_('Supplier'))
    care_instances = fields.FieldList(fields.FormField(CareInstanceForm))


class CareTypeWrapperForm(BaseForm):
    care_type = fields.FieldList(fields.FormField(CareTypeForm))
    care_supplier = fields.FieldList(fields.FormField(CareSupplierForm))


class CareForm(BaseForm):
    client_select = ClientChoice(label=_('Client'))
    client = fields.FormField(ClientForm, label=_('Client Details'))
    care = fields.FieldList(fields.FormField(CareTypeWrapperForm))
