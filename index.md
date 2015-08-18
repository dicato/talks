=============================
Boston Python: Twisted Primer
=============================

August 27, 2015

Patrick Cloke <patrick@cloke.us>
Stephen DiCato


About
=====

Patrick Cloke

`@clokep <https://twitter.com/cloke>`_

http://patrick.cloke.us/

Stephen DiCato

What we want them to learn
==============

* Core concepts of Twisted:
    * Event loop / reactor
    * Deferred
    * Evented programming / async programming
    * Protocol factory, protocol? WTF?
    * When to attempt async. programming? (I/O vs. CPU vs. ...?)

* Simplify examples down from huge 10-part things down to '60 seconds' (small & consumable)


.. rst-class:: build

* Twisted Overview
* Twisted Example
* Deferreds
* Trial / Testing


Twisted
=======

.. rst-class:: build

    What is Twisted?
        An *asynchronous*, *evented* networking framework for Python
    Why use Twisted?
        * Don't worry about low-level networking
        * Easily handle many connections without blocking
        * Built in parsing of many network protocols.
    When shouldn't I use Twisted?
        Twisted will not help you with CPU-bound tasks, e.g. long blocking tasks.

        Twisted is probably not the easiest library if you just want to make an HTTP
        request. (I'd suggest using `requests <http://python-requests.org/>`_.)

    More information at https://twistedmatrix.com/

    To just install it: ``pip install twisted``

.. note::
    Asynchronous: non-blocking against I/O bound tasks (e.g. reading/writing to
    a socket). [#]_

    Evented: user code is notified by the event loop when something it cares
    about happens (e.g. new data is available on a socket). Freqeuntly layered
    in Twisted: e.g. new data to new line to new HTTP request.


Twisted Concepts
================

* Protocols & Factories
* ``twistd``
* Deferreds
* Reactor


Deferreds
=========

* A
* Bulleted
* List


Reactors
========


Trial: Testing Twisted
======================

Stuff


Citations
=========

.. [#] Jean-Paul Calderone, http://stackoverflow.com/a/6118510/1070085
