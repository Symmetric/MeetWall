from distutils.core import setup

setup(
    name="dispatcher",
    packages=["dispatcher"],
    version="0.0.1",
    description="Universal encoding detector",
    author="Paul Tiplady",
    author_email="paul.tiplady@gmail.com",
    url="http://github.com/symmetric/BodySensor",
    # download_url="http://chardet.feedparser.org/download/python3-chardet-1.0.1.tgz",
    # keywords=["encoding", "i18n", "xml"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        'console_scripts': [
            'dispatcher_server = dispatcher.server:run_server',
            'dispatcher_client = dispatcher.client:send_to_server',
        ]
    }
)