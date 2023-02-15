import pandas as pd
import os.path

# DATA_FILE = 'data/bus.csv'
# assert os.path.isfile(DATA_FILE) is True,\
#     "dataset not found! did you run 'prepare-data.py?"

# # load the dataset
# df = pd.read_csv(
#     'data/bus.csv',
#     dtype={
#         'epoch': 'str',
#         'vid': 'category',
#         'lat': 'float32',
#         'lon': 'float32',
#         'hdg': 'Int16',
#         'des': 'category',
#         'dly': 'boolean',
#         'pdist': 'float32'
#     },
#     parse_dates=[
#         'epoch'
#     ],
# )

## FAKE DATA 
import numpy as np
n = 100
#epoch vid lon lat hdg des dly pdist
df = pd.DataFrame(
    {
        'epoch' : np.random.randint(1000, 2000, n),
        'vid': None,
        'lon': np.random.randint(-90225,-90050, n) / 1000,
        'lat': np.random.randint(2988, 3000, n) / 100,
        'hdg' : None,
        'des' : None,
        'dly' : None,
        'pdist': None,
    }
)

df.set_index('epoch')

# clean the data
_len = len(df.index)
df = df[(df['lat'] < 30.386759) & ( df['lat'] > 29.587366) &
        (df['lon'] > -90.874932) & (df['lon'] < -89.513523)]
print("Removed {} Rows".format(_len - len(df.index)))

# narrow down to just route 16
# df = df[(df['des'].str.contains('S. Claiborne Canal St via Poydras St.', na=False))|
#         (df['des'].str.contains('S. Claiborne Poydras St. to S. Carrollton Ave.'))]

#################################
#         Main Visual
#################################
from matplotlib import pyplot as plt
import basemap

avg_lat, avg_lon = df.lat.mean(), df.lon.mean()
std_lat, std_lon = df.lat.std(), df.lon.std()

top = avg_lat + (9 * std_lat)
rgt = avg_lon + (4 * std_lon)
bot = avg_lat - (9 * std_lat)
lef = avg_lon - (4 * std_lon)
z = 10 # 16
img = basemap.image(top, rgt, bot, lef, zoom=z,
    url="http://c.tile.stamen.com/toner/{z}/{x}/{y}.png")

fig, ax = plt.subplots(figsize=(12,8))
ax.scatter(df.lon, df.lat, alpha=0.1, c='red', s=1)
ax.imshow(img, extent=(lef, rgt, bot, top), aspect= 'equal')
plt.savefig(f'visuals/route-{z}-plot.png')

#################################
#     Self-Portrait Visual
#################################
from matplotlib import pyplot as plt

img = plt.imread('visuals/self-portrait.png')
plt.imshow(img)

plt.savefig('visuals/self-portrait-plot.png')

#################################
#      Single Tile Visual
#################################
URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png".format

import math
TILE_SIZE = 256

def point_to_pixels(lon, lat, zoom):
    """convert gps coordinates to web mercator"""
    r = math.pow(2, zoom) * TILE_SIZE
    lat = math.radians(lat)

    x = int((lon + 180.0) / 360.0 * r)
    y = int((1.0 - math.log(
        math.tan(lat) + (1.0 / math.cos(lat))) / math.pi) / 2.0 * r)

    return x, y

zoom = 16
x, y = point_to_pixels(-90.064279, 29.95863, zoom)

x_tile, y_tile = int(x / TILE_SIZE), int(y / TILE_SIZE)

from io import BytesIO
from PIL import Image
import requests

# format the url
url = URL(x=x_tile, y=y_tile, z=zoom)

# make the request
with requests.get(url, headers={"User-Agent":"of_Bryan_Brattlof"}) as resp:
    resp.raise_for_status()
    img = Image.open(BytesIO(resp.content))

# plot the tile
plt.imshow(img)
plt.savefig('visuals/french-quarter-plot.png')

#################################
#      Multi Tile Visual
#################################
top, bot = df.lat.max(), df.lat.min()
lef, rgt = df.lon.min(), df.lon.max()

zoom = 13
x0, y0 = point_to_pixels(lef, top, zoom)
x1, y1 = point_to_pixels(rgt, bot, zoom)

x0_tile, y0_tile = int(x0 / TILE_SIZE), int(y0 / TILE_SIZE)
x1_tile, y1_tile = math.ceil(x1 / TILE_SIZE), math.ceil(y1 / TILE_SIZE)

assert (x1_tile - x0_tile) * (y1_tile - y0_tile) < 50, "That's too many tiles!"

from itertools import product

# full size image we'll add tiles to
img = Image.new('RGB', (
        (x1_tile - x0_tile) * TILE_SIZE,
        (y1_tile - y0_tile) * TILE_SIZE))

# loop through every tile inside our bounded box
for x_tile, y_tile in product(range(x0_tile, x1_tile),
                              range(y0_tile, y1_tile)):

    with requests.get(URL(x=x_tile, y=y_tile, z=zoom), headers={"User-Agent":"of_Bryan_Brattlof"}) as resp:
        resp.raise_for_status()
        tile_img = Image.open(BytesIO(resp.content))

    # add each tile to the full size image
    img.paste(
        im=tile_img,
        box=((x_tile - x0_tile) * TILE_SIZE,\
             (y_tile - y0_tile) * TILE_SIZE))

plt.figure(figsize=(12,8))
plt.imshow(img)
plt.savefig('visuals/the-basemap.png', bbox_inches ="tight")


#################################
#      Crop Lines Visual
#  Don't include this in article
#################################
from PIL import ImageDraw
img2 = img.copy()

# find the mercator coordinates of the top-left corner of all
# the tiles we downloaded from OpenStreetMap
x, y = x0_tile * TILE_SIZE, y0_tile * TILE_SIZE

# draw a red rectangle of the part of the image we want to keep
draw = ImageDraw.Draw(img2)
draw.rectangle(
    (x0 - x,  # left
     y0 - y,  # top
     x1 - x,  # right
     y1 - y), # bottom
    outline=(255, 0, 0),
    width=5)

# draw black rectangles around each individual tile
for x_tile, y_tile in product(range(0, (x1_tile - x0_tile)),
                              range(0, (y1_tile - y0_tile))):

    x, y = x_tile * TILE_SIZE, y_tile * TILE_SIZE
    draw.rectangle(
        (x - 2,  # left
         y - 2,  # top
         (x + TILE_SIZE),  # right
         (y + TILE_SIZE)), # bottom
        outline=(0, 0, 0),
        width=2)

plt.figure(figsize=(12,8))
plt.imshow(img2)
plt.savefig('visuals/basemap-cropping-lines.png', bbox_inches ="tight")

#################################
# Cropping The Multi Tile Visual
#################################
x, y = x0_tile * TILE_SIZE, y0_tile * TILE_SIZE

img = img.crop((
    x0 - x,  # left
    y0 - y,  # top
    x1 - x,  # right
    y1 - y)) # bottom

plt.figure(figsize=(12,8))
plt.imshow(img)
plt.savefig('visuals/basemap-cropped.png', bbox_inches ="tight")

#################################
#       Final Visual
#################################
fig, ax = plt.subplots(figsize=(12,12))

ax.set_ylim(bot, top)
ax.set_xlim(lef, rgt)

ax.scatter(df.lon, df.lat, alpha=0.1, c='red', s=1)
ax.imshow(img, extent=(lef, rgt, bot, top), aspect="equal")

plt.savefig('visuals/final-visual.png')
