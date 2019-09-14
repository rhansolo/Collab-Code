import subprocess
import sys
import argparse
import os
import pickle
import time

TIME_LIMIT = 2 # Time limit in seconds

def run_java(file_path, question_path):
    curr_dir = os.getcwd()
    file_path, file_name = os.path.split(file_path)

    os.chdir(file_path if file_path != '' else '.')

    compiler = subprocess.Popen(['javac', file_name], stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                encoding='utf8')

    c_o = compiler.communicate()
    c_rc = compiler.returncode

    if c_rc != 0:
        os.chdir(curr_dir)
        return c_o[1]

    question = pickle.load(open(question_path, 'rb'))[1]

    results = []

    for case, answer in question:
        try:
            runner = subprocess.Popen(['java', file_name.split('.')[0]]+case,
                                      stdout=subprocess.PIPE,
                                      stdin=subprocess.PIPE,
                                      stderr=subprocess.PIPE, encoding='utf8')

            start = time.time()
            time_exceeded = False
            while runner.poll() is None:
                if time.time()-start > TIME_LIMIT:
                    time_exceeded = True
                    runner.kill()

            if time_exceeded:
                results += 't'
            elif runner.returncode != 0:
                results += 'e'
            else:
                output = runner.communicate()[0].split()
                if output == answer:
                    results += 'c'
                else:
                    results += 'i'
        except:
            results += ["fuck?"]
    os.chdir(curr_dir)

    return results
