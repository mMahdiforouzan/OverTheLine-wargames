
# The Bandit



To connect to level 0, enter.

> `ssh -p 2220 bandit0@bandit.labs.overthewire.org` 

The password for this level is given the `-p` flag is for choosing the port 2220.

`bandit0` is the username and bandit.labs.overthewire.org is the IP.

Swap 0 with the level number in the username to connect to each level.

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

Command every time just to check what's in the directory.

I am gonna assume that's the first command for each level and not mention it anymore.

The only file is name `-` which is a special character. 

> `cat -` 

Doesn't work so let's try something else.

> `cat "./-"`

Works.

The `./` prefix is saying we want the file named `-` in this file.

The double quotation marks are not necessary but it is good practice as we'll see in the next level.


## level 2

The only file is named --spaces in this filename--.

This is where the double quotation marks in the command comes in.

Run

> `cat "./--spaces in this filename--"`


## level 3

This level introduces folders. To open the folder, run

> `cd inhere`

Then type 

> `cat`

Then press tab. Pressing tab tries to autofill the rest of the command. This function helps us get the name of the file that's hidden.


## level 4

In this level, the inhere folder has many files inside.

From the website we know the one containing the password is human-readable.

Go to the inhere folder and enter the command 

> `file ./*`

This will give us a list of the type of everything in this directory.

The password is in the file of type ASCII text.


## level 5

We're looking for one specific file in a sea of files and folders.

We can just stay in the original starting directory and use the 

> `find`

Command to search for our file.

This file has the following specifications. (I added the find command arguments for each as an indented line)

1. Human-readable
    - `-type f`
2. 1033 bytes in size
    - `-size 1033c`
3.  Not executable
    - `! -executable`

The command 

> `find -type f -size 1033c ! -executable`

Gives us the file name.

We can pipeline the name and feed it directly to the cat command using the following line.

> `find -type f -size 1033c ! -executable | xargs cat`

Another option is

> ``cat `find -type f -size 1033c ! -executable` ``

## level 6

This time the file we're looking for can be anywhere on the server.

Run the following command to go to the root directory

> `cd /`

Now we can use `find` like the last level to look for our file.

This time the requirements are different.

1. Owned by user bandit7
    - -user bandit7
2. Owned by group bandit6
    - -group bandit6
3. 33 bytes 
    - -size 33c

The command 

> `find -user bandit7 -group bandit6 -size 33c`

Should get us the file, but `find` gives us an error every time it encounters a file we don't have permissions for.

We fix that by adding a new argument.

> `2>/dev/null`

This redirects all the errors to `/dev/null/` which gets deleted by the system.

To get the password, run the command bellow.

> `find -user bandit7 -group bandit6 -size 33c 2>/dev/null | xargs cat`

### Note

We can used the `grep` command to filter out the Permission denied errors as well.

> `find -user bandit7 -group bandit6 -size 33c -print 2>&1 | grep -v "Permission denied"` 

This gets rid of the Permission denied errors while keeping the other errors which can be helpful.



## level 7

This level is just a simple introduction to `grep`. 

> `grep millionth data.txt`

Will give us the password.


## level 8

In this level we need to find a unique line in our text file. For this we need to use two new commands `sort` and `uniq`.


The following command gives us the password.

> `sort data.txt | uniq -u`

As the name implies, `sort` sorts the file which helps `uniq` remove the duplicate lines. The `-u` flag makes it so `uniq` only outputs the unique lines.


## level 9

In this level the `data.txt` file contains some readable strings but mostly random binary data. The password is in a line that starts with multiple equal signs `=`. Since we need to get only the readable strings out of the file, we use the `strings` command then `grep` to filter out the lines with multiple `=`s.

> `strings data.txt | grep ==`


## level 10

The new text file contains data encoded in base64. We will need to use decoder flag `-d` in the command `base64`.

All we need is the command below.

> `base64 -d data.txt`


## level 11

This challenge brings a new command `tr` which is used to translate from an array of characters to another.

Since we're doing ROT13, we need to map `a-z` to `n-za-m` and the same for capital letters.

The command

> `cat data.txt | tr 'N-ZA-Mn-za-m' 'A-Za-z'`

Gives us the password.


## level 12

This exercise is a bit more complicated. First we need to make a temporary directory so we can make as many files as we want without worrying about permissions.

> `mktemp -d`

Will make us a temporary directory. The `-d` flag is for directory. What we get is like `/tmp/tmp.XXXXXXXXXX` where the Xs are random values.

Now let's copy the `data.txt` we have to our new directory.

> `cp data.txt /tmp/tmp.XXXXXXXXXX`

Then just go to the directory using

> `cd /tmp/tmp.XXXXXXXXXX`

Looking at the file with 

> `cat data.txt` 

Or 

> `xxd data.txt`

We notice the file is actually a hexdump.

We can reverse that using `xxd`

> `xxd -r data.txt compressed`

Now we can begin extracting data from the file.

First, we need to read the hexdump of the file and decompress it using the right tool.

Run

> `xxd compressed` 

To see the hexdump. We see the number of the line followed by a file signature and some data.

For example, `00000000:` is the line and `1f 8b` is the signature for a `gzip`

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

First we need to transfer the `sshkey.private` to our device, which we will use to sign into `bandit14` and getting the password.

Run 

> `scp -P 2220 bandit13@bandit.labs.overthewire.org:* ./`

Which will transfer the private key to our device.

Next we need to make sure the file has the right permissions.

> `ls -l`

Shows us the permissions for each file.

We only want the owner to have permissions so read so we can change that using

> `chmod 700 sshkey.private`

Now we can sign in to `bandit14` using the private key.

> `ssh -i sshkey.private -p 2220 bandit14@bandit.labs.overthewire.org`

The last step is to actually get this level's password, though that isn't necessary since we can just connect to this user using the ssh private key, we will need it for the next level.

We know it is stored in `/etc/bandit_pass/bandit14` from the website so a simple `cat` command should do it.

> `cat /etc/bandit_pass/bandit14`

## level 14

Now we need to send the password for this level to the localhost's port 30000. We can do this using the `nc` command which requires just the hostname and the port we wanna connect to.

We can send the password to that port using pipelining.

> `cat /etc/bandit_pass/bandit14 | nc localhost 30000`


## level 15

This level is the same idea as the last level but this time we need to use SSL/TLS encryption and send the password to port 30001.

To encrypt our message we need to use `ncat` instead of the `nc` command and we need the `--ssl` argument.

The following command should get us the password. 

> `cat /etc/bandit_pass/bandit15 | ncat --ssl localhost 30001`

## level 16

We need to find a port between 31000 and 32000 that has a server listening and the server speaks SSL/TLS.

We will use `nmap` to find which of the ports are open and listening, then we can use `openssl` with the `s_client` command and the `-connect` flag to check if the server is using TLS protocol.

> `nmap -p 31000-32000 localhost`

This will give us a list of ports that are listening.

Then we will use those port numbers one by one in the next step to see which one's are using the TLS protocol.

Note: more than one server in the list might be using the TLS protocol. Only one of them will return the password for the next level, the other ones will return what we send them.

> `openssl s_client -connect localhost:port`

Just replace `port` by the port number and try each one we got from `nmap`.

After finding a server that uses TLS, we can use the next command to see if it's the right one.

> `cat /etc/bandit_pass/bandit16 | ncat --ssl localhost port`

Again replace `port` with the port number. 

The right port for me was `31790` but that might change so try it for yourself.

> `cat /etc/bandit_pass/bandit16 | ncat --ssl localhost 31790`


We are given a RSA private key instead of just a password, we can just copy the whole thing but that will be tricky so let's just make a temporary directory for this file, then we can just transfer it to our device using what we did in level 13.

> `mktemp -d`

Copy the new directory and use `cd` to go there.

> `cat /etc/bandit_pass/bandit16 | ncat --ssl localhost 31790 > ./sshkey17.private`

Now we that have the private key in a file, let's transfer it.

> `scp -P 2220 bandit16@bandit.labs.overthewire.org:[temp directory address]/* ./`

Don't forget to replace the `[temp directory address]` with the address you got earlier.

Now we need to change the permissions for the private key and connect to `bandit17` using the key.

> `chmod 700 sshkey17.private`

> `ssh -i sshkey17.private -p 2220 bandit17@bandit.labs.overthewire.org`



## level 17

This is another very easy level. We just need to find out what's different between the two files we have. `diff` command will take care of that for us.

> `diff password.old password.new` 

And we have the password for the next level.

The line starting with `<` is what was in the `password.old` file and the one starting with `>` is the password for next level.


## level 18

When we connect we see that the server kicks us out. It isn't a bug, it's just to teach us we can send arguments in our `ssh` command.

> `ssh -p 2220 bandit18@bandit.labs.overthewire.org "ls |xargs cat"`

The `ls` command will list what's in the directory, then we are pipelining the list to `cat` which will read us the files. `xargs` is a utility which helps with pipelining and will feed `cat` the list from `ls`.


## level 19


This level is the first time we will use the `exec` command to a `setuid` binary file. It lets us run a command as if it was another user (in this case it's `bandit20`) doing it.

> `exec ./bandit20-do cat /etc/bandit_pass/bandit20`

And we have our password. Onto the next level.


## level 20

This level has another `setuid` binary. But this time it will connect to a localhost's port that it is given as an argument, then if it receives this level's password, it will give us next level's password.

First step is to setup a server on an unoccupied port that listens and will just send this level's password.

> `cat /etc/bandit_pass/bandit20 | xargs echo -n | nc -l -p 33333 &`

Let's digest what's happening. The first part is simple, it reads the current level's password from the `bandit20` file.

In the second part, we are using `xargs` to pass the password from the first part as an argument to the `echo` command. `echo` will just repeat whatever we give it as an argument. The `-n` flag makes it so there is not a newline character at the end of the message.

The third part sets a server using `nc` that listens due to the `-l` flag and the `-p` flag is to specify a port. 

The port number isn't important, it just needs to be unoccupied and we need it for the next part.

Lastly there is the `&` character. It is the main thing we are learning this level. It makes it so the commands (jobs) we entered in that line are all running in the background so we can use the terminal for other commands we wanna run at the same time.

Now that we have setup the server, we can run the `setuid` binary and get the password.

> `exec ./suconnect 33333`



## Level 21

In this level, we are introduced to `cron` which is a time based job scheduler. We need to find out what the job is and use it to find the password.

> `cat /etc/cron.d/cronjob_bandit22`

This will show us the job. We can see that there is a `.sh` file is being ran using `bandit22`'s permissions.

Using `cat` on the file,

> `cat /usr/bin/cronjob_bandit22.sh`

We see that it's actually two commands that are being run.

First one is a `chmod` command that is setting the permissions for a file in the `tmp` folder to `644` which means everyone can read the file but only the owner can write to it.

Second command in the script reads the password for `bandit22` and stores it in the file from the first step. 

This means we can just go to the file in the `tmp` folder and read the password since it can be read by anyone.

> `at /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv`

Should give us the password. However it is possible that the file name has changed. Make sure you use the file that is mentioned in the script (the `.sh` file) from earlier.


## level 22


This level starts with another `cron` job. 

> `cat /usr/bin/cronjob_bandit23.sh`

This time the script is a bit more complicated. We need to figure out some stuff. 

First is the `myname` variable. It is equal to the result of the `whoami` command which just returns the username of the user. For `bandit23`, it will return `bandit23`.

Next up is the `mytarget` value. We can just copy the whole command line and simulate the script by replacing `$myname` with `bandit23`.

> `echo I am user bandit23 | md5sum | cut -d ' ' -f 1 | xargs -I % cat /tmp/%`

This will get us the password but let's see why.

> `echo I am user bandit23 | md5sum | cut -d ' ' -f 1`

This command is what we got from the `cron` job and replaced `$myname` with `bandit23`. It gives us the name of the file in the `/tmp` directory which contains the password for `bandit23`.

Next up is the `xargs` utility which helps us with feeding arguments to the `cat` command. This time we are using the `-I` flag which makes it so we can set a token (in our case `%`) to attach the argument where we need. Without this flag, we won't be able to specify the `/tmp` directory when using `cat`.



## level 23


In this level we need to write our own shell-script. But before we do that we need to find out what's the `cron` job for this level.

> `cat /etc/cron.d/cronjob_bandit24`

This will show us where teh script is. Let's see what's inside the script this time.

> `cat /usr/bin/cronjob_bandit24.sh`

This time around the script is a bit more complicated. But all we need is the `/var/spool/$myname/foo` directory. Remember `whoami` returns the username which would be `bandit24` since it is script that runs as `bandit24`.

> `cd /var/spool/bandit24/foo`

Now we need to make a script-shell that copies the password in a file in the `/tmp` directory.

We can just copy the script from last level and use that to get the password. However we should change the `address` variable a bit so we get a unique file.

Open vim 

> `vim script.sh`

You can change `script` to anything you want.

Press `a` to get in insert mode, then type the following 

> `#!/bin/bash`
>
> `myname=$(whoami)`
>
> `mytarget=$(echo this is user $myname hi | md5sum | cut -d ' ' -f 1)`
>
> `cat /etc/bandit_pass/$myname > /tmp/$mytarget`

You should change `this is user $myname hi` to something unique just to avoid someone else accidentally overwriting your password.

When you're done, press `exit` to go back to the normal mode, then type `:wq` to save and quit.

Next we need to change the script's permission so it can be read by `bandit24`. We need to do this before the `cron` job deletes the script we wrote.

> `chmode 755 script.sh`

Don't forget to use the name you selected earlier. 

Now we just wait a minute or two for the `cron` job to do its thing. 

The next command will give you the password if you didn't change the script we wrote earlier. If you did, just type the same thing as last time between `echo` and the first `|`. Also don't forget to change `$myname` to `bandit24` 

> `echo this is user bandit24 hi | md5sum | cut -d ' ' -f 1 | xargs -I % cat /tmp/%`



## level 24


This level requires us to brute force a unique passcode that we need to attach to the end of the current level's password and then send it to the server listening to port 30002. 

We can do this using a simple script. 

First make a temporary directory and go to it.

> `vim script.sh`

Copy the following in the script.

> `#!/bin/bash`
>
>
> `myname=$(whoami)`
>
> `password=$(cat /etc/bandit_pass/bandit24)`
> 
> `touch results`
>
> `for ((i=0000;i<=9999;i++));`
>
> `do`
>
> `        number=$(printf "%04d\n" $i)`
>
> `        echo $password $number | ncat localhost 30002 >> ./results`
>
> `done`


Next we need to enable execute permissions for the owner so we can run the script.

> `chmod 755 ./script.sh`

Then just run it using

> `./script.sh`

After a few minutes we can get the results using the following command.

> `sort results | uniq -u`


## level 25


The password for this level is given to us in a form of the private key for `bandit26` in the homedirectory for `bandit25`. We can get that using our knowledge from level 13.

The real challenge is that the shell for `bandit26` is not `bin/bash`. We need to find what it is and fix it.

To find out what it is, 

> `cat /etc/passwd | grep bandit26`

The `passwd` file contains some basic information about the users, each user's info is in one line and we need the line mentioning `bandit26`.

The shell for `bandit26` is `/bin/showtext/` so we need to change it to `/bin/bash` so we can do what we need to do for next level.

Since we can't change the permissions or the starting shell for users, we need to get creative. First let's check what `/bin/showtext/` do.

> `cat /bin/showtext`

We see that it uses the `more` command to show us a text file named `text.txt`. Let's use the sshkey we're given to try and get in `bandit26` since if the text is too long, we can use `more`'s interactive nature to get out of it before the `exit 0` command kicks us.

Transfer the sshkey and use it to connect to `bandit26`. I am going to skip over how to since we have already done it twice. 

We see that the text is fairly short so the `more` command doesn't go into the interactive mode. Let's shrink the terminal to only a few lines and try again.

If you see `--More--(XX%)`, you did it right, press `v` to go into vim and then resize the terminal to the size you like. Beside being a text editor, Vim lets us run commands. Pressing `:` gets us in that mode. The following commands include the initial `:` but you don't need to type it twice.

> `:set shell=/bin/bash`
> `:shell`

Now we have a bash shell open that we can use. If you type `exit` by accident, you can just retype `:shell` to get back. If you want to leave the shell, type `exit` to go back to Vim, then type `:q!`. You might have to press `enter` once or twice to get rid of the `more` command's interactive mode.

While we're here let's get the password for this level

> `cat /etc/bandit_pass/bandit26`

We are going to have to do the next level in this shell.


## level 26

This is a pretty easy level. We have a file that let's us run commands as if it was `bandit27` so the first thing we might wanna do is get the password like we have before.

> `exec ./bandit27-do cat /etc/bandit_pass/bandit27`

As you can see, before we get the password, we get kicked out of that shell back to the vim. We can go around that by running this job in the background using `&` at the end

> `exec ./bandit27-do cat /etc/bandit_pass/bandit27 &`


## level 27


This level is an introduction to git. We need to clone the repository at the given address to our machine and then get the password from it. 

Make sure you're not logged into `bandit27` and run the following

> `git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo`

Password is the same as `bandit27`. There should be a new file called repo in the directory you are in.

> `cat ./repo/README`



## level 28

This level starts the same as the last, clone a repo and read the file inside. But this time the password has been redacted so we need to see if it was redacted to begin with or was there an initial commit that had the password.

> `git clone ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo ./repo2`

The `./repo2` is so there isn't a conflict with the `repo` file from last level. Use `cd to go in the new directory and let's check the commits.

> `cd ./repo2`

> `git log`

We see that there are 3 different commits to this repository. We can swap between them using `git switch`. The password is in the second commit so let's go there.

> `git switch origin`

Press `tab` to see the commits and their uid. We want `HEAD^` or `8b7c651`

> `git switch --detach 8b7c651`

The `README.md` file contains the password.



## level 29

This level teaches us about switching to different branches.

> `git clone ssh://bandit29-git@bandit.labs.overthewire.org:2220/home/bandit29-git/repo ./repo3`

The `README.md` file doesn't have the password so let's go to another branch.

> `git switch`

Pressing tab shows us 3 branches. Let's go with `dev`

> `git switch dev`

Check the `README.md` file for passport.


## level 30

Same as the previous levels there is a git repo that we need to clone and get the password from. This time however we are dealing with `git tag`

> `git clone ssh://bandit30-git@bandit.labs.overthewire.org:2220/home/bandit30-git/repo ./repo4`


This is the initial commit and the `README.md` doesn't have the password.

> `git tag`

This shows us if there are any tags and well it turns out there is one. We can view it using `git show`

> `git show secret`

And that's our password.




## level 31


Another repo to clone.

> `git clone ssh://bandit31-git@bandit.labs.overthewire.org:2220/home/bandit31-git/repo ./repo5`

Reading the `README.md` we see that we need to push a text file. There is a `.gitignore` that excludes `.txt` files. So let's just delete it.

> `rm './.gitignore'`

Let's make our text file.

> `echo 'May I come in?' > key.txt`

And the next steps are to add the file to our local git repo, commit the changes and then push the file to the remote repo.

> `git add key.txt`

> `git commit -a`

Now we are presented by a text editor called `nano`. Just describe what we added and press `ctrl + x`.

> `git push`

After you enter this level's password, you are given the password for next level and your push is automatically rejected.



## level 32


This level starts us in a different shell called the `uppershell`. It only lets us use commands that are in uppercase, which are not any we have used before. If we type `printenv` in a bash shell outside of this level, we see that there are multiple variables we might be able to use. We are going with the `$0` variable which let's us get a normal shell.

> `$0`

Using `ls -l` we can see that the `uppershell` file is owned by `bandit33` and is a `setuid` file. I didn't figure this out originally and ran 

> `exec /bin/bash`

After seeing `bandit33@bandit` I realized this is a `setuid` file.

Anyways, now we have a shell we can run our lowercase commands in and we have `bandit33`'s permissions, we can just get the password using

> `cat /etc/bandit_pass/bandit33`



At this time this is the last level available. 

Thanks for reading this document all the way and I hope it was helpful.


