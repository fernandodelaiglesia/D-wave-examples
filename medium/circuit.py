# AWS import Boto3
import boto3

import os

# Each device is loacated in a specific region. us-west-1 is where Rigetti device is located
os.environ['AWS_DEFAULT_REGION'] = "us-east-1"

# AWS imports: Import Braket SDK modules
from braket.circuits import Circuit
from braket.aws import AwsDevice

# When running in real QPU you must enter the S3 bucket you created during onboarding to Braket in the code as follows
my_bucket = f"amazon-braket-your-bucket" # the name of the bucket
my_folder = "YourFolder" # the name of the folder in the bucket
s3_folder = (my_bucket, my_folder)

# set up device
device = AwsDevice("arn:aws:braket:::device/qpu/ionq/ionQdevice")
# device = AwsDevice("arn:aws:braket:::device/qpu/rigetti/Aspen-8")
# Instantiate the local simulator
#from braket.devices import LocalSimulator
#device = LocalSimulator()
execution_windows = device.properties.service.executionWindows
print(f'{device.name} availability windows are:\n{execution_windows}\n')

# Create the Teleportation Circuit
circ = Circuit()

# Put the qubit to teleport in a superposition state
circ.h(0)

# Create the entangled state (qubit 1 reamins in Alice while qubit 2 is sent to Bob)
circ.h(1).cnot(1, 2)

# Teleportation algorithm
circ.cnot(0, 1).h(0)

# Do the trick with deferred measurement

circ.h(2).cnot(0, 2).h(2)     # Control Z 0 -> 2 (developed because IonQ is not having native Ctrl-Z)
circ.cnot(1, 2)               # Control X 1 -> 2

print(circ)

# run circuit
#result = device.run(circ, s3_folder, shots=100, poll_timeout_seconds=1*24*60*60)

result = device.run(circ, shots=100)

# get id and status of submitted task
result_id = result.id
result_status = result.state()

print('ID of task:', result_id)
print('Status of task:', result_status)

if result_status == "COMPLETED":
    # get measurement shots
    counts = result.result().measurement_counts
    # print counts
    print(counts)

