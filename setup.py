from setuptools import setup

setup(
    name='spacepixinvaders',
    version='0.0.1',
    packages=['spacepixinvaders', 'images', 'sounds', 'fonts'],
    install_requires=[
        'pygame',
        'SQLAlchemy',
        'keyboard',
    ],
    setup_requires=[
        'pytest_runner'
    ],
    zip_safe=False,
)