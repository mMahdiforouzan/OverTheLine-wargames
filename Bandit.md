
# The Bandit



To connect to level 0, enter. 

> `ssh -p 2220 bandit0@bandit.labs.overthewire.org` 

The password for this level is given   She `-p` flag is for choosing the port 2220.   bandit0 is the username and bandit.labs.overthewire.org is the IP.    Swap 0 with the level number in the username to connect to each level.
To disconnect from a level, you can just enter the command 

> `exit`


## level 0

Run command   

> `ls`

To seem the files in the directory.

> `cat readme`

To open the file containing the password for level 1.


## level 1

I like running the

> `ls`

command every time just to check what's in the directory.   I am gonna assume that's the first command for each level and not mention it anymore.

the only file is name `-` which is a special character. 

> `cat -` 

doesn't work so let's try something else.

> `cat "./-"`

works.  the  `./` prefix is saying we want the file named `-` in this file.    The double quotation marks are not necessary but it is good practice as we'll see in the next level.


## level 2

the only file is named --spaces in this filename--.    This is where the double quotation marks in the command comes in.

run

> `cat "./--spaces in this filename--"`


## level 3

this level introduces folders. to open the folder, run

> `cd inhere`

then type 

> `cat`

then press tab. pressing tab tries to autofill the rest of the command. This function helps us get the name of the file that's hidden.


## level 4

In this level, the inhere folder has many files inside.   From the website we know the one containing the password is human-readable.

go to the inhere folder and enter the command 

> `file ./*`

This will give us a list of the type of everything in this directory.   The password is in the file of type ASCII text.


## level 5

we're looking for one specific file in a sea of files and folders.    We can just stay in the original starting directory and use the 

> `find`

command to search for our file.   This file has the following specifications. (I added the find command arguments for each as an indented line)

1. human-readable
    - `-type f`
2. 1033 bytes in size
    - `-size 1033c`
3.  not executable
    - `! -executable`

the command 

> `find -type f -size 1033c ! -executable`

gives us the file name.

we can pipeline the name and feed it directly to the cat command using the following line.

> `find -type f -size 1033c ! -executable | xargs cat`

another option is

> ``cat `find -type f -size 1033c ! -executable` ``

## level 6

This time the file we're looking for can be anywhere on the server.   run the following command to go to the root directory

> `cd /`

Now we can use `find` like the last level to  look for our file.    this time the requirements are different.

1. owned by user bandit7
    - -user bandit7
2. owned by group bandit6
    - -group bandit6
3. 33 bytes 
    - -size 33c

the command 

>  `find -user bandit7 -group bandit6 -size 33c`

should get us the file, but `find` gives us an error every time it encounters a file we don't have permissions for.   We fix that by adding a new argument.

> `2>/dev/null`

This redirects all the errors to `/dev/null/` which gets deleted by the system.

to get the password, run the command bellow.

>`find -user bandit7 -group bandit6 -size 33c 2>/dev/null | xargs cat`

### Note

We can used the `grep` command to filter out the Permission denied errors as well.

> `find -user bandit7 -group bandit6 -size 33c -print 2>&1 | grep -v "Permission denied"` 

This gets rid of the Permission denied errors while keeping the other errors which can be helpful.



## level 7

This level is just a simple introduction to `grep`. 

> `grep millionth data.txt`

will give us the password.


## level 8

In this level we need to find a unique line in our text file.    for this we need to use two new commands `sort` and `uniq`.    

the following command gives us the password.

> `sort data.txt | uniq -u`

As the name implies, `sort` sorts the file which helps `uniq` remove the duplicate lines. the `-u` flag makes it so `uniq` only outputs the unique lines.


## level 9

In this level the `data.txt` file contains some readable strings but mostly random binary data.   The password is in a line that starts with multiple equal signs `=`.

Since we need to get only the readable strings out of the file, we use the `strings` command then `grep` to filter out the lines with multiple `=`s.

> `strings data.txt | grep ==`


## level 10

The new text file contains data encoded in base64. We will need to use decoder flag `-d` in the command `base64`.

all we need is the command below.

> `base64 -d data.txt`


## level 11

This challenge brings a new command `tr` which is used to translate from an array of characters to another.     Since we're doing ROT13, we need to map `a-z` to `n-za-m` and the same for capital letters.

The command

> `cat data.txt | tr 'N-ZA-Mn-za-m' 'A-Za-z'`

gives us the password.


## level 12

This exercise is a bit more complicated. first we need to make a temporary directory so we can make as many files as we want without worrying about permissions.

> `mktemp -d`

will make us a temporary directory. the `-d` flag is for directory. What we get is like `/tmp/tmp.XXXXXXXXXX` where the Xs are random values.

Now let's copy the `data.txt` we have to our new directory.

> `cp data.txt /tmp/tmp.XXXXXXXXXX`

then just go to the directory using

> `cd /tmp/tmp.XXXXXXXXXX`

Looking at the file with 

> `cat data.txt` 

or 

> `xxd data.txt`

we notice the file is actually a hexdump.

We can reverse that using `xxd`

> `xxd -r data.txt compressed`

now we can begin extracting data from the file.    First, we need to read the hexdump of the file and decompress it using the right tool.

run

> `xxd compressed` 

to see the hexdump. We see the number of the line followed by a file signature and some data.    For example, `00000000:` is the line and `1f 8b` is the signature for a `gzip`

1. `1f 8b`
    - `.gz` for GZIP
2. `42 5a 68`
    - `.bz2` bzip2
3. if the file contains a `.bin` file
    - `.tar`


Before each extraction stage, we just need to check the file signature and use `mv` to rename the `compressed` file.

1. `1f 8b`
    - `mv compressed compressed.gz`
    - `gunzip compressed.gz`
2. `42 5a 68` 
    - `mv compressed compressed.bz2`
    - `bunzip2 compressed.bz2`
3. `1f 8b`
    - `mv compressed compressed.gz`
    - `gunzip compressed.gz`
4. `data5.bin`  
    - `mv compressed compressed.tar`
    - `tar -xf compressed.tar`
    - The new file is named `data5.bin`
5. `data6.bin`
    - `mv data5.bin compressed.tar`
    - `tar -xf compressed.tar`
    - The new file is `data6.bin`
6. `42 5a 68`
    - `rm compressed` gets rid of the `compressed` file from step 3
    - `mv data6.bin compressed.bz2`
    - `bunzip2 compressed.bz2`
7. `data8.bin`
    - `mv compressed compressed.tar`
    - `tar -xf compressed.tar`
    - The new file is `data8.bin`
8. `1f 8b`
    - `mv data8.bin compressed.gz`
    - `gunzip compressed.gz`
9. the file is no longer compressed
    - `cat compressed` 



## level 13

This level introduces SSH private keys and the `scp` command for securely transferring files.

first we need to transfer the `sshkey.private` to our device, which we will use to sign into `bandit14` and getting the password.

Run 

> `scp -P 2220 bandit13@bandit.labs.overthewire.org:* ./`

which will transfer the private key to our device.      Next we need to make sure the file has the right permissions.

> `ls -l`

shows us the permissions for each file.    we only want the owner to have permissions so read so we can change that using

> `chmod 700 sshkey.private`

now we can sign in to `bandit14` using the private key.

>`ssh -i sshkey.private -p 2220 bandit14@bandit.labs.overthewire.org`

The last step is to actually get this level's password, though that isn't necessary since we can just connect to this user using the ssh private key, we will need it for the next level.   we know it is stored in `/etc/bandit_pass/bandit14` from the website so a simple `cat` command should do it.

>`cat /etc/bandit_pass/bandit14`

## level 14

Now we need to send the password for this level to the localhost's port 30000. we can do this using the `nc` command which requires just the hostname and the port we wanna connect to.   We can send the password to that port using pipelining.

> `cat /etc/bandit_pass/bandit14 | nc localhost 30000`


## level 15

This level is the same idea as the last level but this time we need to use SSL/TLS encryption and send the password to port 30001.      To encrypt our message we need to use `ncat` instead of the `nc` command and we need the `--ssl` argument.

The following command should get us the password. 

>`cat /etc/bandit_pass/bandit15 | ncat --ssl localhost 30001`

