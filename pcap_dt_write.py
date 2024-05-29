import argparse
import os
import subprocess
import sys
import time
from datetime import datetime

FILEEXTS = ["pcap", "pcapng"]
EDITCAP = subprocess.getoutput("which editcap")
TSHARK = subprocess.getoutput("which tshark")
CURRENTTIME = int(time.time())

def show_help():
    print("\nUsage: {} pcapfile(s)".format(os.path.basename(sys.argv[0])))
    print("\nExamples:")
    print("{} /demofiles/sample.pcapng".format(os.path.basename(sys.argv[0])))
    print("{} /demofiles/pcap1.pcap /demofiles/*.pcapng".format(os.path.basename(sys.argv[0])))
    print()

def process_files(files, timestamp):
    if not EDITCAP or not TSHARK:
        print("Required tools not found (Wireshark not installed?)")
        return

    fnotfound = 0
    fsubmitted = 0
    fignored = 0

    for pcapfile in files:
        if os.path.isfile(pcapfile):
            filename = os.path.basename(pcapfile)
            fileext = filename.split('.')[-1]
            if fileext in FILEEXTS:
                fsubmitted += 1
                result = subprocess.getoutput(f"{TSHARK} -r {pcapfile} -T fields -e frame.time_epoch 2>/dev/null | head -1")
                pcaptime = int(result.split('.')[0]) if result else 0
                formatted_new_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %T")
                print(f"Changing first timestamp on {pcapfile} to {formatted_new_time}")

                delta_time = timestamp - pcaptime
                temp_file = f"{pcapfile}_{CURRENTTIME}.tmp"
                editcap_command = f"{EDITCAP} -t {delta_time} {pcapfile} {temp_file} && mv -f {temp_file} {pcapfile}"
                subprocess.call(editcap_command, shell=True)
            else:
                fignored += 1
                print(f"\"{pcapfile}\" does not seem to be a capture file.")
        else:
            print(f"{os.path.basename(pcapfile)}: file not found")
            fnotfound += 1

    print(f"Pcap files edited: {fsubmitted} ; other files (ignored): {fignored} ; input files not found: {fnotfound}")

def main():
    parser = argparse.ArgumentParser(description="Process pcap files.")
    parser.add_argument('files', nargs='*', help='Pcap files to process')
    parser.add_argument('-t', type=int, help='Timestamp to use', default=CURRENTTIME)

    args = parser.parse_args()

    if not args.files:
        show_help()
        sys.exit(1)

    timestamp = args.t if isinstance(args.t, int) else CURRENTTIME
    process_files(args.files, timestamp)

if __name__ == "__main__":
    main()
