#!python2
# -*- coding: utf-8 -*-

"""
   Read the archived titles from a Grundig video recorder with
   Archive System as sold at the beginning of the 1990s, such as the
   GV250VPT.
"""

import struct
import mmap

def convert(inputstr):
    """
    ETSI EN 300 706
    Teletext Lateinischer G0-Primaerzeichensatz – Deutsche Variante
    "#" 0x23  "$" 0x24  "§" 0x40  "^" 0x5E  "_" 0x5F  "°" 0x60
    Ä 0x5B  Ö 0x5C  Ü 0x5D
    ä 0x7B  ö 0x7C  ü 0x7D  ß 0x7E
    """

    inputstr = inputstr.replace("¤", "$")
    inputstr = inputstr.replace("@", "§")
    inputstr = inputstr.replace("[", "Ä")
    inputstr = inputstr.replace("\\", "Ö")
    inputstr = inputstr.replace("]", "Ü")
    inputstr = inputstr.replace("`", "°")
    inputstr = inputstr.replace("{", "ä")
    inputstr = inputstr.replace("|", "ö")
    inputstr = inputstr.replace("}", "ü")
    inputstr = inputstr.replace("~", "ß")
    return inputstr

def main(infilename):
    """
    read file infilename and dump the recordings found to stdout
    """

    infilehandle = open(infilename, 'r+b')
    # memory map input file
    infilemap = mmap.mmap(infilehandle.fileno(), 0)

    infilemap.seek(4678)
    catdata = infilemap.read(15*6)

    categories = []

    for i in range(15):
        categories.append(convert(struct.unpack_from('6s', catdata, i*6)[0]))

    recordings = infilemap.read(32768 - 4768 - 15*6)
    # 000012a0  b0 01 f5 01 38 02 38 44  65 72 20 52 6f 73 65 6e  |....8.8Der Rosen|
    # 000012b0  6b 72 69 65 67 20 20 20  20 20 20 20 20 20 20 20  |krieg           |
    # 000012c0  20 20 20 20 20 11 04 94                           |     ...|

    # 000012a0  b|0 01| f5| 01 38| 02 38| 44  65 72 20 52 6f 73 65 6e  |....8.8Der Rosen|
    # 000012b0  6b 72 69 65 67 20 20 20  20 20 20 20 20 20 20 20       |krieg           |
    # 000012c0  20 20 20 20 20| 11 04 94                               |     ...|

    # bei _einem_ EEPROM:
    # - 700 Titel mit 40 Zeichen
    # - 968Byte Timer-Puffer und Senderkennungen
    # - 700 dreistellige Badnnummern von 001 bis 999 möglich
    # - "Mit dem Eintragen eines Titels ins Archiv wird die
    #   Bandlänge (Cassettenspielzeit) der jweiligen
    #   Cassettenummer zugeordnet."

    for i in range(700):
        entry = struct.unpack_from('BBBBBBB30sBBB', recordings, i*40)
        if entry[0] == 255:
            break

        # first nibble: category index
        catidx = entry[0] / 16
        # nibbles 2-4: tape number
        tape = 100 * (entry[0] % 16) + 10 * (entry[1] / 16)  + entry[1] % 16

        # so far only two values seen: 0xf5 and 0xb9. Suspicion is
        # that this encodes if the recording is in longplay or
        # not. We are also missing the tape length...
        # 0xf5 = %1111 0101
        # 0Xb9 = %1011 1001
        flags = entry[2]

        # data is stored as "readable hex", 0x01 0x38 means start time "01:38"
        starthour = 10 * (entry[3] / 16) + entry[3] % 16
        startmin = 10 * (entry[4] / 16) + entry[4] % 16

        endhour = 10 * (entry[5] / 16) + entry[5] % 16
        endmin = 10 * (entry[6] / 16) + entry[6] % 16

        durationmins = (endhour - starthour) * 60 + endmin - startmin
        durationhours = durationmins / 60
        durationmins = durationmins % 60

        # 30 chars in teletext encoding
        title = convert(entry[7])

        # data is storead as "readable hex" again
        day = 10 * (entry[8] / 16)  + entry[8] % 16
        month = 10 * (entry[9] / 16)  + entry[9] % 16
        year = 1900 + 10 * (entry[10] / 16) + entry[10] % 16
        if year < 1970:
            year += 100

        print "%3.3d %s 0x%x %02.2d:%02.2d-%02.2d:%02.2d (%02.2d:%02.2d) %02.2d.%02.2d.%04.4d %s" % (
            tape, categories[catidx],
            flags, starthour, startmin,
            endhour, endmin,
            durationhours, durationmins,
            day, month, year,
            title)

    if infilemap:
        infilemap.close()
    if infilehandle:
        infilehandle.close()

main("binary.bin")
