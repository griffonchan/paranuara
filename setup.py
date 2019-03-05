import setuptools

setuptools.setup(
    name='paranuara',
    version='1.0.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'json',
        'pytest'
    ]
)
