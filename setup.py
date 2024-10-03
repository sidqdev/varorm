from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

with open("LICENSE", 'r') as f:
    license = f.read()

project_urls = {
  'GitHub': 'https://github.com/sidqdev/varorm',
  'Telegram': 'https://t.me/sidqdev'
}


setup(
    name='varorm',
    version='0.1.5',
    author='Sidq',
    author_email='abba.dmytro@gmail.com',
    description='Variable orm with django admin support',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=license,
    project_urls=project_urls,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    package_data={'varorm.dj': ['templates/*.html']},
    include_package_data=True,
    python_requires='>=3.6',
)

