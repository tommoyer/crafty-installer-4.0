import os
import sys
import shutil
import logging
import argparse
import platform
import subprocess

from app.helper import helper
from app.pretty import pretty

defaults = {
    'install_dir': "/var/opt/minecraft/crafty",
}



    logging.info("Python version {}.{} found - Continuing".format(sys.version_info.major, sys.version_info.minor))
    pretty.info("Python version {}.{} found".format(sys.version_info.major, sys.version_info.minor))

    # do we want to install to default dir?
    install_dir = helper.get_user_valid_input("Install Crafty to this directory? {}".format(defaults['install_dir']),
                                       ["y", "n"])
    if install_dir == 'n':
        install_dir = helper.get_user_open_input("Where would you like Crafty to install?")
        pretty.info("Installing Crafty to {}".format(install_dir))
    else:
        install_dir = defaults['install_dir']
        pretty.info("Installing Crafty to /var/opt/minecraft/crafty")

    # make sure the directory is there
    helper.ensure_dir_exists(install_dir)

    # can we write to the dir?
    if not helper.check_writeable(install_dir):
        pretty.critical("Unable to write to {} - Permission denied".format(install_dir))
        logging.critical("Unable to write to {} - Permission denied".format(install_dir))
        sys.exit(1)

    # is this a fresh install?
    files = os.listdir(install_dir)

    logging.info("Looking for old crafty install in: {}".format(install_dir))

    if len(files) > 0:
        logging.warning("Old Crafty install detected: {}".format(install_dir))
        pretty.info("Old Crafty Install Detected, do you wish to delete this old install?")
        del_old = helper.get_user_valid_input("Delete files in {}? ".format(install_dir), ['y', 'n'])

        if del_old == "y":
            logging.info("User said to delete old files")
            pretty.info("Deleting old copies of Crafty")
            shutil.rmtree(install_dir)
            helper.ensure_dir_exists(install_dir)

        else:
            logging.info("User is keeping old files")
            pretty.warning("Installing on top of an old install isn't supported - God Speed")












