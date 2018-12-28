from setuptools import setup
setup(
  name = 'pyeverlights',
  packages = ['pyeverlights'],
  version = '0.1.0',
  description = 'A library for controlling an EverLights lighting system.',
  author = 'Jon Caruana',
  author_email = 'jon@joncaruana.com',
  url = 'https://github.com/joncar/pyeverlights',
  download_url = 'https://github.com/joncar/pyeverlights/tarball/0.1.0',
  keywords = ['everlights'],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
  ],
  license = 'MIT',
  install_requires = ['aiohttp']
  )
