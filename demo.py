#!/bin/env python
# coding=utf-8

"""
Demo script. Run:

python.exe demo.py
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

logging.basicConfig(level=logging.DEBUG)

from django.conf import settings
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.utils.timezone import now as tznow
from django.shortcuts import render
from django.views import View
from django.conf.urls.static import static

basename = os.path.splitext(os.path.basename(__file__))[0]


def rel(*path):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), *path)
    ).replace('\\', '/')


if not settings.configured:
    settings.configure(
        DEBUG=os.environ.get('DEBUG', True),
        TIMEZONE='UTC',
        INSTALLED_APPS=['easy_pdf'],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [rel('tests', 'templates')],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                    ],
                },
            },
        ],
        STATIC_ROOT=os.path.abspath(rel('tests', 'static')),
        STATIC_URL='/static/',
        STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'djangobower.finders.BowerFinder',
        #'django.contrib.staticfiles.storage.StaticFilesStorage',
        ),
	STATICFILES_DIRS = os.path.abspath(rel('tests', 'static')),
        ROOT_URLCONF=basename,
        WSGI_APPLICATION='{}.application'.format(basename),
        ALLOWED_HOSTS=[
            '0.0.0.0',
            'localhost',
            'easy-pdf.herokuapp.com'
        ]
    )


from easy_pdf.views import PDFTemplateView


class DemoPDFView(PDFTemplateView):
    template_name = 'hello.html'

    def get_context_data(self, **kwargs):
        return super(DemoPDFView, self).get_context_data(
            pagesize='A4',
            title='Hi there!',
            today=tznow(),
            **kwargs
        )

class HtmlPDFView(View):
    def get(self,request):
        return render(request,'hello.html')


urlpatterns = [
    url(r'^$', DemoPDFView.as_view()),
    url(r'html/$', HtmlPDFView.as_view())
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import call_command

    call_command('runserver', '0.0.0.0:8000')
