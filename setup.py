from setuptools import setup, find_packages


def readme(file='', split=False):
    with open(file) as f:
        if split:
            return f.readlines()
        else:
            return f.read()


setup(
    name='IoTbs',
    version='0.0.1',
    description='Slack MQTT based interface for IoT Signage',
    long_description=readme('README.md'),
    url='https://github.com/stucamp/IoTbs',
    author='Stu Campbell',
    author_email='stucampbell.git@gmail.com',
    packages=find_packages(),
    python_requires='>=3.8',
    license='MIT License',
    install_requires=[
        'Flask',
        'paho-mqtt',
        'python-dotenv',
        'requests',
        'slack',
        'slackclient',
        'slackeventsapi',
    ],
    classifiers=[
        'Topic :: Communications',
        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',

    ],
)
