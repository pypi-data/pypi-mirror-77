from setuptools import setup

def readme():
  with open('README.md', encoding='utf-8') as f:
    README = f.read()
  return README

setup(
  name="python-optiEncoder",
  version="2.0.1",
  description="A python package to optimally encode a list",
  long_description=readme(),
  long_description_content_type="text/markdown",
  author="Sahil Ahuja",
  author_email="sahil27ahuja1999@gmail.com",
  license="MIT",
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  packages=["optiEncoder"],
  include_package_data=True,
  install_requires=[            # I get to this in a second
    'pandas',
  ],
)