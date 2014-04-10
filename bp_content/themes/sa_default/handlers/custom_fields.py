from bp_content.themes.sa_default.handlers import models
from bp_includes.external.wtforms.fields.core import Field, SelectField
from bp_includes.external.wtforms.widgets.core import TextInput

__author__ = 'joshainglis'


class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []


class BetterTagListField(TagListField):
    def __init__(self, label='', validators=None, remove_duplicates=True, **kwargs):
        super(BetterTagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def process_formdata(self, valuelist):
        super(BetterTagListField, self).process_formdata(valuelist)
        if self.remove_duplicates:
            self.data = list(self._remove_duplicates(self.data))

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item


class SupplierChoice(SelectField):
    def __init__(self, *args, **kwargs):
        super(SupplierChoice, self).__init__(*args, **kwargs)
        self.choices = [(x.key.id(), x.name) for x in models.Supplier.query().order(models.Supplier.name)]


class ClientChoice(SelectField):
    def __init__(self, *args, **kwargs):
        super(ClientChoice, self).__init__(*args, **kwargs)
        self.choices = [(x.key.id(), "{}, {}".format(x.name_last, x.name_first))
                        for x in models.Client.query().order(models.Client.name_last)]
        self.choices.insert(0, ('new', "New Client"))


class CareSupplierChoice(SelectField):
    def __init__(self, *args, **kwargs):
        super(CareSupplierChoice, self).__init__(*args, **kwargs)
        self.choices = [(x.key.id(), x.name) for x in models.CareSupplier.query().order(models.CareSupplier.name)]
        self.choices.insert(0, ('new', "New Care Supplier"))