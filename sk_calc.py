#################################################################################
#
#   Calculate a SMB3 random Session Key from PCAP data to decrypt SMB3 trafic.
#   TryHackMe Room "BLOCK": https://tryhackme.com/r/room/blockroom
#
#   Idea stolen from Khris Tolbert: 
#   https://medium.com/maverislabs/decrypting-smb3-traffic-with-just-a-pcap-absolutely-maybe-712ed23ff6a2
#
#################################################################################
import hashlib
import hmac
import argparse
from Cryptodome.Cipher import ARC4
from Cryptodome.Cipher import DES
from Cryptodome.Hash import MD4

def generateEncryptedSessionKey(keyExchangeKey, exportedSessionKey):
   cipher = ARC4.new(keyExchangeKey)
   cipher_encrypt = cipher.encrypt

   sessionKey = cipher_encrypt(exportedSessionKey)
   return sessionKey

parser = argparse.ArgumentParser(description="Calculate the Random Session Key based on data from a PCAP.")
parser.add_argument("-u","--user",required=True,help="User name")
parser.add_argument("-d","--domain",required=True, help="Domain name")
parser.add_argument("-p","--password",required=True,help="Password of User")
parser.add_argument("-hsh","--hash",required=True,help="User's NTLM Hash")
parser.add_argument("-n","--ntproofstr",required=True,help="NTProofString. This can be found in PCAP (provide Hex Stream)")
parser.add_argument("-k","--key",required=True,help="Encrypted Session Key. This can be found in PCAP (provide Hex Stream)")
parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

args = parser.parse_args()
# Check if both --hash and --password are used...
if args.password and args.hash:
    print "The use of -hsh and -p are mutually exclusive ..."
    sys.exit(2)

# Upper Case User and Domain
user = str(args.user).upper().encode('utf-16le')
domain = str(args.domain).upper().encode('utf-16le')

# Create 'NTLM' Hash of password
if args.password:
    # Create 'NTLM' Hash of password
    passw = args.password.encode('utf-16le')
    hash1 = hashlib.new('md4', passw)
    password = hash1.digest()
else:
    # Directly use the provided NTLM Hash
    password = bytes.fromhex(args.hash)

# Calculate the ResponseNTKey
h = hmac.new(password, digestmod=hashlib.md5)
h.update(user+domain)
respNTKey = h.digest()

# Use NTProofSTR and ResponseNTKey to calculate Key Exchange Key
NTproofStr = bytes.fromhex(args.ntproofstr)
h = hmac.new(respNTKey, digestmod=hashlib.md5)
h.update(NTproofStr)
KeyExchKey = h.digest()

# Calculate the Random Session Key by decrypting Encrypted Session Key with Key Exchange Key via RC4
RsessKey = generateEncryptedSessionKey(KeyExchKey, bytes.fromhex(args.key))

if args.verbose:
    print("USER WORK: " + user.decode('utf-16le') + "" + domain.decode('utf-16le'))
    print("PASS HASH: " + password.hex())
    print("RESP NT:   " + respNTKey.hex())
    print("NT PROOF:  " + NTproofStr.hex())
    print("KeyExKey:  " + KeyExchKey.hex())
print("Random Session Key: " + RsessKey.hex())

