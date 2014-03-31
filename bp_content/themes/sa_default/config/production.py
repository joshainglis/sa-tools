import os

config = {

    # This config file will be detected in production environment and values defined here will overwrite those in config.py
    'environment': "production",

    # webapp2 sessions
    'webapp2_extras.sessions': {'secret_key': '-2{ZNAz&Cku/%{Gvx/yaUYl.*-}gol`QIMdr[_`L`[1dFvE+FV9,Juspb:b{zr-f'},

    # webapp2 authentication
    'webapp2_extras.auth': {'user_model': 'bp_includes.models.User',
                            'cookie_name': 'SA-Tool-session'},

    # jinja2 templates
    'webapp2_extras.jinja2': {'template_path': ['bp_admin/templates',
                                                'bp_content/themes/%s/templates' % os.environ['theme']],
                              'environment_args': {'extensions': ['jinja2.ext.i18n']}},

    # application name
    'app_name': "OSI",

    # the default language code for the application.
    # should match whatever language the site uses when i18n is disabled
    'app_lang': 'en_AU',

    # Locale code = <language>_<territory> (ie 'en_US')
    # to pick locale codes see http://cldr.unicode.org/index/cldr-spec/picking-the-right-language-code
    # also see http://www.sil.org/iso639-3/codes.asp
    # Language codes defined under iso 639-1 http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    # Territory codes defined under iso 3166-1 alpha-2 http://en.wikipedia.org/wiki/ISO_3166-1
    # disable i18n if locales array is empty or None
    'locales': ['en_AU', 'es_ES', 'it_IT', 'zh_CN', 'id_ID', 'fr_FR', 'de_DE', 'ru_RU', 'pt_BR', 'cs_CZ',
                'vi_VN', 'nl_NL'],

    # contact page email settings
    'contact_sender': "joshainglis@gmail.com",
    'contact_recipient': "joshainglis@gmail.com",

    # Password AES Encryption Parameters
    # aes_key must be only 16 (*AES-128*), 24 (*AES-192*), or 32 (*AES-256*) bytes (characters) long.

    'aes_key': "YrixyYiz40wVzY0KYQBYoFjuval3it34",
    'salt': "N[?Mc}53C MTYa%M*_v<w#_r<cLr k!>U }>!G5{B#QAA:R w-dg-$ow^vGH|_-?",

    'enable_federated_login': False,

    # Use a complete Google Analytics code, no just the Tracking ID
    'google_analytics_code': "",  # TODO Set This

    # add status codes and templates used to catch and display errors
    # if a status code is not listed here it will use the default app engine
    # stacktrace error page or browser error page
    'error_templates': {
        403: 'errors/default_error.html',
        404: 'errors/default_error.html',
        500: 'errors/default_error.html',
    },

    # fellas' list
    'developers': (
        ('Josha Inglis', 'joshainglis@gmail.com'),
    ),

    # If true, it will write in datastore a log of every email sent
    'log_email': True,

    # If true, it will write in datastore a log of every visit
    'log_visit': True,


    # ----> ADD MORE CONFIGURATION OPTIONS HERE <----

}
