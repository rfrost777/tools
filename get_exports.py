###########################################################################################
# Write the original exports table of a WINDOWS DLL
# to a file. Useful for PrivEsc with proxy DLL's,
# e.g. abuse vulnerable software.
#
# Usage: python3 get_exports.py --target <NAME>.dll --originalPath 'C:\Windows\System32\<NAME>.dll' > proxy.def
# then cross-compile your proxy-dll like this:
#
#   x86_64-w64-mingw32-gcc -m64 -c -Os proxy.c -Wall -shared -masm=intel
#   x86_64-w64-mingw32-gcc -shared -m64 -def proxy.def proxy.o -o proxy.dll
#
# Credit:   Taken and modified from Cobalt-Strike git repo:
#           https://github.com/Cobalt-Strike/ProxyDLLExample/blob/main/get_exports.py
###########################################################################################
import pefile
import argparse

parser = argparse.ArgumentParser(description='Write exports of a target DLL to a file.')
parser.add_argument('--target', required=True, type=str, help='Target WINDOWS DLL.')
parser.add_argument('--originalPath', required=True, type=str, help='Original (Windows) DLL path.')

args = parser.parse_args()

target = args.target
original_path = args.originalPath.replace('\\','/')

dll = pefile.PE(target)

print("EXPORTS", end="\r\n")

for export in dll.DIRECTORY_ENTRY_EXPORT.symbols:
    if export.name:
        print(f"    {export.name.decode()}={original_path}.{export.name.decode()} @{export.ordinal}", end="\r\n")
