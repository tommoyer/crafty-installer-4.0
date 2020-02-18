import sys
import platform
import logging
import subprocess

from app.helper import helper
from app.pretty import pretty


def print_intro():
    msg = "-" * 25
    msg += "# \t \t Crafty Controller Linux Installer \t \t #"
    msg += "-" * 25
    msg += "\n \t\t\t This program will install Crafty Controller on your Linux Machine"
    msg += "\n \t\t\t This program isn't perfect, but will do it's best to get you up an running"

    msg += "\n"
    pretty.header(msg)


if __name__ == "__main__":
    logging.basicConfig(filename='../installer.log',
                        filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    print_intro()

    # are we on linux?
    if platform.system() != "Linux":
        pretty.critical("This script requires Linux")
        logging.critical("This script requires Linux")
        sys.exit(1)

    pretty.info("Linux Check Success")

    # are we on Python 3.7+?
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 7):
        pretty.critical("This script requires Python 3.7 or higher!")
        pretty.critical("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
        logging.critical("Python Version < 3.7: {}.{} was found".format(sys.version_info.major, sys.version_info.minor))

        # offer ubuntu install
        if "ubuntu" in str(platform.uname()).lower():
            pretty.info("Ubuntu detected")
            install_requirements = helper.get_user_valid_input("Install Ubuntu requirements?", ['y', 'n'])
            if install_requirements == "y":
                pretty.info("Installing required packages for Ubuntu - Please enter sudo password when prompted")
                subprocess.check_output("app/ubuntu_install_depends.sh")



