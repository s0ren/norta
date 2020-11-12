import datetime
import tarfile
import os.path
import json
import csv


CSV_HEADER = 'epoch vid lon lat hdg des dly pdist'.split()
DATA_FILE = 'data/bus.log.tar.gz'
CSV_FILE = 'data/bus.csv'


# sanity checks
print("Checking Sanity...")

assert os.path.isfile(DATA_FILE) is True,\
    "not found! make sure '{}' exists.".format(DATA_FILE)

assert os.path.isfile(CSV_FILE) is False,\
    "output file '{}' exists! I will not overrite data!".format(CSV_FILE)

assert tarfile.is_tarfile(DATA_FILE) is True,\
    "'{}' may be corrupted! 'tarfile' cannot read it".format(DATA_FILE)

with tarfile.open(DATA_FILE, mode='r|*') as tar:
    assert 'bus.log' in tar.getnames(),\
        "'bus.log' isn't in the archive!"
    tar_member = tar.getmember('bus.log')


# create CSV_FILE and begin writing to it
bus_csv_file = open(CSV_FILE, 'w')
csv = csv.DictWriter(bus_csv_file, fieldnames=CSV_HEADER)
csv.writeheader()


# decompress and convert the DATA_FILE file to CSV format
with tarfile.open(DATA_FILE, mode='r|*') as tar:
    print("Converting '{}' to CSV...".format(DATA_FILE))

    f = tar.extractfile(tar_member)
    for response in f:
        data = json.loads(response)

        epoch = data['epoch']
        for position in data['ResultData']:
            position['epoch'] = epoch
            csv.writerow(position)

bus_csv_file.close()
print("Done!!!")
