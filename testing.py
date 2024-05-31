# This file is used to test the main.py file

import os
from colorama import Fore, Back, Style
from main import main

# Test all the files inside the test directory
def test_all_files():
    # create testing dir
    if not os.path.exists("testing_cache"):
        os.mkdir("testing_cache")
    ## Grab all the directories in the test directory
    directories = os.listdir("test")
    ## Loop through all the directories
    for directory in directories:
        print(Fore.BLUE + f"-----------------------------")
        print(Fore.GREEN + f"Testing {directory}")
        ## Grab all the files in the directory
        files = os.listdir(f"test/{directory}")
        ## Loop through all the files
        for file in files:
            ## Run the test
            run_test(f"test/{directory}/{file}")
    delete_cache()

# Example test is many lines of statments and final line is the expected result

def run_test(file):
    # Read the file
    with open(file) as f:
        lines = f.readlines()
        expected_result = lines[-1]
        ## Create a new file with all but the same line
        #Create the dir if it does not exist
        paths = file.split("/")
        for i in range(1, len(paths)):
            if not os.path.exists(f"testing_cache/{'/'.join(paths[:i])}"):
                os.mkdir(f"testing_cache/{'/'.join(paths[:i])}")

        new_file = open(f"testing_cache/{file}", "w")
        new_file.write("".join(lines[:-1]))
        new_file.close()


        # Run the main.py file
        try:
            res = main(f"testing_cache/{file}")
        except Exception as e:
            print(Fore.RED + f"❌Test {file} failed e:{e}")
        res =  str(main(f"testing_cache/{file}")).replace("\n","")
        # Compare the results
        if res == expected_result:
            print(f"🧪Test {file} passed: exp:{expected_result},res:{res}")
        else:
            print(Fore.RED + f"❌Test {file} failed exp:{expected_result},res:{res}")

def delete_cache():
    os.system("rm -rf testing_cache")

test_all_files()