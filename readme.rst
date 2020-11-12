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
location of all the buses and streetcars they had in service for a new website
and iOS/Android app. I began collecting this data on February 1, 2019, making
requests to the API every minute (with cron) till October 8th, 2019. Totaling
just under 360,000 responses from the API.

The API returned a JSON response that I appended to a file called ``bus.log``
that eventually grew to 5.2G (608M after being tar-balled) when I stopped polling
the API. This is on the larger end of what I feel comfortable publishing online.
So if you wish for a copy please `send a DM or email me
<https://bryanbrattlof.com/connect/>`__ and I'll gladly send it to you.

Preparing The Data
##################

`prepare-data.py <https://git.bryanbrattlof.com/norta/tree/prepare-data.py>`__:
is a small script to convert the ``bus.log.tar.gz`` file into a CSV file named
``bus.csv`` that can be easily inserted into pandas using something like this:.

.. code-block:: python

   import pandas as pd
   df = pd.read_csv(
       'data/bus.csv',
       dtype={
           'epoch': 'str',
           'vid': 'category',
           'lat': 'float32',
           'lon': 'float32',
           'hdg': 'Int16',
           'des': 'category',
           'dly': 'boolean',
           'pdist': 'float32'
       },
       parse_dates=[
           'epoch'
       ],
    )
    df.set_index('epoch')

Base-map
########

**TODO**

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
