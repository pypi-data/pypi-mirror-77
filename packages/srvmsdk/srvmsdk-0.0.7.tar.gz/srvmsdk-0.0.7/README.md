# Test

# install
```
python3 -m pip install --upgrade setuptools wheel
python3 -m pip install twine
```

# setup
```
python3 setup.py sdist bdist_wheel
```

# upload pypi
```
twine upload dist/*
```