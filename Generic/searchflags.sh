#!/bin/sh
#https://github.com/rebane2001/rc-tools
#Needs a rewrite but works good enough for now
if [ ! "$#" -eq 3 ]
then
	echo "Search flags by Rebane";
	echo "Supresses errors by default, case insensitive, recursive";
	echo "Usage: $0 suffix minlen maxlen directory";
	echo "Example: '$0 IceCTF 4 128' to search for IceCTF{example_flag} .";
	exit 0;
fi
echo '\033[0;34mGrep:\033[0;0m'
grep --color=always	 -rain $1{.\\{$2\,$3\\}} $4 2>/dev/null
echo '\033[0;34mStrings:\033[0;0m'
find $4 -type f -exec strings {} \; | tail -n +1 | grep --color=always -ain $1{.\\{$2\,$3\\}} 2>/dev/null
echo '\033[0;34mGrep hex:\033[0;0m'
grep --color=always	 -rain $(echo -n $1 | xxd -pu -c 1000000 | tr -d '0a')7B.\\{$2\,$3\\}.\\{0\,$3\\}7D $4 2>/dev/null
echo '\033[0;34mStrings hex:\033[0;0m'
find $4 -type f -exec strings {} \; | tail -n +1 | grep --color=always -ain $(echo -n $1 | xxd -pu -c 1000000 | tr -d '0a')7B.\\{$2\,$3\\}.\\{0\,$3\\}7D 2>/dev/null
echo '\033[0;34m(b64 should be here but I havent implemented yet):\033[0;0m'
#find . -type f -exec command_here {} \;