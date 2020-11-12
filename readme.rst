New Orleans Regional Transit Authority
######################################

Here is the code I used for `the essays I wrote <https://bryanbrattlof.com/
norta/>`__ on `my website <https://bryanbrattlof.com>`__. Each script assumes
you are running at least Python 3.6. All other dependencies are listed in
``requirements.txt`` that can be installed via pip:

.. code-block::

   $ pip install -r requirements.txt

The Data-set
############

A few years ago New Orleans, Louisiana published an API with the real time
location of all the buses and streetcars they had in service in the city for a
new website and iOS/Android app. I began collecting this data on February 1,
2019, making requests to the API every minute (with cron) till October 8th, 2019.
Totaling just under 360,000 responses from the API.

The API returned a JSON response that I appended to a file called ``bus.log``
that eventually grew to 5.2G (608M after being tar-balled) when I stopped polling
the API. This is on the larger end of what I feel comfortable publishing online.
So if you wish for a copy please `send a DM or email me
<https://bryanbrattlof.com/connect/>`__ and I'll gladly give you a copy.

Preparing The Data
##################

**TODO**

Base-map
########

The full write-up is available at
https://bryanbrattlof.com/adding-openstreetmaps-to-matplotlib/

Contributing
############

Feel free to help in any way you wish. `Buying me Beer
<https://www.buymeacoffee.com/bryanbrattlof>`_, emailing issues, or `patches via
email <https://bryanbrattlof.com/connect/>`_, are all warmly welcomed,
especially beer.

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :alt: License: MIT
