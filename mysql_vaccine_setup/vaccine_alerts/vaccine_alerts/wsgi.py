"""
WSGI config for vaccine_alerts project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import vaccine_alerts
import threading
from django.core.wsgi import get_wsgi_application
import alerts
from alerts import models
import urllib.request
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
from datetime import date
import time


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccine_alerts.settings')

application = get_wsgi_application()
