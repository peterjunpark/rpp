"""
MIT License

Copyright (c) 2019 - 2024 Advanced Micro Devices, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys
sys.dont_write_bytecode = True
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..' ))
from common import *

# Set the timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

scriptPath = os.path.dirname(os.path.realpath(__file__))
headerFilePath = scriptPath + "/../TEST_QA_IMAGES_VOXEL"
dataFilePath = scriptPath + "/../TEST_QA_IMAGES_VOXEL"
qaInputFile = scriptPath + "/../TEST_QA_IMAGES_VOXEL"
outFolderPath = os.getcwd()
buildFolderPath = os.getcwd()
caseMin = 0
caseMax = 5

# Get a list of log files based on a flag for preserving output
def get_log_file_list():
    return [
        outFolderPath + "/OUTPUT_PERFORMANCE_LOGS_HOST_VOXEL_" + timestamp + "/Tensor_voxel_host_pkd3_raw_performance_log.txt",
        outFolderPath + "/OUTPUT_PERFORMANCE_LOGS_HOST_VOXEL_" + timestamp + "/Tensor_voxel_host_pln3_raw_performance_log.txt",
        outFolderPath + "/OUTPUT_PERFORMANCE_LOGS_HOST_VOXEL_" + timestamp + "/Tensor_voxel_host_pln1_raw_performance_log.txt"
    ]

# Functionality group finder
def func_group_finder(case_number):
    if case_number == 0:
        return "arithmetic_operations"
    elif case_number == 1:
        return "geometric_augmentations"
    else:
        return "miscellaneous"

def run_unit_test(headerPath, dataPath, dstPathTemp, layout, case, numRuns, testType, qaMode, batchSize):
    print("\n\n\n\n")
    print("--------------------------------")
    print("Running a New Functionality...")
    print("--------------------------------")
    bitDepths = [0, 2]
    if qaMode:
        bitDepths = [2]
    for bitDepth in bitDepths:
        print("\n\n\nRunning New Bit Depth...\n-------------------------\n\n")
        print("\n\n\n\n")
        print(f"./Tensor_voxel_host {headerPath} {dataPath} {dstPathTemp} {layout} {case} {numRuns} {testType} {qaMode} {batchSize} {bitDepth}")
        result = subprocess.run([buildFolderPath + "/build/Tensor_voxel_host", headerPath, dataPath, dstPathTemp, str(layout), str(case), str(numRuns), str(testType), str(qaMode), str(batchSize), str(bitDepth), scriptPath], stdout=subprocess.PIPE) # nosec
        print(result.stdout.decode())
        print("------------------------------------------------------------------------------------------")

def run_performance_test(loggingFolder, logFileLayout, headerPath, dataPath, dstPathTemp, layout, case, numRuns, testType, qaMode, batchSize):
    print("\n\n\n\n")
    print("--------------------------------")
    print("Running a New Functionality...")
    print("--------------------------------")
    bitDepths = [0, 2]
    for bitDepth in bitDepths:
        with open(f"{loggingFolder}/Tensor_voxel_host_{logFileLayout}_raw_performance_log.txt", "a") as log_file:
            print(f"./Tensor_voxel_host {headerPath} {dataPath} {dstPathTemp} {layout} {case} {numRuns} {testType} {qaMode} {batchSize} {bitDepth}")
            process = subprocess.Popen([buildFolderPath + "/build/Tensor_voxel_host", headerPath, dataPath, dstPathTemp, str(layout), str(case), str(numRuns), str(testType), str(qaMode), str(batchSize), str(bitDepth), scriptPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) # nosec
            while True:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break
                print(output.strip())
                if "Running" in output or "max,min,avg wall times" in output:
                    cleaned_output = ''.join(char for char in output if 32 <= ord(char) <= 126)  # Remove control characters
                    cleaned_output = cleaned_output.strip()  # Remove leading/trailing whitespace
                    log_file.write(cleaned_output + '\n')
                    if "max,min,avg wall times" in output:
                        log_file.write("\n")
        print("------------------------------------------------------------------------------------------")

# Parse and validate command-line arguments for the RPP test suite
def rpp_test_suite_parser_and_validator():
    parser = argparse.ArgumentParser()
    parser.add_argument("--header_path", type = str, default = headerFilePath, help = "Path to the nii header")
    parser.add_argument("--data_path", type = str, default = dataFilePath, help = "Path to the nii data file")
    parser.add_argument("--case_start", type = int, default = caseMin, help = "Testing range starting case # - Range must be in [" + str(caseMin) + ":" + str(caseMax) + "]")
    parser.add_argument("--case_end", type = int, default = caseMax, help = "Testing range ending case # - Range must be in [" + str(caseMin) + ":" + str(caseMax) + "]")
    parser.add_argument('--test_type', type = int, default = 0, help = "Type of Test - (0 = Unit tests / 1 = Performance tests)")
    parser.add_argument('--case_list', nargs = "+", help = "List of case numbers to list", required = False)
    parser.add_argument('--qa_mode', type = int, default = 0, help = "Run with qa_mode? Output images from tests will be compared with golden outputs - (0 / 1)", required = False)
    parser.add_argument('--num_runs', type = int, default = 1, help = "Specifies the number of runs for running the performance tests")
    parser.add_argument('--preserve_output', type = int, default = 1, help = "preserves the output of the program - (0 = override output / 1 = preserve output )" )
    parser.add_argument('--batch_size', type = int, default = 1, help = "Specifies the batch size to use for running tests. Default is 1.")
    args = parser.parse_args()

    # check if the folder exists
    validate_path(args.header_path)
    validate_path(args.data_path)
    validate_path(qaInputFile)

    # validate the parameters passed by user
    if ((args.case_start < caseMin or args.case_start > caseMax) or (args.case_end < caseMin or args.case_end > caseMax)):
        print("Starting case# and Ending case# must be in the 0:1 range. Aborting!")
        exit(0)
    elif args.case_end < args.case_start:
        print("Ending case# must be greater than starting case#. Aborting!")
        exit(0)
    elif args.test_type < 0 or args.test_type > 1:
        print("Test Type# must be in the 0 / 1. Aborting!")
        exit(0)
    elif args.qa_mode < 0 or args.qa_mode > 1:
        print("QA mode must be in the 0 / 1. Aborting!")
        exit(0)
    elif args.case_list is not None and args.case_start > caseMin and args.case_end < caseMax:
        print("Invalid input! Please provide only 1 option between case_list, case_start and case_end")
        exit(0)
    elif args.num_runs <= 0:
        print("Number of Runs must be greater than 0. Aborting!")
        exit(0)
    elif args.batch_size <= 0:
        print("Batch size must be greater than 0. Aborting!")
        exit(0)
    elif args.preserve_output < 0 or args.preserve_output > 1:
        print("Preserve Output must be in the 0/1 (0 = override / 1 = preserve). Aborting")
        exit(0)

    if args.case_list is None:
        args.case_list = range(args.case_start, args.case_end + 1)
        args.case_list = [str(x) for x in args.case_list]
    else:
        for case in args.case_list:
            if int(case) < caseMin or int(case) > caseMax:
                print("The case# must be in [" + str(caseMin) + ":" + str(caseMax) + "]")
                exit(0)

    # if QA mode is enabled overwrite the input folders with the folders used for generating golden outputs
    if args.qa_mode:
        args.header_path = headerFilePath
        args.data_path = dataFilePath

    return args

args = rpp_test_suite_parser_and_validator()
headerPath = args.header_path
dataPath = args.data_path
caseStart = args.case_start
caseEnd = args.case_end
testType = args.test_type
caseList = args.case_list
qaMode = args.qa_mode
numRuns = args.num_runs
preserveOutput = args.preserve_output
batchSize = args.batch_size

if qaMode and os.path.abspath(qaInputFile) != os.path.abspath(headerPath):
    print("QA mode should only run with the given Input path: ", qaInputFile)
    exit(0)

if qaMode and batchSize != 3:
    print("QA mode can only run with a batch size of 3.")
    exit(0)

# set the output folders and number of runs based on type of test (unit test / performance test)
if(testType == 0):
    if qaMode:
        outFilePath = os.path.join(outFolderPath + "/QA_RESULTS_HOST_VOXEL_" + timestamp)
    else:
        outFilePath = os.path.join(outFolderPath + "/OUTPUT_VOXEL_HOST_" + timestamp)
    numRuns = 1
elif(testType == 1):
    if "--num_runs" not in sys.argv:
        numRuns = 100 #default numRuns for running performance tests
    outFilePath = os.path.join(outFolderPath + "/OUTPUT_PERFORMANCE_LOGS_HOST_VOXEL_" + timestamp)
else:
    print("Invalid TEST_TYPE specified. TEST_TYPE should be 0/1 (0 = Unittests / 1 = Performancetests)")
    exit()

if preserveOutput == 0:
    validate_and_remove_folders(outFolderPath, "OUTPUT_VOXEL_HOST")
    validate_and_remove_folders(outFolderPath, "QA_RESULTS_HOST_VOXEL")
    validate_and_remove_folders(outFolderPath, "OUTPUT_PERFORMANCE_LOGS_HOST_VOXEL")

os.mkdir(outFilePath)
loggingFolder = outFilePath
dstPath = outFilePath

# Validate DST_FOLDER
validate_and_remove_files(dstPath)

# Enable extglob
if os.path.exists(buildFolderPath + "/build"):
    shutil.rmtree(buildFolderPath + "/build")
os.makedirs(buildFolderPath + "/build")
os.chdir(buildFolderPath + "/build")

# Run cmake and make commands
subprocess.run(["cmake", scriptPath], cwd=".")   # nosec
subprocess.run(["make", "-j16"], cwd=".")  # nosec

# List of cases supported
supportedCaseList = ['0', '1', '2', '3', '4', '5']

print("\n\n\n\n\n")
print("##########################################################################################")
print("Running all layout Inputs...")
print("##########################################################################################")

bitDepths = [0, 2]
if testType == 0:
    for case in caseList:
        if case not in supportedCaseList:
            continue
        for layout in range(3):
            dstPathTemp, logFileLayout = process_layout(layout, qaMode, case, dstPath, "host", func_group_finder)
            if qaMode == 0:
                if not os.path.isdir(dstPathTemp):
                    os.mkdir(dstPathTemp)

            run_unit_test(headerPath, dataPath, dstPathTemp, layout, case, numRuns, testType, qaMode, batchSize)
else:
    for case in caseList:
        if case not in supportedCaseList:
            continue
        for layout in range(3):
            dstPathTemp, logFileLayout = process_layout(layout, qaMode, case, dstPath, "host", func_group_finder)
            run_performance_test(loggingFolder, logFileLayout, headerPath, dataPath, dstPathTemp, layout, case, numRuns, testType, qaMode, batchSize)

# print the results of qa tests
nonQACaseList = [] # Add cases present in supportedCaseList, but without QA support

if qaMode and testType == 0:
    qaFilePath = os.path.join(outFilePath, "QA_results.txt")
    checkFile = os.path.isfile(qaFilePath)
    if checkFile:
        print_qa_tests_summary(qaFilePath, supportedCaseList, nonQACaseList)

layoutDict = {0:"PKD3", 1:"PLN3", 2:"PLN1"}
if (testType == 0 and qaMode == 0):   # Unit tests
    create_layout_directories(dstPath, layoutDict)
elif (testType == 1):   # Performance tests
    log_file_list = get_log_file_list()

    functionality_group_list = [
        "arithmetic_operations",
        "geometric_augmentations",
    ]

    for log_file in log_file_list:
        print_performance_tests_summary(log_file, functionality_group_list, numRuns)
