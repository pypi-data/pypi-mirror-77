Changelog
=========

### 2.0.0 (24/08/2020)

- Django 3 compatibility: replaced calls to django.conf.urls.url with django.urls.path or re_path. 
  PR: https://github.com/ixc/wagtail-instance-selector/pull/9.
- Frontend: fixed a bug where the actions container used for the select button might not exist.
  PR: https://github.com/ixc/wagtail-instance-selector/pull/8
- Frontend: simplified object selection in list items by consolidating on the 
  data-instance-selector-pk attribute.
  PR: https://github.com/ixc/wagtail-instance-selector/pull/8

### 1.2.1 (23/03/2020)

- Django 3 import fix. 
  PR: https://github.com/ixc/wagtail-instance-selector/pull/2.


### 1.1.0 (23/09/2019)

- Added hooks to enable selection on non-standard list views.


### 1.0.1 (06/06/2019)

- PyPI fix.


### 1.0.0 (06/06/2019)

- Initial release.
