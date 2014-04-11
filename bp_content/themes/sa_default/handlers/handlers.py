# -*- coding: utf-8 -*-

"""
    A real simple app for using webapp2 with auth and session.

    It just covers the basics. Creating a user, login, logout
    and a decorator for protecting certain handlers.

    Routes are setup in routes.py and added in main.py
"""
# standard library imports
import logging
# related third party imports
from google.appengine.ext.ndb.key import Key
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from webapp2_extras import json
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from webapp2_extras.i18n import gettext as _
from bp_content.themes.sa_default.handlers import models
from bp_content.themes.sa_default.handlers.models import Supplier, Aid
from bp_includes.external import httpagentparser
# local application/library specific imports
import bp_includes.lib.i18n as i18n
from bp_includes.lib.basehandler import BaseHandler
from bp_includes.lib.decorators import user_required
from bp_includes.lib import captcha, utils
import bp_includes.models as models_boilerplate
import bp_content.themes.sa_default.handlers.forms as forms


class ContactHandler(BaseHandler):
    """
    Handler for Contact Form
    """

    def get(self):
        """ Returns a simple HTML for contact form """

        if self.user:
            user_info = self.user_model.get_by_id(long(self.user_id))
            if user_info.name or user_info.last_name:
                self.form.name.data = user_info.name + " " + user_info.last_name
            if user_info.email:
                self.form.email.data = user_info.email
        params = {
            "exception": self.request.get('exception')
        }

        return self.render_template('contact.html', **params)

    def post(self):
        """ validate contact form """

        if not self.form.validate():
            return self.get()
        remote_ip = self.request.remote_addr
        city = i18n.get_city_code(self.request)
        region = i18n.get_region_code(self.request)
        country = i18n.get_country_code(self.request)
        coordinates = i18n.get_city_lat_long(self.request)
        user_agent = self.request.user_agent
        exception = self.request.POST.get('exception')
        name = self.form.name.data.strip()
        email = self.form.email.data.lower()
        message = self.form.message.data.strip()
        template_val = {}

        try:
            # parsing user_agent and getting which os key to use
            # windows uses 'os' while other os use 'flavor'
            ua = httpagentparser.detect(user_agent)
            _os = ('flavor' in ua) and 'flavor' or 'os'

            operating_system = str(ua[_os]['name']) if "name" in ua[_os] else "-"
            if 'version' in ua[_os]:
                operating_system += ' ' + str(ua[_os]['version'])
            if 'dist' in ua:
                operating_system += ' ' + str(ua['dist'])

            browser = str(ua['browser']['name']) if 'browser' in ua else "-"
            browser_version = str(ua['browser']['version']) if 'browser' in ua else "-"

            template_val = {
                "name": name,
                "email": email,
                "ip": remote_ip,
                "city": city,
                "region": region,
                "country": country,
                "coordinates": coordinates,

                "browser": browser,
                "browser_version": browser_version,
                "operating_system": operating_system,
                "message": message
            }
        except Exception as e:
            logging.error("error getting user agent info: %s" % e)

        try:
            subject = _("Contact") + " " + self.app.config.get('app_name')
            # exceptions for error pages that redirect to contact
            if exception != "":
                subject = "{} (Exception error: {})".format(subject, exception)

            body_path = "emails/contact.txt"
            body = self.jinja2.render_template(body_path, **template_val)

            email_url = self.uri_for('taskqueue-send-email')
            taskqueue.add(url=email_url, params={
                'to': self.app.config.get('contact_recipient'),
                'subject': subject,
                'body': body,
                'sender': self.app.config.get('contact_sender'),
            })

            message = _('Your message was sent successfully.')
            self.add_message(message, 'success')
            return self.redirect_to('contact')

        except (AttributeError, KeyError), e:
            logging.error('Error sending contact form: %s' % e)
            message = _('Error sending the message. Please try again later.')
            self.add_message(message, 'error')
            return self.redirect_to('contact')

    @webapp2.cached_property
    def form(self):
        return forms.ContactForm(self)


class SecureRequestHandler(BaseHandler):
    """
    Only accessible to users that are logged in
    """

    @user_required
    def get(self, **kwargs):
        user_session = self.user
        user_session_object = self.auth.store.get_session(self.request)

        user_info = self.user_model.get_by_id(long(self.user_id))
        user_info_object = self.auth.store.user_model.get_by_auth_token(
            user_session['user_id'], user_session['token'])

        try:
            params = {
                "user_session": user_session,
                "user_session_object": user_session_object,
                "user_info": user_info,
                "user_info_object": user_info_object,
                "userinfo_logout-url": self.auth_config['logout_url'],
            }
            return self.render_template('secure_zone.html', **params)
        except (AttributeError, KeyError), e:
            return "Secure zone error:" + " %s." % e


class DeleteAccountHandler(BaseHandler):
    @user_required
    def get(self, **kwargs):
        chtml = captcha.displayhtml(
            public_key=self.app.config.get('captcha_public_key'),
            use_ssl=(self.request.scheme == 'https'),
            error=None)
        if self.app.config.get('captcha_public_key') == "PUT_YOUR_RECAPCHA_PUBLIC_KEY_HERE" or \
                        self.app.config.get('captcha_private_key') == "PUT_YOUR_RECAPCHA_PUBLIC_KEY_HERE":
            chtml = '<div class="alert alert-error"><strong>Error</strong>: You have to ' \
                    '<a href="http://www.google.com/recaptcha/whyrecaptcha" target="_blank">sign up ' \
                    'for API keys</a> in order to use reCAPTCHA.</div>' \
                    '<input type="hidden" name="recaptcha_challenge_field" value="manual_challenge" />' \
                    '<input type="hidden" name="recaptcha_response_field" value="manual_challenge" />'
        params = {
            'captchahtml': chtml,
        }
        return self.render_template('delete_account.html', **params)

    def post(self, **kwargs):
        challenge = self.request.POST.get('recaptcha_challenge_field')
        response = self.request.POST.get('recaptcha_response_field')
        remote_ip = self.request.remote_addr

        cResponse = captcha.submit(
            challenge,
            response,
            self.app.config.get('captcha_private_key'),
            remote_ip)

        if cResponse.is_valid:
            # captcha was valid... carry on..nothing to see here
            pass
        else:
            _message = _('Wrong image verification code. Please try again.')
            self.add_message(_message, 'error')
            return self.redirect_to('delete-account')

        if not self.form.validate() and False:
            return self.get()
        password = self.form.password.data.strip()

        try:

            user_info = self.user_model.get_by_id(long(self.user_id))
            auth_id = "own:%s" % user_info.username
            password = utils.hashing(password, self.app.config.get('salt'))

            try:
                # authenticate user by its password
                user = self.user_model.get_by_auth_password(auth_id, password)
                if user:
                    # Delete Social Login
                    for social in models_boilerplate.SocialUser.get_by_user(user_info.key):
                        social.key.delete()

                    user_info.key.delete()

                    ndb.Key("Unique", "User.username:%s" % user.username).delete_async()
                    ndb.Key("Unique", "User.auth_id:own:%s" % user.username).delete_async()
                    ndb.Key("Unique", "User.email:%s" % user.email).delete_async()

                    #TODO: Delete UserToken objects

                    self.auth.unset_session()

                    # display successful message
                    msg = _("The account has been successfully deleted.")
                    self.add_message(msg, 'success')
                    return self.redirect_to('home')


            except (InvalidAuthIdError, InvalidPasswordError), e:
                # Returns error message to self.response.write in
                # the BaseHandler.dispatcher
                message = _("Incorrect password! Please enter your current password to change your account settings.")
                self.add_message(message, 'error')
            return self.redirect_to('delete-account')

        except (AttributeError, TypeError), e:
            login_error_message = _('Your session has expired.')
            self.add_message(login_error_message, 'error')
            self.redirect_to('login')

    @webapp2.cached_property
    def form(self):
        return forms.DeleteAccountForm(self)


class AddSupplierHandler(BaseHandler):
    def get(self, clear=True):
        if clear:
            self.form.supplier_name.data = ''
            self.form.email.data = ''
            self.form.phone.data = ''
            self.form.website.data = ''
            self.form.notes.data = ''

        return self.render_template('add_supplier.html')

    def post(self):
        """ validate contact form """

        if not self.form.validate():
            return self.get(clear=False)
        name = self.form.supplier_name.data.strip()
        email = self.form.email.data.lower()
        phone = self.form.phone.data.strip()
        website = self.form.website.data.strip().lower()
        notes = self.form.notes.data.strip()

        new_supplier = Supplier(name=name,
                                email=email,
                                phone=phone,
                                website=website,
                                notes=notes)

        new_supplier_key = new_supplier.put()

        return self.get()


    @webapp2.cached_property
    def form(self):
        return forms.SupplierForm(self)


class AddAidHandler(BaseHandler):
    def get(self, clear=True):
        if clear:
            self.form.name.data = ''
            self.form.cost.data = ''
            self.form.maintenance.data = ''
            self.form.replacement.data = ''
            self.form.installation.data = ''
            self.form.postage.data = ''
            self.form.supplier.data = ''
            self.form.tags.data = ''
            self.form.notes.data = ''
        edit_id = self.request.get('aid_id')
        if edit_id:
            aid = ndb.Key(urlsafe=edit_id).get()
            self.form.name.data = aid.name
            self.form.cost.data = aid.cost
            self.form.maintenance.data = aid.maintenance
            self.form.replacement.data = aid.replacement
            self.form.installation.data = aid.installation
            self.form.postage.data = aid.postage
            self.form.supplier.data = aid.supplier.get().name
            self.form.tags.data = aid.tags
            self.form.notes.data = aid.notes
        return self.render_template('add_aid.html')

    def post(self):
        """ validate contact form """

        if not self.form.validate():
            return self.get(clear=False)
        name = self.form.name.data.strip()
        cost = self.form.cost.data
        maintenance = self.form.maintenance.data
        replacement = self.form.replacement.data
        installation = self.form.installation.data
        postage = self.form.postage.data
        supplier = self.form.supplier.data
        tags = self.form.tags.data
        notes = self.form.notes.data.strip()

        edit_id = self.request.get('aid_id')
        logging.info(edit_id)
        if edit_id:
            new_aid = ndb.Key(urlsafe=edit_id).get()
            logging.info(new_aid)
        else:
            new_aid = Aid()
        new_aid.name = name
        new_aid.cost = cost
        new_aid.maintenance = maintenance
        new_aid.replacement = replacement
        new_aid.installation = installation
        new_aid.postage = postage
        new_aid.supplier = Key("Supplier", supplier)
        new_aid.tags = tags
        new_aid.notes = notes

        new_aid_key = new_aid.put()

        return self.get()

    @webapp2.cached_property
    def form(self):
        return forms.AidForm(self)


class ViewSuppliers(BaseHandler):
    def get(self):
        data = Supplier.query().order(Supplier.name)
        return self.render_template('view_suppliers.html', table_data=data)


class ViewAids(BaseHandler):
    show_fields = ['name']

    def get(self):
        data = Aid.query().order(Aid.name)
        return self.render_template('view_aids.html', table_data=data)


class AjaxGetFullProductHandler(webapp2.RequestHandler):
    def post(self):
        record_id = json.decode(self.request.body).get('record_id')
        record = Aid.get_by_id(int(record_id))
        try:
            record_dict = dict(
                name=record.name,
                cost=record.cost,
                supplier=record.supplier.get().name,
                maintenance=record.maintenance,
                replacement=record.replacement,
                error=False,
            )
        except AttributeError:
            record_dict = {'error': True}
        record_dict['id'] = record_id
        res = json.encode(record_dict)
        self.response.out.write(res)


class AjaxGetClientHandler(webapp2.RequestHandler):
    def post(self):
        record_id = json.decode(self.request.body).get('record_id')
        record = models.Client.get_by_id(int(record_id))
        try:
            record_dict = dict(
                name_first=record.name_first,
                name_last=record.name_last,
                dob=record.dob.strftime("%Y-%m-%d"),
                sex=record.sex,
                contact=record.contact,
                unit=record.address.unit,
                address1=record.address.address1,
                address2=record.address.address2,
                suburb=record.address.suburb,
                state=record.address.state,
                error=False,
            )
        except AttributeError:
            record_dict = {'error': True}
        record_dict['id'] = record_id
        res = json.encode(record_dict)
        self.response.out.write(res)


class AjaxGetCareSupplierHandler(webapp2.RequestHandler):
    def post(self):
        record_id = json.decode(self.request.body).get('record_id')
        record = models.CareSupplier.get_by_id(int(record_id))
        try:
            record_dict = dict(
                supplier_name=record.name,
                email=record.email,
                website=record.website,
                phone=record.phone,
                notes=record.notes,
                price_models=[(x.id(), x.get.name()) for x in record.price_models],
                error=False,
            )
        except AttributeError:
            record_dict = {'error': True}
        record_dict['id'] = record_id
        res = json.encode(record_dict)
        self.response.out.write(res)


class EnterCare(BaseHandler):
    @webapp2.cached_property
    def form(self):
        return forms.CareForm(self)

    def get(self):
        return self.render_template('add_care.html')

    @staticmethod
    def _handle_client(client_data, customer_choice):
        if customer_choice != 'new':
            client = models.Client.get_by_id(int(customer_choice))
            altered = not all([
                client.name_first == client_data["name_first"],
                client.name_last == client_data["name_last"],
                client.dob == client_data["dob"],
                client.sex == client_data["sex"],
                client.address == client_data["address"],
                client.contact == client_data["contact"]
            ])
        else:
            client = models.Client()
            altered = True
        if altered:
            client.name_first = client_data['name_first']
            client.name_last = client_data["name_last"]
            client.dob = client_data["dob"]
            client.sex = client_data["sex"]
            address = client_data["address"]
            client.address = models.Address(
                unit=address['unit'],
                address1=address['address1'],
                address2=address['address2'],
                suburb=address['suburb'],
                state=address['state']
            )
            client.contact = client_data["contact"]
            client_key = client.put()
        else:
            client_key = client.key
        return client_key

    @staticmethod
    def _handle_care_supplier(supplier_data, supplier_choice):
        if supplier_choice != 'new':
            supplier = models.CareSupplier.get_by_id(int(supplier_choice))
            supplier = models.CareSupplier
            altered = not all([
                supplier.name == supplier_data["supplier_name"],
                supplier.email == supplier_data["email"],
                supplier.phone == supplier_data["phone"],
                supplier.website == supplier_data["website"],
                supplier.notes == supplier_data["notes"],
            ])
        else:
            supplier = models.Client()
            altered = True
        if altered:
            supplier.name = supplier_data["supplier_name"]
            supplier.email = supplier_data["email"]
            supplier.phone = supplier_data["phone"]
            supplier.website = supplier_data["website"]
            supplier.notes = supplier_data["notes"]
            supplier_key = supplier.put()
        else:
            supplier_key = supplier.key
        return supplier_key

    def post(self):
        # if not self.form.validate():
        #     logging.warning('Did not validate, %s', self.form.errors)
        #     return self.get()
        client_key = self._handle_client(client_data=self.form.client.data,
                                         customer_choice=self.form.client_select.data)



        # care_data = self.form.care.data
        # for care_type_wrapper in care_data:
        #     care_types = [x.care_type.data if x.care_type.data is not 'other' else x.care_type_other.data for x in
        #                   care_type_wrapper.care_type.data]
        #     care_suppliers = care_type_wrapper.care_supplier.data
        #     for care_supplier in care_suppliers:
        #         supplier = care_supplier.supplier.data
        #         care_instances = care_supplier.care_instances.data
        #         for care_instance in care_instances:
        #             date_start = care_instance.date_start.data
        #             date_end = care_instance.date_end.data
        #             hours = care_instance.hours.data
        #             minutes = care_instance.minutes.data
        #             frequency = care_instance.frequency.data

        return self.render_template('add_care.html')
