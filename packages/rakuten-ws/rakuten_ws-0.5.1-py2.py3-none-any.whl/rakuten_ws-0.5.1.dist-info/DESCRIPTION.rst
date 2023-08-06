===============================
Python Rakuten Web Service
===============================



.. image:: https://img.shields.io/pypi/v/rakuten-ws.svg
    :target: https://pypi.python.org/pypi/rakuten-ws

.. image:: https://travis-ci.org/alexandriagroup/rakuten-ws.svg?branch=master
    :target: https://travis-ci.org/alexandriagroup/rakuten-ws
    :alt: CI Status

.. image:: http://codecov.io/github/alexandriagroup/rakuten-ws/coverage.svg?branch=master
    :target: http://codecov.io/github/alexandriagroup/rakuten-ws?branch=master
    :alt: Coverage Status

.. image:: https://readthedocs.org/projects/python-rakuten-web-service/badge/?version=latest
    :target: http://python-rakuten-web-service.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Unofficial Python Client for Rakuten Web Service


* Free software: MIT license
* Documentation: https://rakuten-ws.readthedocs.io.


Supported APIs
--------------

-  `Rakuten Ichiba API`_
-  `Rakuten Ichiba RMS Item API`_
-  `Rakuten Ichiba RMS Product API`_
-  `Rakuten Ichiba RMS Order API`_
-  `Rakuten Ichiba RMS RakutenPayOrder API`_
-  `Rakuten Ichiba RMS Inventory API`_
-  `Rakuten Ichiba RMS Cabinet API`_
-  `Rakuten Ichiba RMS Navigation API`_
-  `Rakuten Ichiba RMS Category API`_
-  `Rakuten Books API`_
-  `Rakuten Travel API`_
-  `Rakuten Auction API`_
-  `Rakuten Kobo API`_
-  `Rakuten GORA API`_
-  `Rakuten Recipe API`_
-  `Rakuten Other APIs`_


.. _Rakuten Ichiba API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=1
.. _Rakuten Ichiba RMS Item API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?contents=/en/common/1-1_service_index/itemapi
.. _Rakuten Ichiba RMS Product API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?contents=/en/common/1-1_service_index/productapi
.. _Rakuten Ichiba RMS Order API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?contents=/en/common/1-1_service_index/orderapi
.. _Rakuten Ichiba RMS RakutenPayOrder API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?contents=/en/common/1-1_service_index/rakutenpayorderapi
.. _Rakuten Ichiba RMS Inventory API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?contents=/en/common/1-1_service_index/inventoryapi
.. _Rakuten Ichiba RMS Cabinet API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?contents=/en/common/1-1_service_index/cabinetapi
.. _Rakuten Ichiba RMS Navigation API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?contents=/en/common/1-1_service_index/navigationapi
.. _Rakuten Ichiba RMS Category API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?contents=/en/common/1-1_service_index/categoryapi
.. _Rakuten Books API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=2
.. _Rakuten Travel API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=4
.. _Rakuten Auction API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=4
.. _Rakuten Kobo API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=7
.. _Rakuten GORA API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=8
.. _Rakuten Recipe API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=6
.. _Rakuten Other APIs: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=9


Installation
------------

Requirements:
  - python >= 2.7
  - python-lxml

You can install, upgrade, uninstall rakuten-ws with these commands::

  $ pip install [--user] rakuten-ws
  $ pip install [--user] --upgrade rakuten-ws
  $ pip uninstall rakuten-ws


Development
-----------

konch_ provides a useful development environment. To execute it, run the command::

   konch


The old solution was to use ptpython_ in interactive mode. To execute it, run the command::

   webservice

.. _konch: https://konch.readthedocs.io/en/latest/
.. _ptpython: https://github.com/prompt-toolkit/ptpython




Python Rakuten Web Service changelog
==================================================

Version 0.5.1
-------------

Release on August 22th 2020

- Fixed the recording of the response by scrubbing more information

Version 0.5.0
-------------

Release on August 22th 2020

- Added the new API RakutenPayOrder

Version 0.4.4
-------------

Release on November 6th 2019

- Fixed the parameters for `RmsService.items.update`
- Updated the API version of some endpoints

Version 0.4.3
-------------

Released on April 19th 2017

- Set `RmsOrderAPI.getOrder.isOrderNumberOnlyFlg` to False by default.

Version 0.4.3.dev0
------------------

**unreleased**

Version 0.4.2
-------------

Released on March 31st 2017

- Fixed `RmsOrderAPI.getOrder` and `RmsOrderAPI.updateOrder`

Version 0.4.1
-------------

Released on March 29th 2017

- Retrieve inventory information about multiple items at once (RmsInventoryAPI)

Version 0.4.0
-------------

Released on March 27th 2017

- Added support for RmsInventoryAPI

Version 0.3.0
-------------

Released on March 21st 2017

- Added support for RMS Category API

Version 0.2.1
-------------

Released on February 28th 2017

- Dropped upload_images function to keep the project as close as possible to Rakuten APIs
- Sorted xml keys recursively

Version 0.2.0
-------------

Released on February 22nd 2017

- Added support for RMS Cabinet API
- Added support for RMS Navigation API
- Added support for Python 3.6

Version 0.1.1
-------------

Released on January 13th 2017

- Included WSDL files in the Pypi package

Version 0.1.0
-------------

Released on January 03rd 2017

- First release on PyPI.


