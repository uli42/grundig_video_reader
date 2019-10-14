Read the archived titles from a Grundig video recorder with Archive
System as sold at the beginning of the 1990s, such as the GV250VPT.

Extract the eeprom from the device and read it externally. Then name
the resulting 32kB binary as "binary.bin" and run this little python
program to dump the archive contents.

It will print a list of 15 stored recording categories. Following that
a list of all recordings will be printed line by line. Line format:

AAA BBBBBB CCCC DD:DD-EE:EE FF.FF.FFFF GGGGGGGGGGGGGGGGGGGGGGGGGG 

* A cassette number
* B category of the recording
* C unknown flag, maybe marking longplay recordings
* D start position on the tape as hm:mm
* E end position on the tape as hm:mm
* F date of the recording
* G title of the recording

Example: 
017 Komöd. 0xf5 00:21-00:34 30.11.1995 Mutter und Sohn
