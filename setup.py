from setuptools import setup, find_packages

setup(
    name='graph_curation',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask_RESTful==0.3.6',
        'Flask==0.12.2',
        'protobuf==3.5.2.post1',
        'pyArango==1.3.1',
        'Flask-JWT-Extended==3.3.4',
        'PyJWT==1.5.3',
        'Flask-Cors==3.0.6'
    ],
)
