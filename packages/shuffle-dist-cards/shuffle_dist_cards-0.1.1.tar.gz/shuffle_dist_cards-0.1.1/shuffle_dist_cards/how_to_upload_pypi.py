#cd proj_dir
#python setup.py sdist
#pip install twine

# commands to upload to the pypi test repository
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# pip install --index-url https://test.pypi.org/simple/ distributions

# command to upload to the pypi repository
# twine upload dist/*
# pip install distributions
