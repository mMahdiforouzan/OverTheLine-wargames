
# Krypton

This is a step-by-step guide for the krypton game from [overthewire.org](https://overthewire.org/wargames/krypton/)

This guide's commands are for linux, I personally used kali linux, and it does assume you have either played the bandit wargame or have some basic knowledge with unix. If you're on windows, you can follow the steps about how to break each code but some commands are going to be different.

The Host URL for this challenge is `krypton.labs.overthewire.org` at the 2231 port.

And the username follows the same pattern as before. Username is `kryptonX` where X is the level number.

## level 0

The encrypted password is given in `base64`, we can decipher it easily using the following command in bash. You need to replace `password` by the password given in the website.

> `echo -n password | base64 -d`

Now that we have the password, let's connect to the server.

> `ssh -p 2231 krypton1@krypton.labs.overthewire.org`

This game doesn't put us in the right directory like the bandit game so we need to get there first.

> `cd ../../krypton/`

All the levels are in different files, we're going to go ahead and start in `krypton1`. I will not describe how to move between levels just to keep things moving faster.


## level 1

The file has a `README` describing the cipher and an encrypted file named `krypton2`. The cipher is a ROT13 and since we did this already in the bandit game, we know we can just solve it using the `tr` command.

> `cat krypton2 | tr {a-zA-z} {n-za-mN-ZA-M}`
