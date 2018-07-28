import zipfile
import urllib.request
from os import path

dir_path = path.dirname(path.dirname(path.abspath(__file__)))

url = 'https://www2.census.gov/geo/tiger/TIGER2017/CD/tl_2017_us_cd115.zip'
filename = dir_path + '/districts/data/tl_2017_us_cd115.zip'
# print( filename, '@@@@@@@@')
urllib.request.urlretrieve(url, filename)

zip_ref = zipfile.ZipFile(filename, 'r')
zip_ref.extractall(dir_path+'/districts/data')
zip_ref.close()
