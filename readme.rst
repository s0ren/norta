New Orleans Regional Transit Authority
######################################

Here is the code I used for `the essays I wrote <https://bryanbrattlof.com/
norta/>`__ on `my website <https://bryanbrattlof.com>`__. Each script assumes
you are running at least Python 3.6. All other dependencies are listed in
``requirements.txt`` that can be installed via pip:

.. code-block::

   $ pip install -r requirements.txt

The current versions that work on *my computer*\ :sup:`tm` are:

- matplotlib=3.3.2
- pandas=1.1.3
- pillow=7.0.0
- requests=2.24.0

The Data
########

A few years ago New Orleans, Louisiana published an API with the real time
location of all the buses and streetcars they had in service for a new website
and iOS/Android app. I began collecting this data on February 1, 2019, making
requests to the API every minute (with cron) till October 8th, 2019. Totaling
just under 360,000 responses from the API.

The API returned a JSON response that I appended to a file called ``bus.log``
that eventually grew to 5.2G (608M after being tar-balled) when I stopped polling
the API. This is on the larger end of what I feel comfortable publishing online.
So I've published `the torrent file <https://git.bryanbrattlof.com/norta/plain/
data/bus.log.tar.gz.torrent>`__ you can use to download the data, or if you
need a direct copy please `DM (twitter) or email
<https://bryanbrattlof.com/connect/>`__ me and I'll gladly send you a copy.

prepare-data.py
###############

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

usage
-----

With the ``bus.log.tar.gz`` inside the ``data`` directory, simply run the python
script to generate the ``bus.csv`` file inside the ``data`` directory like so:

.. code-block::

   $ python prepare-data.py

There is no data cleaning involved. This script will only decompress and convert
the log file into a csv file.

basemap.py
##########

`basemap.py <https://git.bryanbrattlof.com/norta/tree/basemap.py>`__: is a simple
module that downloads and combines OpenStreetMap tiles into one large image you
can add to your matplotlib visuals.

dependencies
------------

It assumes you have `requests <https://requests.readthedocs.io/en/master/>`__, and
`pillow <https://python-pillow.org/>`__ libraries installed.

.. code-block::

   $ pip install requests pillow

usage
-----

To use this module, pass the bounding box in GPS coordinates of the area into
the ``top``, ``rgt``, ``bot``, ``lef`` arguments along with the appropriate
``zoom`` level:

.. code-block:: python

   import basemap

   top, bot = df.lat.max(), df.lat.min()
   lef, rgt = df.lon.min(), df.lon.max()

   img = basemap.image(top, rgt, bot, lef, zoom=13)

The module will return a ``Pillow.Image()`` object that you can add to your
matplotlib visuals like this:

.. code-block:: python

   from matplotlib import pyplot as plt
   fig, ax = plt.subplots()
   ax.imshow(img, extent=(lef, rgt, bot, top), aspect= 'equal')
   plt.show()

You can also use ``url`` to specify which tile servers you want to use:

.. code-block:: python

   img = basemap.image(top, rgt, bot, lef, zoom=13,
       url="http://c.tile.stamen.com/toner/{z}/{x}/{y}.png")

Any extra arguments to format the ``url`` argument can be passed along as key word arguments in the ``basemap.image()`` function. For example:

.. code-block:: python

   img = basemap.image(top, rgt, bot, lef, zoom=13, api=API_KEY
       url="http://tileserver.example.com/{api}/{z}/{x}/{y}.png")

add-osm-to-mpl.py
#################

`add-osm-to-mpl.py <https://git.bryanbrattlof.com/norta/tree/add-osm-to-mpl.py>`__:
holds all the example code and code to generate the visuals I used in my `Adding
OpenStreetMaps To MatplotLib <https://bryanbrattlof.com/
adding-openstreetmaps-to-matplotlib/>`__ article.

Contributing
############

Feel free to help in any way you wish. `Buying me Beer
<https://www.buymeacoffee.com/bryanbrattlof>`_, emailing issues, or `patches via
email <https://bryanbrattlof.com/connect/>`_, are all warmly welcomed,
especially beer.

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :alt: License: MIT
