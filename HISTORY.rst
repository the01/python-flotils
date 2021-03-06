.. :changelog:

History
=======

0.5.3 (2019-08-03)
--------------------

* Update supported versions


0.5.2 (2019-04-15)
--------------------

* pyyaml FullLoader
* load/save bug fixes


0.5.1 (2019-04-14)
--------------------

* Fix json loading bug
* Make json time loading more permissable


0.5.0 (2019-03-26)
--------------------

* Fix typos
* Flake8 not version bound
* Update pyyaml
* Remove deprecated code
* Fix open() calls (use io.open(), no byte open, utf8 encoding)
* StartStopable.is_running
* DateTimeEn/Decode free of time zone (always utc)
* Drop "python-dateutil" dependency
* Basic loadable test file


0.4.2 (2018-01-27)
--------------------

* missing merge


0.4.1 (2018-01-27)
--------------------

* small __init__ changes


0.4.0 (2018-01-27)
--------------------

* add convenience module (PrintableBase, FromToDictBase)
* add save_file/load_file to Loadable
* remove deprecated logException, warn from Logable
* __future__ imports in runable


0.3.5a0 (2017-03-06)
--------------------

* Deprecated camel-case methods in loadable, new save/load methods


0.3.4a0 (2017-03-06)
--------------------

* Add yaml loading/saving code


0.3.3a0 (2017-03-06)
--------------------

* Add get_logger function


0.3.2b0 (2016-11-25)
--------------------

* Fix relative import in loadable


0.3.2a0 (2016-08-14)
--------------------

* Add datetime.timedelta to JSONEncoder/Decoder


0.3.1a0 (2016-03-31)
--------------------

* Catch interrupt in Stopable.stop() when sleeping


0.3.0a0 (2016-03-08)
--------------------

* Move webscraper to own package


0.2.14b0 (2016-03-02)
---------------------

* Fix missing calls to parent init method


0.2.13a0 (2016-01-28)
---------------------

* Runable (Startable, Stopable, StartStopable, SignalStopWrapper)


0.2.12a0 (2016-01-07)
---------------------

* WebScraper


0.2.11a0 (2015-12-31)
---------------------

* Loadable
* Changed documentation


0.2.10a0 (2015-12-27)
---------------------

* First release on PyPI.
* Logable
