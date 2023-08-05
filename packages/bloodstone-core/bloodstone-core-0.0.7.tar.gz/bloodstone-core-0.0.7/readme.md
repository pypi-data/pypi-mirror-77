# upload to pypi

## 项目打包
python setup.py sdist build


## 项目上传 需要账号密码,创建文件：~/.pypirc
python setup.py sdist bdist_egg upload


### 使用twine上传 
twine upload dist/*

## .pypirc格式如下
[distutils]
index-servers=pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = <username>
password = <password>


# Install
pip install bloodstone-core

if package cannot be found under tsinghua source
pip install bloodstone-core -i https://pypi.python.org/simple/


# Use
eg.
from wmpy_util import time_util, img_util

# Use without install
add to python path
export PYTHONPATH=$PYTHONPATH:${A path to wmpy_util}
eg. /Users/workspace/python/python_lib


## IN PYCHARM
open preferences/project structure
then choose add content root
and mark parent directory of wmpy_util as SOURCE ROOT