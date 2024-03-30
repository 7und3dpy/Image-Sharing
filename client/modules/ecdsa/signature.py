from .utils import *
from .utils.der import parse, encodeConstructed, encodePrimitive, DerFieldType
from .utils.binary import hexFromByteString, byteStringFromHex, base64FromByteString, byteStringFromBase64
from .utils.compatibility import *

class Signature: 

    def __init__(self, r, s, recoveryId = None): 
        self.r = r
        self.s = s
        self.recoveryID = recoveryId

    def _fromString(self, string, recoveryID = None): 
        r, s = parse(string)[0]
        return Signature(r, s, recoveryID)
    
    def _toString(self):
        return encodeConstructed(
            encodePrimitive(DerFieldType.integer, self.r), 
            encodePrimitive(DerFieldType.integer, self.s)
        ) 
    
    def fromDer(self, string, recoveryByte = False): 
        recoveryId = None
        if recoveryByte: 
            recoveryId = string[0] if isinstance(string[0], int) else ord(string)
            recoveryId -= 27
            string = string[1:]

        hexadecimal = hexFromByteString(string)
        return self._fromString(hexadecimal, recoveryId)
    
    def toDer(self, withRecoveryID = False): 
        hexadecimal = self._toString()
        encodedSequence = byteStringFromHex(hexadecimal)
        if not withRecoveryID:
            return encodedSequence
        return toBytes(chr(27 + self.recoveryID)) + encodedSequence
    
    def fromBase64(self, string, recoveryByte = False): 
        der = byteStringFromBase64(string)
        return self.fromDer(der, recoveryByte)
    
    def toBase64(self, withRecoveryId = False): 
        return base64FromByteString(self.toDer(withRecoveryId))