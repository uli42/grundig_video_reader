A little tool to read the archived titles from a Grundig video
recorder with Archive System as sold at the beginning of the 1990s,
such as the GV250VPT.

These systems were able to store the tape contents for recordings on
an EEPROM chip. Every tape you were using was marked and could be
recognized by the recorder when it was re-inserted. Every recording
was stored on the EEPROM with tape number, tape position, duration,
recording date and title. When using this system you did not have to
write down what was stored on your tapes but could look it up directly
on the recorder and make the recorder comfortably position the tape
right at the beginning of the desired title. You could also identify
free slots for new recordings.

By dumping the EEPROM content you can restore this information even
after your recorder was asleep in the attic for many years. With the
help of this tool you can create a nice list with all information
contained in the EEPROM dump.

How to use:

Extract the EEPROM from the device and read it using some EEPROM
reader. Then rename the resulting 32kB binary to `binary.bin` and run
`readeeprom.py` to dump the archive contents.

It will print a list of all recordings line by line. You can
sort the output by tape number and start position like this:
`readeeprom.py | sort -k1,1 -k4.1,4.2 -k4.4,4.5`

Output format:

```
AAA BBBBBB CCCC DD:DD-EE:EE (FF:FF) GG.GG.GGGG HHHHHHHHHHHHHHHHHHHHHHHHHH 
```

  * A cassette number
  * B tape length in minutes
  * C category of the recording
  * D start position on the tape as hm:mm
  * E end position on the tape as hm:mm
  * F recording duration as hh:mm
  * G date of the recording
  * H title of the recording

Example output line:
```
017 245min Komöd. 0xf5 00:21-00:34 (00:13) 30.11.1995 Mutter und Sohn
```