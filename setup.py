from setuptools import setup


setup(
    name='mu',
    version='0.1',
    description='A simple editor for kids, teachers and new programmers.',
    author='Nicholas Tollervey',
    author_email='ntoll@ntoll.org',
    url='https://github.com/ntoll/mu',
    packages=['mu'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Education',
        'Topic :: Education',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            "mu = mu.app.run",
        ],
    },
    data_files=[('/etc/udev/rules.d', ['conf/90-usb-microbit.rule', ]),
                ('/usr/share/pixmaps', ['conf/mu.png', ]),
                ('/usr/share/applications', ['conf/mu.desktop', ])],
)
