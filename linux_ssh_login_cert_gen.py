"""code to generate a new public and private key pair use to login as the current user in ubuntu"""
import os
import subprocess
import sys
import time
import getpass  # to get the current user name
import shutil  # to copy the files
import stat  # to change the permissions of the files
import pwd  # to get the user id
import grp  # to get the group id
import re  # to check if the key is already in the authorized_keys file
import argparse  # to parse the command line arguments
import logging  # to log the actions
import logging.handlers  # to log the actions
import datetime  # to get the current date and time
import socket  # to get the hostname
import tempfile  # to create a temporary directory
import fileinput  # to edit the files
import glob  # to find the files
import platform  # to get the OS name and version

#function to get the current user name
def get_current_user():
    """get the current user name"""
    return getpass.getuser()

#function to get the user id
def get_user_id(user_name):
    """get the user id"""
    return pwd.getpwnam(user_name).pw_uid

#funtion to get password
def get_password():
    """get the password"""
    return getpass.getpass()

#function to create a temporary directory
def create_temp_dir():
    """create a temporary directory"""
    return tempfile.mkdtemp()

#function to generate a new public and private key pair
def generate_key_pair(temp_dir, user_name):
    """generate a new public and private key pair"""
    #create a new key pair
    subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-C", user_name, "-f", temp_dir + "/id_rsa"], check=True)
    #change the permissions of the private key
    os.chmod(temp_dir + "/id_rsa", stat.S_IRUSR | stat.S_IWUSR)
    #change the permissions of the public key
    os.chmod(temp_dir + "/id_rsa.pub", stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

#function to get the public key
def get_public_key(temp_dir):
    """get the public key"""
    #open the public key file
    with open(temp_dir + "/id_rsa.pub", "r") as public_key_file:
        #read the public key
        public_key = public_key_file.read()
    #return the public key
    return public_key

#function to copy the public key to the authorized_keys file
def copy_public_key_to_authorized_keys(public_key, user_name):
    """copy the public key to the authorized_keys file"""
    #open the authorized_keys file
    with open("/home/" + user_name + "/.ssh/authorized_keys", "a") as authorized_keys_file:
        #write the public key to the authorized_keys file
        authorized_keys_file.write(public_key)

#function to copy the private key to the .ssh directory
def copy_private_key_to_ssh_dir(temp_dir, user_name):
    """copy the private key to the .ssh directory"""
    #copy the private key to the .ssh directory
    shutil.copy(temp_dir + "/id_rsa", "/home/" + user_name + "/.ssh/id_rsa")

#function to change the permissions of the private key
def change_permissions_of_private_key(user_name):
    """change the permissions of the private key"""
    #change the permissions of the private key
    os.chmod("/home/" + user_name + "/.ssh/id_rsa", stat.S_IRUSR | stat.S_IWUSR)

#FUNCTION TO COPY PRIVATE KEY TO HOME
def copy_private_key_to_home(temp_dir, user_name):
    """copy the private key to the home directory"""
    #copy the private key to the home directory
    shutil.copy(temp_dir + "/id_rsa", "/home/" + user_name + "/id_rsa")

#main function
def main():
    """main function"""
    #get the current user name
    user_name = get_current_user()
    #get the user id
    user_id = get_user_id(user_name)
    #get the password
    password = get_password()
    #create a temporary directory
    temp_dir = create_temp_dir()
    #generate a new public and private key pair
    generate_key_pair(temp_dir, user_name)
    #get the public key
    public_key = get_public_key(temp_dir)
    #copy the public key to the authorized_keys file
    copy_public_key_to_authorized_keys(public_key, user_name)
    #copy the private key to the .ssh directory
    copy_private_key_to_ssh_dir(temp_dir, user_name)
    #change the permissions of the private key
    change_permissions_of_private_key(user_name)
    #copy the private key to the home directory
    copy_private_key_to_home(temp_dir, user_name)


#run the main function
# if this file is run as a script
# and not imported as a module
# then run the main function
# to start the program
if __name__ == "__main__":
    #run the main function
    main()
