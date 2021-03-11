"""
"""

import sys
from painter import application

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def main() -> int:
    """
    Main entry point into the application
    """

    app = application.PainterApplication(sys.argv)
    app.exec_()

    return 0

# Main entry point into the application
if __name__ == '__main__':
    sys.exit(main())

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#