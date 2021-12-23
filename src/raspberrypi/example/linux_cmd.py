import subprocess  
  
def ping(servers):
    
    # The command you want to execute   
    cmd = 'ping'
  
    # send one packet of data to the host 
    # this is specified by '-c 1' in the argument list 
    outputlist = []
    # Iterate over all the servers in the list and ping each server
    for server in servers:
        temp = subprocess.Popen([cmd, '-c 1', server], stdout = subprocess.PIPE) 
        # get the output as a string
        output = str(temp.communicate()) 
    # store the output in the list
        outputlist.append(output)
    return outputlist
  
def snap_libcamera_pi():
    cmd = ["libcamera-still -o ~/Documents/hawkeye/src/raspberrypi/example/test.jpg"]
    subprocess.run(cmd, shell=True)

def clean_snap():
    cmd = ["rm ~/Documents/hawkeye/src/raspberrypi/example/test.jpg"]
    subprocess.run(cmd, shell=True)

if __name__ == '__main__': 
    
    snap_libcamera_pi()