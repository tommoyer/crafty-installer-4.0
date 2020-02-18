import os
import time
import subprocess
import logging

logger = logging.getLogger(__name__)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class helper_obj:

    def clear_screen(self):
        time.sleep(.5)
        os.system('clear')

    def run_command(self, command_list):
        process = subprocess.Popen(['ls', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return out, err

    def get_user_valid_input(self, q, valid_answers):
        while True:
            n = input("\n{}{} - {}{}: ".format(bcolors.BOLD, q, valid_answers, bcolors.ENDC)).lower()
            if n in valid_answers:
                return n

    def get_user_open_input(self, q):
        n = input("\n{}{}{}: ".format(bcolors.BOLD, q, bcolors.ENDC))
        return n

    def ensure_dir_exists(self, path):
        try:
            os.makedirs(path)
            logging.debug("Created Directory : {}".format(path))

        # directory already exists - non-blocking error
        except FileExistsError:
            pass

    def check_writeable(self, path):
        filename = os.path.join(path, "tempfile.txt")
        try:
            fp = open(filename, "w").close()
            os.remove(filename)

            logging.info("{} is writable".format(filename))
            return True

        except Exception as e:
            logging.critical("Unable to write to {} - Error: {}".format(path, e))
            return False

    def check_file_exists(self, path):
        if os.path.exists(path) and os.path.isfile(path):
            logging.debug('Found path: {}'.format(path))
            return True
        else:
            return False



helper = helper_obj()