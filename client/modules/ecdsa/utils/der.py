from datetime import datetime
from .oid import oidToHex, oidFromHex
from .binary import hexFromInt, intFromHex, byteStringFromHex, bitsFromHex

class DerFieldType: 

    integer = "integer"
    bitString = "bitString"
    octetString = "octetString"
    null = "null"
    object = "object"
    printableString = "printableString"
    utcTime = "utcTime"
    sequence = "sequence"
    set = "set"
    oidContainer = "oidContainer"
    publicKeyPointContainer = "publicKeyPointContainer"

hexTagToType = {
    "02": DerFieldType.integer, 
    "03": DerFieldType.bitString, 
    "04": DerFieldType.octetString, 
    "05": DerFieldType.null, 
    "06": DerFieldType.object, 
    "07": DerFieldType.printableString, 
    "08": DerFieldType.utcTime, 
    "09": DerFieldType.sequence, 
    "10": DerFieldType.set, 
    "11": DerFieldType.oidContainer, 
    "12": DerFieldType.publicKeyPointContainer
    }

typeToHexTag = {v: k for k, v in hexTagToType.items()}

def parse(hexadecimal): 
    if not hexadecimal: 
        return []
    typeByte, hexadecimal = hexadecimal[:2], hexadecimal[2:]
    length, lengthBytes = readLengthBytes(hexadecimal)
    content, hexadecimal = hexadecimal[lengthBytes: lengthBytes + length], hexadecimal[lengthBytes + length:]
    if len(content) < length:
        raise Exception("Missing bytes in DER parse")
    
    tagData = getTagData(typeByte)
    if tagData["isConstructed"]: 
        content = parse(content)

    valueParser = {
        DerFieldType.null: parseNull, 
        DerFieldType.object: parseOid, 
        DerFieldType.utcTime: parseTime, 
        DerFieldType.integer: parseInteger, 
        DerFieldType.printableString: parseString,
    }.get(tagData["type"], parseAny)
    return [valueParser(content)] + parse(hexadecimal)

def parseAny(hexadecimal): 
    return hexadecimal

def parseOid(hexadecimal): 
    return tuple(oidFromHex(hexadecimal))

def parseString(hexadecimal): 
    return byteStringFromHex(hexadecimal).decode

def parseTime(hexadecimal): 
    string = parseString(hexadecimal)
    return datetime.strptime(string, "%y%m%d%H%M%SZ")

def parseNull(content):
    return None

def parseInteger(hexadecimal): 
    integer = intFromHex(hexadecimal)
    bits = bitsFromHex(hexadecimal[0])
    if bits[0] == "0": # negative numbers are encoded using two's complement
        return integer
    bitCount = 4 * len(hexadecimal)

    return integer - (2 ** bitCount)

def encodedInteger(num): 
    hexadecimal = hexFromInt(abs(num))
    if num < 0: 
        bitCount = 4 * len(hexadecimal)
        twosComplement = (2 ** bitCount) + num
        return hexFromInt(twosComplement)
    
    bits = bitsFromHex(hexadecimal[0])
    if bits[0] == "1": # if first bit was left as 1, number would be parsed as a negative integer with two's complement
        hexadecimal = "00" + hexadecimal
    return hexadecimal

def readLengthBytes(hexadecimal): 
    lengthBytes = 2
    lengthIndicator = intFromHex(hexadecimal[0:lengthBytes])
    isShortForm = lengthIndicator < 128 # checks if first bit of byte is 1 (a.k.a. short-form)
    if isShortForm: 
        length = lengthIndicator * 2
        return length, lengthBytes
    
    lengthLength = lengthIndicator - 128 # nullifies first bit of byte (only used as long-form flag)
    if lengthLength == 0: 
        raise Exception("Indefinite length encoding located in DER")
    lengthBytes += 2 * lengthLength
    length = intFromHex(hexadecimal[2:lengthBytes]) * 2
    return length, lengthBytes

def generateLengthBytes(hexadecimal): 
    size =  len(hexadecimal) // 2
    length = hexFromInt(size)
    if size < 128: # checks if first bit of byte should be 0 (a.k.a. short-form flag)
        return length.zfill(2)
    lengthLength = 128 + len(length) // 2 # +128 sets the first bit of the bytes as 1 (a.k.a. long-form flag)
    return hexFromInt(lengthLength) + length

def getTagData(tag): 
    bits = bitsFromHex(tag)
    bit8, bit7, bit6 = bits[:3]

    tagClass = {
        "0": {
            "0": "universal", 
            "1": "application", 
        }, 
        "1": {
            "0": "context-specific", 
            "1": "private", 
        }, 
    }[bit8][bit7]
    isConstructed = bit6 == "1"

    return {
        "class": tagClass, 
        "isConstructed": isConstructed, 
        "type": hexTagToType.get(tag)
    }


def encodedPrimitive(tagType, value): 
    if tagType == DerFieldType.integer: 
        value = encodedInteger(value)
    if tagType == DerFieldType.object: 
        value = oidToHex(value)
    return "{tag}{size}{value}".format(typeToHexTag[tagType], generateLengthBytes(value), value)

def encodeConstructed(encodedValues): 
    return encodePrimitive(DerFieldType.sequence, "".join(encodedValues))