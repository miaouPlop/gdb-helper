from setuptools import setup

setup(
    name='gdbhelper',
    version='0.1',
    packages=['gdbhelper'],
    install_requires=[
        'pwntools',
        'psutil'
    ],
    url='https://github.com/miaouPlop/gdb-helper',
    license='MIT',
    author='miaouPlop',
    author_email='yorick.lesecque@gmail.com',
    description='GDB lightweight instrumentation'
)
