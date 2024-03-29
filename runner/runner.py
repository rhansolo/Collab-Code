import subprocess
import sys
import argparse
import os
import pickle
import time

TIME_LIMIT = 2 # Time limit in seconds

def run_java(file_path, question_path):
    file_path, file_name = os.path.split(file_path)

    compiler = subprocess.Popen(['javac', os.path.join(file_path, file_name)], stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                encoding='utf8')

    c_o = compiler.communicate()
    c_rc = compiler.returncode

    if c_rc != 0:
        return c_o[1]

    question = pickle.load(open(question_path, 'rb'))[1]

    results = []

    for case, answer in question:
        try:
            runner = subprocess.Popen(['java', '-cp', file_path, file_name.split('.')[0]]+case,
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

    return results

def run_python(file_path, question_path):

    question = pickle.load(open(question_path, 'rb'))[1]
    results = []

    runner = subprocess.Popen(['python3','-O', file_path]+question[0][0],
                                                stdout=subprocess.PIPE,
                                                stdin=subprocess.PIPE,
                                                stderr=subprocess.PIPE, encoding='utf8')

    start = time.time()
    time_exceeded = False
    while runner.poll() is None:
        if time.time()-start > TIME_LIMIT:
            time_exceeded = True
            runner.kill()

    if runner.returncode != 0 and time_exceeded == False:
        return runner.communicate()[1]

    for case, answer in question:
        try:
            runner = subprocess.Popen(['python3','-O', file_path]+case,
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

    return results

def run_cpp(file_path, question_path):
    file_path, file_name = os.path.split(file_path)

    compiler = subprocess.Popen(['g++', '-O2', '-lm', '-std=c++0x', os.path.join(file_path, file_name), '-o', os.path.join(file_path, 'Solution.out')], stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                encoding='utf8')

    c_o = compiler.communicate()
    c_rc = compiler.returncode

    if c_rc != 0:
        return c_o[1]

    question = pickle.load(open(question_path, 'rb'))[1]

    results = []

    for case, answer in question:
        try:
            runner = subprocess.Popen([os.path.join('.', file_path, 'Solution.out')]+case,
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

    return results
