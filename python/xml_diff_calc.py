import xml.etree.ElementTree as ET
import argparse
from pathlib import Path


def calc_diff(old_file_path, new_file_path, args):
    old_interfaces = map_interface_data(ET.parse(old_file_path).findall('devices/interface'))
    new_interfaces = map_interface_data(ET.parse(new_file_path).findall('devices/interface'))
    if args.verbose:
        print("Old:", old_interfaces, "\nNew:", new_interfaces)

    for k, v in old_interfaces.items():
        if new_interfaces[k] != v:
            print("Interface", k, "mac address has changed to", new_interfaces[k], "from", v)


def map_interface_data(interfaces):
    interfaces_map = {}
    for interface in interfaces:
        interfaces_map[interface.find('alias').get('name')] = interface.find('mac').get('address')

    return interfaces_map


def run():
    args = setup()
    try:
        old_file_path = Path(args.old_file).resolve(strict=True)
        new_file_path = Path(args.vm_file).resolve(strict=True)
    except FileNotFoundError:
        print("File's doesn't exists")
    else:
        calc_diff(old_file_path, new_file_path, args)


def setup():
    parser = argparse.ArgumentParser("XML Diff calculator")
    parser.add_argument('old_file', help='Xml file path of old xml')
    parser.add_argument('vm_file', help='New xml file from VM')
    parser.add_argument("-v", "--verbose", help="prints more info", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    run()
