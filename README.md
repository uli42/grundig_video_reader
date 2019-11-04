Read the archived titles from a Grundig video recorder with Archive
System as sold at the beginning of the 1990s, such as the GV250VPT.

Extract the eeprom from the device and read it using some eeprom
reader. Then name the resulting 32kB binary as "binary.bin" and run
this little python program to dump the archive contents.

It will print a list of all recordings will be line by line. You can
sort the output by tape number and start position like this:
readeeprom.py | sort -k1,1 -k4.1,4.2 -k4.4,4.5

Output format:

AAA BBBBBB CCCC DD:DD-EE:EE (FF:FF) GG.GG.GGGG HHHHHHHHHHHHHHHHHHHHHHHHHH 

* A cassette number
* B tape length in minutes
* C category of the recording
* D start position on the tape as hm:mm
* E end position on the tape as hm:mm
* F recording duration as hh:mm
* G date of the recording
* H title of the recording

Example: 
017 245min Komöd. 0xf5 00:21-00:34 (00:13) 30.11.1995 Mutter und Sohn
