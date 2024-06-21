#!/usr/bin/python3

#Installing Redis server

import os
import sys
import subprocess
from datetime import datetime
import tarfile

# Only allow root user to execute the script.
if os.geteuid()==0:
  print('Allowed to execute.')
else:
  print('Access denied. Execute as Sudoer.')

#defining functions
#Download Redis
def download_redis():
 redis_url="http://download.redis.io/releases/redis-4.0.9.tar.gz"
 subprocess.run(["wget", redis_url])
 print('Downloaded successfully!!!')

#Extract Redis
def extract_redis():
 subprocess.run(["tar", "xvzf", "redis-4.0.9.tar.gz"])
 print('Extracted successfully!!!')

#Compile Redis
def compile_redis():
  os.chdir("redis-4.0.9")
  subprocess.run(["make"])
  print('Compiled successfully!!!')

#Install redis
def install_redis(): 
  os.chdir("redis-4.0.9") 
  subprocess.run(["make", "install"])
  print('Installation Done...') 

#Run redis
def run_redis():
  subprocess.run(["redis-server"])
  print('Redis running successfully!!!')

#Check status of Redis server.
def status_redis():
    subprocess.run(["sudo", "service", "redis-server", "status"])
    print("Redis server status checked successfully!...")

#Starting Redis Server
def start_redis():
  subprocess.run(["sudo","service", "redis-server", "start"])
  print('Redis Server Started!!!')

#Backup the files of Redis Server
def backup_redis():
    print("Backing up Redis database...")
    # Define backup directory and file names
    backup_dir = "/home/vagrant/REDIS_BACKUP_JUN13"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"redis_bkp_jun14{timestamp}.rdb"
    tar_file = f"redis_backup_jun14{timestamp}.tar.gz"

    # Run the Redis save or bgsave command to create an RDB file
    method = input("Choose backup method ('save' or 'bgsave'): ").strip().lower()
    if method == "save":
        try:
            subprocess.run(["redis-cli", "SAVE"], check=True)
            print("Backup created using the SAVE command.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the SAVE command: {e}")
            return
    elif method == "bgsave":
        try:
            subprocess.run(["redis-cli", "BGSAVE"], check=True)
            print("Backup created using the BGSAVE command.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the BGSAVE command: {e}")
            return
    else:
        print("Invalid backup method. Choose 'save' or 'bgsave'.")
        return

    # Copy the RDB file to the backup directory
    try:
        redis_data_dir = "/var/lib/redis"  # Adjust this path as needed
        original_rdb_path = os.path.join(redis_data_dir, "dump.rdb")
        backup_rdb_path = os.path.join(backup_dir, backup_file)
        subprocess.run(["sudo", "cp", original_rdb_path, backup_rdb_path], check=True)
        print("RDB file copied successfully....")

        # Create a tar.gz file from the RDB file
        with tarfile.open(os.path.join(backup_dir, tar_file), "w:gz") as tar:
            tar.add(backup_rdb_path, arcname=backup_file)

        #Optionally remove the original RDB file from the backup directory
        os.remove(backup_rdb_path)
        print(f"Removed temporary backup file {backup_rdb_path}")

        print(f"Backup created and saved successfully as {tar_file}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while copying the RDB file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print('Redis backup is completed')

#Stopping Redis Server
def stop_redis():
 subprocess.run(["sudo", "service", "redis-server", "stop"])
 print('Redis Server Stopped!!!') 
# Checking Status of Redis Server
def status_redis():
 subprocess.run(["systemctl", "status", "redis.service"])
 print('Status executed...')

if sys.argv[1]=='download':
  download_redis()
elif sys.argv[1]=='extract':
  extract_redis() 
elif sys.argv[1]=='compile':
  compile_redis()
elif sys.argv[1]=='run':
  run_redis()
elif sys.argv[1]=='install':
  install_redis()
elif sys.argv[1]=='start':
  start_redis()
elif sys.argv[1]=='status':
  status_redis()
elif sys.argv[1]=='backup':
  backup_redis()
elif sys.argv[1]=='stop':
  stop_redis()
else:
  print('Help: ./redis.py {download|extract|compile|install|start|status|stop|backup}')