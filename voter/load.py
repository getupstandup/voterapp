import os
import csv
import requests

from django.contrib.gis.utils import LayerMapping
from .models import *


# Auto-generated `LayerMapping` dictionary for tl_2017_us_cd115 model
district_mapping = {
    'statefp': 'STATEFP',
    'districtid': 'CD115FP',
    'boundary': 'MULTIPOLYGON',
}

cd115_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'tl_2017_us_cd115.shp')
)

def load_districts(verbose=True):
    lm = LayerMapping(District, cd115_shp, district_mapping,
        transform=False, encoding='iso-8859-1',
    )

    lm.save(strict=True, verbose=verbose)

def load_representatives():
    url = 'http://clerk.house.gov/member_info/text-labels-115.txt'
    info = requests.get(url).text

    for ii in info.split('\n')[1:]:
        row = ii.split('\t')
        if len(row) < 12:
            continue
            
        defaults = {
            'prefix': row[0],
            'first_name': row[1],
            'middle_name': row[2],
            'last_name': row[3],
            'suffix': row[4],
            'address': row[5],
            'city': row[6],
            'state': row[7],
            'zip_4': row[8],
            'bioguideid': row[10],
            'party': row[11]            
        }

        Representative.objects.update_or_create(st_dis_115=row[9], defaults=defaults)
