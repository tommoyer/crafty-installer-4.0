#!/usr/bin/env python3

import os
import sys
import json
import time
import distro as pydistro
import shutil
import platform
import logging
import subprocess

from app.helper import helper
from app.pretty import pretty

with open('config.json', 'r') as fh:
    defaults = json.load(fh)

if len(sys.argv) > 1:
    if sys.argv[1] == "-d":
        defaults['debug_mode'] = True
        pretty.info("Debug mode turned on")


#our pretty header
def do_header():

    if not defaults['debug_mode']:
        helper.clear_screen()

    msg = "-" * 25
    msg += "# \t \t Crafty Controller Linux Installer \t \t #"
    msg += "-" * 25
    msg += "\n \t\t\t This program will install Crafty Controller on your Linux Machine"
    msg += "\n \t\t\t This program isn't perfect, but it will do it's best to get you up an running"

    msg += "\n"
    pretty.header(msg)


def get_valid_input(question: str, answers: list ):
    valid = False

    while not valid:
        response = input("{} - {}: ".format(question, answers))

        if int(response) in list(answers):
            return int(response)


# here we can define other distro shell scripts for even better support
def do_distro_install(distro):
    real_dir = os.path.abspath(os.curdir)

    pretty.warning("This install could take a long time depending on how old your system is.")
    pretty.warning("Please be patient and do not exit the installer otherwise things may break")

    if distro == "ubuntu_18_04.sh":
        pretty.info("We are updating Apt, python3.7, open-jdk, pip, and virtualenv")
        script = os.path.join(real_dir, 'app', 'ubuntu_18_04.sh')

    elif distro == "debian_10.sh":
        pretty.info("We are updating Apt, python3.7, open-jdk, pip, and virtualenv")
        script = os.path.join(real_dir, 'app', 'debian_10.sh')

    elif distro == "ubuntu_20_04.sh":
        pretty.info("We are updating Apt, python3.8, open-jdk, pip, and virtualenv")
        script = os.path.join(real_dir, 'app', 'ubuntu_20_04.sh')

    else:
        pretty.critical("Unknown Distro: {}".format(distro))
        sys.exit(1)

    logger.info("Running {}".format(script))

    #resp = subprocess.check_output("app/ubuntu_install_depends.sh", shell=True)
    try:
        p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE)
        while True:
            line = p.stdout.readline()
            if not line:
                break
            print(line.decode("utf-8"))

    except Exception as e:

        pretty.critical("Error installing dependencies: {}".format(e))
        logger.critical("Error installing dependencies: {}".format(e))

# creates the venv and clones the git repo
def setup_repo():
    do_header()

    # create new virtual environment
    pretty.info("Creating New Virtual Environment")

    venv_dir = os.path.join(install_dir, 'venv')

    # changing to install dir
    os.chdir(install_dir)
    pretty.info("Jumping into install directory: {}".format(os.path.abspath(os.curdir)))
    logger.info("Changed directory to: {}".format(os.path.abspath(os.curdir)))

    # creating venv
    try:
        subprocess.check_output('virtualenv --python=/usr/bin/python3 {}'.format(venv_dir), shell=True)
    except Exception as e:
        logger.critical("Unable to create virtual environment!")
        logger.critical("Error: {}".format(e))
        sys.exit(1)

    # cloning the repo
    pretty.info("Cloning the Git Repo...this could take a few moments")
    subprocess.check_output('git clone http://gitlab.com/crafty-controller/crafty-web.git', shell=True)


# this switches to the branch chosen and does the pip install and such
def do_virt_dir_install():
    do_header()

    # choose your destiny
    pretty.info("Choose your destiny:")
    pretty.info("Crafty comes in different branches:")
    pretty.info("Master - Most Stable, should be bug free")
    pretty.info("Beta - Pretty Stable, very few bugs known")
    pretty.info("Snaps - Unstable, but full of exciting things!")
    pretty.info("Dev - Highly Unstable, full of bugs and new features")

    # unattended
    if not defaults['unattended']:
        branch = helper.get_user_valid_input("Which branch of Crafty would you like to run?", ['master',
                                                                                           'beta',
                                                                                           'snaps',
                                                                                           'dev'])
    else:
        branch = defaults['branch']

    # changing to git repo dir
    os.chdir(os.path.join(install_dir, "crafty-web"))
    pretty.info("Jumping into repo directory: {}".format(os.path.abspath(os.curdir)))
    logger.info("Changed directory to: {}".format(os.path.abspath(os.curdir)))

    logger.info("User choose {} branch".format(branch))

    # default empty output
    git_output = ""

    # branch selection
    if branch == 'master':
        pretty.info("Slow and Stable it is")

    elif branch == "beta":
        pretty.info("The beta branch is a great choice")

    elif branch == 'snaps':
        pretty.info("Snaps is where the cool kids hangout")

    elif branch == 'dev':
        pretty.info("Way to saddle up cowboy!")

    # create a quick script / execute pip install
    do_pip_install(branch)

# installs pip requirements via shell script
def do_pip_install(branch):
    src = os.path.join(starting_dir, 'app', 'pip_install_req.sh')
    dst = os.path.join(install_dir, 'pip_install_req.sh')

    logger.info("Copying PIP install script")
    shutil.copyfile(src, dst)

    pip_command = "{} '{}' {}".format(dst, install_dir, branch)

    logger.info("Chmod +x {}".format(dst))
    subprocess.check_call("chmod +x {}".format(dst), shell=True)

    logger.info('Running Pip: {}'.format(pip_command))
    pretty.warning("We are now going to install all the python modules for Crafty - This process can take awhile depending on your internet connection")

    time.sleep(3)

    try:
        p = subprocess.Popen([pip_command], shell=True, stdout=subprocess.PIPE)
        while True:
            line = p.stdout.readline()
            if not line:
                break
            print(line.decode("utf-8"))

        # pip_output = subprocess.check_output(pip_command, shell=True)
        # logger.info("Pip output: \n{}".format(pip_output))

    except Exception as e:
        logger.error("Pip failed due to error: {}".format(e))

    if not defaults['debug_mode']:
        os.remove(dst)


# Creates the run_crafty.sh
def make_startup_script():
    os.chdir(install_dir)
    logger.info("Changing to {}".format(os.path.abspath(os.curdir)))

    txt = "#!/bin/bash\n"
    txt += "cd {}\n".format(install_dir)
    txt += "source venv/bin/activate \n"
    txt += "cd crafty-web \n"
    txt += "python{}.{} crafty.py \n".format(sys.version_info.major, sys.version_info.minor)
    with open("run_crafty.sh", 'w') as fh:
        fh.write(txt)
        fh.close()

    subprocess.check_output("chmod +x *.sh", shell=True)


# Creates the update_crafty.sh
def make_update_script():
    os.chdir(install_dir)
    logger.info("Changing to {}".format(os.path.abspath(os.curdir)))

    txt = "#!/bin/bash\n"
    txt += "cd {}\n".format(install_dir)
    txt += "source venv/bin/activate \n"
    txt += "cd crafty-web \n"
    txt += "git pull \n"
    txt += "pip3 install -r requirements.txt \n"
    with open("update_crafty.sh", 'w') as fh:
        fh.write(txt)
        fh.close()

    subprocess.check_output("chmod +x *.sh", shell=True)


# Creates the run as a service.sh
def make_service_script():
    os.chdir(install_dir)
    logger.info("Changing to {}".format(os.path.abspath(os.curdir)))

    txt = "#!/bin/bash\n"
    txt += "cd {}\n".format(install_dir)
    txt += "source venv/bin/activate \n"
    txt += "cd crafty-web \n"
    txt += "python{}.{} crafty.py -d\n".format(sys.version_info.major, sys.version_info.minor)
    with open("run_crafty_service.sh", 'w') as fh:
        fh.write(txt)
        fh.close()

    subprocess.check_output("chmod +x *.sh", shell=True)


def make_service_file():
    os.chdir(install_dir)
    logger.info("Changing to {}".format(os.path.abspath(os.curdir)))
    txt = """
[Unit]
Description=Crafty Controller
After=network.target

[Service]
Type=simple

User=crafty
WorkingDirectory={0}

ExecStart={0}/run_crafty_service.sh

Restart=on-failure
# Other restart options: always, on-abort, etc

# The install section is needed to use
# `systemctl enable` to start on boot
# For a user service that you want to enable
# and start automatically, use `default.target`
# For system level services, use `multi-user.target`
[Install]
WantedBy=multi-user.target
""".format(install_dir)

    with open("crafty.service", 'w') as fh:
        fh.write(txt)
        fh.close()

    subprocess.check_output("cp crafty.service /etc/systemd/system/crafty.service", shell=True)


# get distro
def get_distro():
    id = pydistro.id()
    version = pydistro.version()
    print(f"ID: {id} Version: {version}")
    # get distro
    if id == "debian":
        if version == "10":
            # logger.info("Debian 10 'Buster' Selected")
            file = "debian_10.sh"
        else:
            file = "error debian"
            # pretty.critical("Unsupported version: {}".format(distro))
            # sys.exit(1)
    elif id == "ubuntu":
        if version == "18.04":
            # logger.info("Ubuntu 18.04 Selected")
            file = "ubuntu_18_04.sh"
        elif version == "20.04":
            # logger.info("Ubuntu 20.04 Selected")
            file = "ubuntu_20_04.sh"
        else:
            file = "error Ubuntu"
            # pretty.critical("Unsupported version: {}".format(distro))
            # sys.exit(1)
    else:
        file = "error distro"
        pretty.critical("Unknown Distro: {}".format(distro))
        sys.exit(1)
    #print(f"Ouput: {file}")
    return file

if __name__ == "__main__":

    logging.basicConfig(filename='installer.log',
                        filemode='w',
                        format='[+] Crafty Installer: %(levelname)s - %(message)s',
                        level=logging.INFO)

    logger = logging.getLogger(__name__)

    logger.info("Installer Started")

    starting_dir = os.path.abspath(os.path.curdir)
    temp_dir = os.path.join(starting_dir, 'temp')

    do_header()

    # are we on linux?
    if platform.system() != "Linux":
        pretty.critical("This script requires Linux")
        logger.critical("This script requires Linux")
        sys.exit(1)

    pretty.info("Linux Check Success")
    pretty.info("Python Version Check - {}.{}".format(sys.version_info.major, sys.version_info.minor))

    distro = get_distro()
    if not distro:
        pretty.critical("Unable to find distro information, or your distro is not supported.")
        logger.critical("Unable to find distro information")
        sys.exit(1)

    # default py_check
    py_check = False

    # are we at least on 3.6?
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
        pretty.critical("This script requires Python 3.6 or higher!")
        pretty.critical("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
        logger.critical("Python Version < 3.6: {}.{} was found".format(sys.version_info.major, sys.version_info.minor))
        time.sleep(1)
        pretty.warning("Your python version didn't check out - do you want us to fix this for you?")
    else:
        py_check = True

    # unattended
    if not defaults['unattended']:
        install_requirements = helper.get_user_valid_input("Install {} requirements?".format(distro), ['y', 'n'])
    else:
        install_requirements = 'y'

    if install_requirements == "y":
        pretty.info("Installing required packages for {} - Please enter sudo password when prompted".format(distro))
        do_distro_install(distro)
    else:
        if not py_check:
            pretty.critical("This script requires Python 3.6 or higher!")
            sys.exit(1)

    do_header()

    # do we want to install to default dir?
    pretty.info("Crafty's Default install directory is set to: {}".format(defaults['install_dir']))

    # unattended
    if not defaults['unattended']:
        install_dir = helper.get_user_valid_input(
            "Install Crafty to this directory? {}".format(defaults['install_dir']),
            ["y", "n"])
    else:
        install_dir = 'y'

    do_header()

    if install_dir == 'n':
        install_dir = helper.get_user_open_input("Where would you like Crafty to install to?")
    else:
        install_dir = defaults['install_dir']

    pretty.info("Installing Crafty to {}".format(install_dir))
    logger.info("Installing Crafty to {}".format(install_dir))

    # can we write to the dir?
    if not helper.check_writeable(install_dir):
        pretty.warning("Unable to write to {} - Permission denied".format(install_dir))
        logger.warning("Unable to write to {} - Permission denied".format(install_dir))

        # unattended
        if not defaults['unattended']:
            own_install_dir = helper.get_user_valid_input("Do you want us to fix this permission issue?", ['y', 'n'])
        else:
            own_install_dir = "y"

        if own_install_dir == "y":
            try:
                # make a temp dir
                helper.ensure_dir_exists(temp_dir)

                # let's create a quick sh script to create the dir as root, and then chown the dir to the current user
                fix_perms_sh = os.path.join(temp_dir, 'fix_perms.sh')

                with open(fix_perms_sh, 'w') as fh:
                    txt = "#!/bin/bash\n"
                    txt += "sudo mkdir -p {}\n".format(install_dir)
                    txt += "sudo chown crafty:crafty {}\n".format(install_dir)
                    fh.write(txt)
                    fh.close()

                    subprocess.check_output("chmod +x {}".format(fix_perms_sh), shell=True)
                    subprocess.check_output(fix_perms_sh, shell=True)

                    if not helper.check_writeable(install_dir):
                        logger.critical("Unable to fix permissions issue after shell script")
                        pretty.critical("Unable to fix permissions issue")
                        sys.exit(1)


            except Exception as e:
                logger.critical("Unable to fix permissions issue")
                pretty.critical("Unable to fix permissions issue")

            # after changing the ownership, let's see if we can write to it now.
            if not helper.check_writeable(install_dir):
                logger.critical("{} is still unwritable - Unable to fix permissions issue".format(install_dir))
                sys.exit(1)

    # is this a fresh install?
    files = os.listdir(install_dir)

    time.sleep(1)

    do_header()

    logger.info("Looking for old crafty install in: {}".format(install_dir))

    if len(files) > 0:
        logger.warning("Old Crafty install detected: {}".format(install_dir))
        pretty.info("Old Crafty Install Detected, do you wish to delete this old install?")

        # unattended
        if not defaults['unattended']:
            del_old = helper.get_user_valid_input("Delete files in {}? ".format(install_dir), ['y', 'n'])
        else:
            del_old = "y"

        if del_old == "y":
            logger.info("User said to delete old files")
            pretty.info("Deleting old copies of Crafty")

            try:
                shutil.rmtree(install_dir)

            except Exception as e:
                pretty.warning("Unable to write to {} - Permission denied".format(install_dir))
                logger.warning("Unable to write to {} - Permission denied".format(install_dir))

                # unattended
                if not defaults['unattended']:
                    force_old_removal = helper.get_user_valid_input("Do you want us to fix this permission issue?",
                                                              ['y', 'n'])
                else:
                    force_old_removal = "y"

                if force_old_removal == "y":

                    helper.ensure_dir_exists(temp_dir)

                    remove_old_dir_script = os.path.join(temp_dir, 'force_old_removal.sh')

                    with open(remove_old_dir_script, 'w') as fh:
                        txt = "#!/bin/bash\n"
                        txt += "sudo rm -rf {}\n".format(install_dir)
                        fh.write(txt)
                        fh.close()
                        subprocess.check_output("chmod +x {}".format(remove_old_dir_script), shell=True)
                        subprocess.check_output(remove_old_dir_script, shell=True)

                    try:
                        files = os.listdir(install_dir)
                    except:
                        pass

                    if len(files) > 0:
                        logger.critical("Unable to delete the old install directory")
                        pretty.critical("Unable to delete the old install directory")
                        sys.exit(1)

            helper.ensure_dir_exists(install_dir)

        else:
            logger.info("User is keeping old files")
            pretty.warning("Installing on top of an old install isn't supported - God Speed")

    setup_repo()

    do_virt_dir_install()

    do_header()

    logger.info("Creating Shell Scripts")
    pretty.info("Making start and update scripts for you")

    make_startup_script()
    make_update_script()

    service_answer = helper.get_user_valid_input("Would you like to make a service file for Crafty?", ['y', 'n'])
    if service_answer == "y":
        make_service_script()
        make_service_file()

    # fixing permission issues
    cmd = "sudo chown crafty:crafty -R {dir} && sudo chmod 2775 -R {dir}".format(dir=install_dir)
    subprocess.check_output(cmd, shell=True)

    time.sleep(1)
    do_header()

    # fix permission issues
    cmd = "chown crafty:crafty -R {dir} && chmod 2775 -R {dir}".format(dir=install_dir)
    subprocess.check_output(cmd, shell=True)

    pretty.info("Cleaning up temp dir")
    helper.ensure_dir_exists(temp_dir)

    if not defaults['debug_mode']:
        shutil.rmtree(temp_dir)

    pretty.info("Congrats! Crafty is now installed!")
    pretty.info("We created a user called 'crafty' for you to run crafty as.")
    pretty.info("Your install is located here: {}".format(install_dir))
    pretty.info("You can run crafty by running {}".format(os.path.join(install_dir, "run_crafty.sh")))
    pretty.info("You can update crafty by running {}".format(os.path.join(install_dir, "update_crafty.sh")))
    if service_answer:
        pretty.info("A service unit file has been saved in /etc/systemd/system/crafty.service")
        pretty.info("You will need to run Crafty once normally to get the admin password before enabling the service or running the command 'sudo systemctl status crafty.service' after starting the service")
        pretty.info("run this command to enable crafty as a service- 'sudo systemctl enable crafty.service' ")
        pretty.info("run this command to start the crafty service- 'sudo systemctl start crafty.service' ")

