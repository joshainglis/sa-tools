"""
Using redirect route instead of simple routes since it supports strict_slash
Simple route: http://webapp-improved.appspot.com/guide/routing.html#simple-routes
RedirectRoute: http://webapp-improved.appspot.com/api/webapp2_extras/routes.html#webapp2_extras.routes.RedirectRoute
"""
from webapp2_extras.routes import RedirectRoute
from bp_content.themes.sa_default.handlers import handlers

secure_scheme = 'https'

# Here go your routes, you can overwrite boilerplate routes (bp_includes/routes)

_routes = [
    RedirectRoute('/secure/', handlers.SecureRequestHandler, name='secure', strict_slash=True),
    RedirectRoute('/settings/delete_account', handlers.DeleteAccountHandler, name='delete-account', strict_slash=True),
    RedirectRoute('/contact/', handlers.ContactHandler, name='contact', strict_slash=True),
    RedirectRoute('/add_supplier/', handlers.AddSupplierHandler, name='add-supplier', strict_slash=True),
    RedirectRoute('/add_aid/', handlers.AddAidHandler, name='add-aid', strict_slash=True),
    RedirectRoute('/add_care/', handlers.EnterCare, name='add-care', strict_slash=True),
    RedirectRoute('/view_aids/', handlers.ViewAids, name='view-aids', strict_slash=True),
    RedirectRoute('/view_suppliers/', handlers.ViewSuppliers, name='view-suppliers', strict_slash=True),
    RedirectRoute('/get_full_product_info/', handlers.AjaxGetFullProductHandler, name='ajax-aids', strict_slash=True),
    RedirectRoute('/get_all_product_info/', handlers.AjaxGetAllProductsHandler, name='ajax-all-aids', strict_slash=True),
    RedirectRoute('/get_client_info/', handlers.AjaxGetClientHandler, name='ajax-client', strict_slash=True),
    RedirectRoute('/get_care_supplier_info/', handlers.AjaxGetCareSupplierHandler, name='ajax-care-supplier', strict_slash=True),
    RedirectRoute('/upload_csv/', handlers.UploadCSV, name='upload-csv', strict_slash=True),
    RedirectRoute('/upload_image/', handlers.UploadImageHandler, name='upload-image', strict_slash=True),
]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)
