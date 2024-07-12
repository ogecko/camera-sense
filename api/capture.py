import subprocess
import time
import os
import argparse
from datetime import datetime, timedelta

# Set up the argument parser
parser = argparse.ArgumentParser(description='Take pictures at regular intervals.')
parser.add_argument('-d', '--directory', type=str, default='.', help='Directory to store the pictures')
parser.add_argument('-f', '--filename', type=str, required=True, help='Filename prefix')
parser.add_argument('-t', '--time', type=int, default=60, help='Total duration to run in minutes')
parser.add_argument('-i', '--interval', type=float, default=1, help='Interval between photos in minutes')

# Parse the command line arguments
args = parser.parse_args()

# Function to take a picture with libcamera-still
def take_picture(filename):
    command = f"libcamera-still -v 0 -o {filename}"
    try:
        subprocess.run(command.split(), check=True)
        # Log the timestamp and filename
        print(f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} Picture {filename} taken successfully.")
    except subprocess.CalledProcessError as e:
        print(f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} An error occurred while taking {filename}: {e.stderr.decode()}")

# Calculate the next minute mark for the first picture
next_minute = (datetime.now() + timedelta(minutes=args.interval)) #.replace(second=0, microsecond=0)

# Ensure the directory exists
if not os.path.exists(args.directory):
    os.makedirs(args.directory)
    
# Loop to take a picture at the start of every interval for the specified total time
for i in range(int(args.time / args.interval)):
    filename = os.path.join(args.directory, f"{args.filename}_{datetime.now().strftime('%Y-%m-%d_%Hh%M')}_{i+1:05d}.jpg")
    take_picture(filename)
    
    # Wait until the next interval
    while datetime.now() < next_minute:
        time.sleep(1)
    next_minute += timedelta(minutes=args.interval)

print("Finished taking pictures.")