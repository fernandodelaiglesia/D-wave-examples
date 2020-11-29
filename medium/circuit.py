# AWS import Boto3
import boto3

import os

# Each device is loacated in a specific region. us-west-1 is where Rigetti device is located
os.environ['AWS_DEFAULT_REGION'] = "us-west-1"

# AWS imports: Import Braket SDK modules
from braket.circuits import Circuit
from braket.aws import AwsDevice

# When running in real QPU you must enter the S3 bucket you created during onboarding to Braket in the code as follows
my_bucket = f"amazon-braket-Your-Bucket-Name" # the name of the bucket
my_folder = "Your-Folder-Name" # the name of the folder in the bucket
s3_folder = (my_bucket, my_folder)

# 

# Create the Teleportation Circuit
circ = Circuit()
## Set the state to teleport applying an unitary
import numpy as np
my_unitary = np.array([[np.sqrt(2)/np.sqrt(3) , 1/np.sqrt(2)],[1/np.sqrt(3), -np.sqrt(2)/np.sqrt(2)]])
circ.unitary(matrix=my_unitary, targets=[0])

# Create the entangled state
bell_state = circ.h(1).cnot(1, 2)

print(circ)
