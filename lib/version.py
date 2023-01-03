#!/usr/bin/env python3

def ver_info(version_info):
    revision_number = '.'.join(str(c) for c in version_info)
    version = 'ver. '+revision_number
    return version

if (__name__ == '__main__'):
    vers=(0, 0)
    print(ver_info(vers))
    