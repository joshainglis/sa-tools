from wtforms import validators, ValidationError

__author__ = 'joshainglis'


class AnyOfList(validators.AnyOf):
    def __call__(self, form, field):
        tags = field.data
        for tag in tags:
            if tag.upper().strip() not in self.values:
                message = self.message
                if message is None:
                    message = field.gettext('Invalid value, must be one of: %(values)s.')

                raise ValidationError(message % dict(values=self.values_formatter(self.values)))
