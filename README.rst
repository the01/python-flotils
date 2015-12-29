FLOTILS
#######

Some utility functions and classes I use in many projects.


flotils.logable
===============
Module to ease logging efforts


default_logging_config
----------------------
Dict with my default configuration (includes function logging and,
if installed, colorlog).

Use ``logging.config.dictConfig(default_logging_config)``


Logable
-------
Class to facilitate clean logging with class/function/id information

Inherited classes have a name property consisting of the class name and
optionally an id. They also expose all logging calls of a logger
(``.debug()``, ``.warning()``, ``.exception()``,..)


**Example**

.. code-block:: python

  from flotils.logable import Logable

  class Demo(Loadable):

    def work_on_something(self):
        # do something
        self.debug("working on something")
        self.info("Finished working")

    def work_on_something_else(self):
        self.warning("Something might go wrong")
        self.error("Something went wrong")
        self.warning("Told you!")

  import logging
  logging.basicConfig(level=logging.DEBUG)
  demo1 = Demo()
  demo1.work_on_something()
  logging.debug("Inbetween")
  demo1.work_on_something_else()

*Output*

::

  >> DEBUG:Demo:working on something
     INFO:Demo:Finished working
     DEBUG:root:Inbetween
     WARNING:Demo:Something might go wrong
     ERROR:Demo:Something went wrong
     WARNING:Demo:Told you!


and with an id:

.. code-block:: python

    demo2 = Demo({'id': "demo2"})
    demo2.work_on_something()
    logging.debug("Inbetween")
    demo2.work_on_something_else()

*Output*

::

  >> DEBUG:Demo.demo2:working on something
     INFO:Demo.demo2:Finished working
     DEBUG:root:Inbetween
     WARNING:Demo.demo2:Something might go wrong
     ERROR:Demo.demo2:Something went wrong
     WARNING:Demo.demo2:Told you!

and with id and default_logging_config:

.. code-block:: python

    import logging.config
    from flotils.logable import default_logging_config
    logging.config.dictConfig(default_logging_config)
    logging.getLogger().setLevel(logging.DEBUG)

    demo3 = Demo({'id': "demo3"})
    demo3.work_on_something()
    logging.debug("Inbetween")
    demo3.work_on_something_else()

*Output*

::

  >> 2015-12-27 20:30:48 DEBUG   [Demo.demo2.work_on_something] working on something
     2015-12-27 20:30:48 INFO    [Demo.demo2.work_on_something] Finished working
     2015-12-27 20:30:48 DEBUG   [root] Inbetween
     2015-12-27 20:30:48 WARNING [Demo.demo2.work_on_something_else] Something might go wrong
     2015-12-27 20:30:48 ERROR   [Demo.demo2.work_on_something_else] Something went wrong
     2015-12-27 20:30:48 WARNING [Demo.demo2.work_on_something_else] Told you!


ModuleLogable
-------------
Same as ``Logable``, but used for module level logging

.. code-block:: python

  from flotils.logable import ModuleLogable

  class Logger(ModuleLogable):
      pass

  logger = Logger()
  logger.info("Greetings from module")

*Output*

::

  >> 2015-12-27 20:41:43 INFO    [__main__] Greetings from module

