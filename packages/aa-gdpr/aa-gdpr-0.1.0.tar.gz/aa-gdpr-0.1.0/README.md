# AA-GDPR

A Collection of resources to help Alliance Auth installs meet GDPR legislation.

This Repository cannot guarantee your Legal requirements but aims to reduce the technical burden.

## Current Features
 Local Staticfile delivery of resources to avoid using CDNs
* Javascript
* Less 3.12.2
* Moment.js v2.27 https://github.com/moment/moment
* jQuery 3.5.1 & 2.2.4 https://github.com/jquery/jquery
* jQuery-DateTimePicker v2.5.20 https://github.com/xdan/datetimepicker
* Twitter-Bootstrap v3.4.1 https://github.com/twbs/bootstrap
* X-editable 1.5.1
* Less 2.7.3 & 3.12.2
* Datatables 1.10.21
* Clipboard.js 2.0.6
* Fonts
* FontAwesome v5.14 https://github.com/FortAwesome/Font-Awesome
* OFL Lato
* CSS
* Datatables
* FontAwesome
* jQuery-DateTimePicker
* x-editable

Planned Features:
User Data Views
Right to be Forgotten Requests

## Installation
 1. Install the Repo `pip install git+https://gitlab.com/soratidus999/aa-gdpr.git`
 2. Add `INSTALLED_APPS.insert(0, 'aagdpr')` right before your `INSTALLED_APPS` list in your projects `local.py`
 3. Run migrations (There should be none yet)
 4. Gather your staticfiles `python manage.py collectstatic`
 3. Configure your settings as below

# Settings

AVOID_CDN - Will Attempt to load CSS JS and Fonts from staticfiles whenever possible avoiding CDNs. Default False.