"""
"""

import sys
from setuptools import setup
from painter import __version__ as version

#----------------------------------------------------------------------------------------------------------------------------------#

def main() -> int:
    """
    Main entry point for the setuptools script
    """

    setup(
        name='Painter',
        version=version,
        packages=['painter'],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        options={})

    return 0

# Main entry point for the setuptools script
if __name__ == '__main__':
    sys.exit(main())

#----------------------------------------------------------------------------------------------------------------------------------#