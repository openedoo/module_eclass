.. Openedoo eclass module documentation master file, created by
   sphinx-quickstart on Fri May  5 23:41:26 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Openedoo eclass API
==================================================

API Endpoints
-------------

.. http:get::  /eclass/

    Retrieve a list of eclass::

        "[
            {
                \"name\":  \"xyz\",
                \"admin\":  \"\",
                \"university\":  \"uny\",
                \"member\":  \"\",
                \"course\":  \"xyz\",
                \"unique_code\":  \"qweasd\",
                \"privilege\":  \"public\",
                \"id\":  1
            },
            {
                \"name\":  \"xyz\",
                \"admin\":  \"\",
                \"university\":  \"uny\",
                \"member\":  \"\",
                \"course\":  \"xyz\",
                \"unique_code\":  \"qweasd\",
                \"privilege\":  \"public\",
                \"id\":  2
            },
        ]"

.. http:post::  /eclass/

    Add an eclass.

    Accepted Request is `application/json`::

        {
          "name": "yutyutyu",
          "course": "xyz",
          "university": "uny",
          "member": "",
          "admin": "",
          "privilege": "public",
          "unique_code": "qweasd"
        }

    Returns::

        {
          "message": "success"
        }


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
