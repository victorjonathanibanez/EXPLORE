from setuptools import setup, find_packages

setup(
    name='explore',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        # List your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
        ],
    },
    # Other project metadata
    author='Victor Ibañez',
    author_email='victor.ibanez@uzh.ch',
    description='object recognition test analysis with deep learning',
    long_description='A longer description of your package',
    url='https://github.com/victorjonathanibanez/EXPLORE',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Researchers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
