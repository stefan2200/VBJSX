import random
import re


# String obfuscation (easy & effective)
def string(input_string, ob_type="random"):
    if not ob_type:
        return '"%s"' % input_string.replace('"', '\\"')
    r = random.randint(0, 2)
    output = ''
    if r == 0 or ob_type == "hex":
        strb = b'%s' % input_string
        for char in strb:
            output += "\\x%s" % char.encode('hex')
        return '"%s"' % output

    if r == 1:
        shift = random.randint(1, 12)
        for char in input_string:
            output += " + String.fromCharCode(%d-%d) " % (ord(char) + shift, shift)

    if r == 2:
        shift = random.randint(1, 12)
        for char in input_string:
            output += " + String.fromCharCode(%d+%d) " % (ord(char) - shift, shift)

    return output.strip()[1:]


# The default string obfuscation techniques seem to trigger AV signatures, re-obfuscating
def posh_reobfus(input_string, obfus=False):
    for x in re.findall(r"\((['\"].+?['\"])\)", input_string):
        raw = x.replace("'", '').replace(' ', '').replace('+', '').replace('"', '')
        reobfuscated = string(raw, obfus)
        input_string = input_string.replace(x, reobfuscated)
    return input_string