.. _install:

Installation
============

.. _pipinstall:

Installing with pip
-------------------

These instructions cover installation with the ``pip`` package
management tool.  This will install pymodeler and its dependencies into
your python distribution.

Before starting the installation process, you will need to determine
whether you have setuptools and pip installed in your local python
environment.  The following command will install both packages in your
local environment:

.. code-block:: bash

   $ curl https://bootstrap.pypa.io/get-pip.py | python -

Check if pip is correctly installed:

.. code-block:: bash

   $ which pip

Once again, if this isn't the pip in your python environment something went wrong.
Now install pymodeler by running:

.. code-block:: bash

   $ pip install pymodeler

To run the ipython notebook examples you will also need to install
jupyter notebook:
   
.. code-block:: bash

   $ pip install jupyter

.. Running pip and setup.py with the ``user`` flag is recommended if you do not
.. have write access to your python installation (for instance if you are
.. running in a UNIX/Linux environment with a shared python
.. installation).  To install pymodeler into the common package directory
.. of your python installation the ``user`` flag should be ommitted.

Finally, check that pymodeler imports:

.. code-block:: bash

   $ python
   Python 2.7.8 (default, Aug 20 2015, 11:36:15)
   [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.56)] on darwin
   Type "help", "copyright", "credits" or "license" for more information. 
   >>> import pymodeler
   >>> pymodeler.__file__


The instructions describe how to install development versions of
Pymodeler.  Before installing a development version we recommend first
installing a tagged release following the :ref:`pipinstall` 
instructions above.

The development version of Pymodeler can be installed by running ``pip
install`` with the URL of the git repository:

.. code-block:: bash
                
   $ pip install git+https://github.com/kadrlica/pymodeler.git

This will install the most recent commit on the master branch.  Note
that care should be taken when using development versions as
features/APIs under active development may change in subsequent
versions without notice.
   
   
Upgrading
---------

By default installing pymodeler with ``pip`` will get the latest tagged
released available on the `PyPi <https://pypi.python.org/pypi>`_
package respository.  You can check your currently installed version
of pymodeler with ``pip show``:

.. code-block:: bash

   $ pip show pymodeler
   
To upgrade your pymodeler installation to the latest version run the pip
installation command with ``--upgrade --no-deps`` (remember to also
include the ``--user`` option if you're running at SLAC):
   
.. code-block:: bash
   
   $ pip install pymodeler --upgrade --no-deps
   Collecting pymodeler
   Installing collected packages: pymodeler
     Found existing installation: pymodeler 0.1.0
       Uninstalling pymodeler-0.1.0:
         Successfully uninstalled pymodeler-0.1.0
   Successfully installed pymodeler-0.1.1

.. _gitinstall:
   
Developer Installation
----------------------

These instructions describe how to install pymodeler from its git source
code repository using the ``setup.py`` script.  Installing from source
can be useful if you want to make your own modifications to the
pymodeler source code.  Note that non-developers are recommended to
install a tagged release of pymodeler following the :ref:`pipinstall` or
instructions above.

First clone the pymodeler git repository and cd to the root directory of
the repository:

.. code-block:: bash

   $ git clone https://github.com/kadrlica/pymodeler.git
   $ cd pymodeler
   
To install the latest commit in the master branch run ``setup.py
install`` from the root directory:

.. code-block:: bash

   # Install the latest commit
   $ git checkout master
   $ python setup.py install --user 

A useful option if you are doing active code development is to install
your working copy of the package.  This will create an installation in
your python distribution that is linked to the copy of the code in
your local repository.  This allows you to run with any local
modifications without having to reinstall the package each time you
make a change.  To install your working copy of pymodeler run with the
``develop`` argument:

.. code-block:: bash

   # Install a link to your source code installation
   $ python setup.py develop --user 

You can later remove the link to your working copy by running the same
command with the ``--uninstall`` flag:

.. code-block:: bash

   # Install a link to your source code installation
   $ python setup.py develop --user --uninstall
   

Specific release tags can be installed by running ``git checkout``
before running the installation command:
   
.. code-block:: bash
   
   # Checkout a specific release tag
   $ git checkout X.X.X 
   $ python setup.py install --user 

To see the list of available release tags run ``git tag``.
   
Issues
------

If you are running OSX El Capitan or newer you may see errors like the following:

.. code-block:: bash
                
   dyld: Library not loaded

In this case you will need to disable the System Integrity Protections
(SIP).  See `here
<http://www.macworld.com/article/2986118/security/how-to-modify-system-integrity-protection-in-el-capitan.html>`_
for instructions on disabling SIP on your machine.

