from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

major_version = 0
minor_version = 1
build_version = 1

version = '{0}.{1}.{2}'.format(major_version, minor_version, build_version)

setup(name='image_colors',
      version=version,
      description='Image color extraction',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Other Audience',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Graphics',
      ],
      keywords='image average color',
      url='',
      author='Rhys Hansen',
      author_email='rhyshonline@gmail.com',
      license='MIT',
      packages=['image_colors'],
      install_requires=[
          'Pillow',
      ],
      include_package_data=True,
      zip_safe=False)
