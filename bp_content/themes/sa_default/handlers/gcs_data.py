__author__ = 'joshainglis'

from google.appengine.ext import blobstore
from google.appengine.api import app_identity, images
import bp_content.themes.sa_default.external.cloudstorage as gcs
from bp_content.themes.sa_default.handlers.models import ImageModel as Dynamics
import os
import mimetypes
# bonus, zip Dynamics entities and binary GCS blobs
import zipfile
import logging


default_bucket = app_identity.get_default_gcs_bucket_name()
gae_development = os.environ['SERVER_SOFTWARE'].startswith('Development')


def gcs_serving_url(dyn):
    """ serving url for google cloud storage dyn entity """

    gcs_file_name = '/%s/%s' % (default_bucket, dyn.filename)

    if dyn.extension in ['png', 'jpg', 'gif', 'jpeg']:
        dyn.serving_url = images.get_serving_url(
            blobstore.create_gs_key('/gs' + gcs_file_name), secure_url=True)
    elif gae_development:
        # this SDK feature has not been documented yet !!!
        dyn.serving_url = 'http://localhost:8080/_ah/gcs' + gcs_file_name
    else:
        dyn.serving_url = 'https://storage.googleapis.com' + gcs_file_name

    return dyn.serving_url


def gcs_read_blob(dyn):
    """ read binary blob from google cloud storage """

    gcs_file_name = '/%s/%s' % (default_bucket, dyn.filename)
    try:
        with gcs.open(gcs_file_name) as f:
            return f.read()
    except gcs.NotFoundError, e:
        logging.warning('GCS file %s NOT FOUND : %s' % (gcs_file_name, e))
        return None


def gcs_write_blob(dyn, blob):
    """ update google cloud storage dyn entity """

    gcs_file_name = '/%s/%s' % (default_bucket, dyn.filename)

    content_type = mimetypes.guess_type(dyn.filename)[0]
    if dyn.extension in ['js', 'css']:
        content_type += b'; charset=utf-8'

    with gcs.open(gcs_file_name, 'w', content_type=content_type,
                  options={b'x-goog-acl': b'private'}) as f:

        # f.write(images.resize(blob, width=100, height=100))

        try:
            f.write(images.resize(blob, width=100, height=100))
        except:
            f.write(blob)
    return gcs_file_name


def gcs_content_type(dyn):
    gcs_file_name = '/%s/%s' % (default_bucket, dyn.filename)

    return gcs.stat(gcs_file_name).content_type


def gcs_zip_dynamics():
    """ bonus: save Dynamics and GCS blobs in a zip archive """

    gcs_file_name = '/%s/dynamics.zip' % default_bucket

    with gcs.open(gcs_file_name, 'w', content_type=b'multipart/x-zip') as f:

        with zipfile.ZipFile(f, 'w') as z:

            for each in Dynamics.query():
                member_dir = each.filename.replace('.', '_').encode('utf-8')
                z.writestr(b'%s/safe_key.txt' % member_dir, each.key.urlsafe().encode('utf-8'))
                z.writestr(b'%s/serving_url.txt' % member_dir, each.serving_url.encode('utf-8'))

                # if we have a GCS blob for this entity, save it in this member
                blob = gcs_read_blob(each)
                if blob:
                    z.writestr(b'%s/%s' % (member_dir, each.filename), blob)
                    z.writestr(b'%s/content_type.txt' % member_dir, gcs_content_type(each))


# # example create a serving url
# entity = Dynamics(id='test.pdf', filename='test.pdf')
# gcs_serving_url(entity)
# entity.put()
