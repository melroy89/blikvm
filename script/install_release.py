# eg: python3 install_release.py --releasepath release
# after run this script, need reboot.
import subprocess
import os
import re
import argparse

gArgs = None
def doArgParse():
    global gArgs
    optParser = argparse.ArgumentParser(description='build and tar file')
    optParser.add_argument('--releasepath', nargs='?', default='/tmp/kvm_update/release/', type=str, help='release path')
    gArgs = optParser.parse_args()

def execute_cmd(cmd,sh_path):
    try: 
        output = subprocess.check_output(cmd, shell = True, cwd=sh_path )
        if len(output) > 5 :
            tmp = ' '.join(output.decode('utf-8').split())
            pid = tmp.split(' ')[1]
            cmd = "kill " + pid
            output = subprocess.check_output(cmd, shell = True, cwd=sh_path )
    except subprocess.CalledProcessError as e:
        out_bytes = e.output.decode()
        code = e.returncode
        print("error code:",code, out_bytes)

def main():
    global gArgs
    doArgParse()
    sh_path = os.path.split(os.path.realpath(__file__))[0]
    # kill run pthread
    
    # kill kvmd-main
    cmd = "ps -aux | grep kvmd-main | grep -v grep"
    execute_cmd(cmd,sh_path)
    print('kill main done')

    # kill kvmd-web
    cmd = "ps -aux | grep kvmd-web | grep -v grep"
    execute_cmd(cmd,sh_path)
    print('kill web done')

    # kill kvmd-ustreamer
    cmd = "ps -aux | grep ustreamer | grep -v grep"
    execute_cmd(cmd,sh_path)
    print('kill ustreamer done')

    # install all software
    if os.path.exists(gArgs.releasepath):
        cmd = "mount -o remount,rw / && mount -o remount,rw /boot && bash install-kvmd-main.sh && bash install-ustreamer.sh && bash install-kvmd-hid.sh \
        && bash install-kvmd-web.sh && bash install-kvmd-msd.sh && cp package.json /usr/bin/blikvm/package.json &&  mount -o remount,ro / && mount -o remount,ro /boot"
        subprocess.check_output(cmd, shell = True, cwd=gArgs.releasepath )
        # cmd = "cp package.json /usr/bin/kvm_json/package.json"
        # subprocess.check_output(cmd, shell = True, cwd=gArgs.releasepath )
        # cmd = "reboot"
        # subprocess.check_output(cmd, shell = True, cwd=gArgs.releasepath )
    else:
        print(gArgs.releasepath, ' not exit')

if __name__ == '__main__':
    main()
