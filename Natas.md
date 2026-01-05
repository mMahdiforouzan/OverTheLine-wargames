# Natas

This game is done through a browser. I am going to use Firefox until level 5 so some of the shortcuts might be different if you're using a different browser.

After level 5 I'll be using a bash shell sometimes so I can connect to the website using `curl`. This is what I decided to do because doing it in firefox would require a lot of changes to security features built in.

To connect to each level, we need a URL, username and password.

URL is always in the `http://natasX.natas.labs.overthewire.org` format where `X` is the level number. And the username is `natasX`. 


## level 0

> URL: `http://natas0.natas.labs.overthewire.org`
> username: `natas0`
> password: `natas0`

From now on I am going to assume you know all the details since username and URL are easy to change (Just change the 0) and you should have the password from doing the level.
 
## level 1

After connecting, we don't see anything on the page so let's check the source code of the page. We can `right click` and find `View page source` or just use `ctrl + u`

The password is commented at the bottom.


## level 2

In this level, right clicking is blocked but `ctrl + u` isn't.

Password is in the same place


## level 3

This time there is no comments but in the source code we cam see that there is a png pixel located in a directory named `files`. Let's go to that directory by changing the URL to the following.

> `http://natas2.natas.labs.overthewire.org/files/`

You can also just click on the `src` for the `img` to go to it then delete `pixel.png` from the URL.

The source code looks a bit crazy so you can just remove the `view-source:` in the url to get a more user-friendly look. 

I am going to just refer to this as the normal mode and the source code view as source code from this point forward.

There are two files here, `pixel.png` and `users.txt`. Our password is in the text file.


## level 4


This time around there is nothing in the source code. Except a hint to google not being able to find the information leak. Google and other search engines use crawlers which are automated robots that crawl the web to find every server and what's on them. There is a `robots.txt` file that servers can create that tells this robots where they can and can't go. It is located in the root directory.

> `http://natas3.natas.labs.overthewire.org/robots.txt`

The excluded directory is where the `users.txt` is with the password inside.


## level 5

For this level I am going to use a bash terminal so I can use `curl` to change a request header.

We can connect to the website using the following command.

> `curl natas4:password http://natas4.natas.labs.overthewire.org`

Replace the `password` by the password you got from last level.

As you can see, we need the server to think we are coming from `http://natas5.natas.labs.overthewire.org/`. We can do that by changing the `referer` response header in our request.

> `curl -u natas4:password -H "referer: http://natas5.natas.labs.overthewire.org/" http://natas4.natas.labs.overthewire.org`

Don't forget to change the `password`.



## level 6

This time around we need to change cookies for our connection. Let's first check what cookies there are with this level.

> `curl -u natas5:password -c natas5 http://natas5.natas.labs.overthewire.org`

This will create a file called `natas5` in the current directory. Reading it with the `cat` command we see that there is a `loggedin 0` cookie. 

We can change that in the file and use the `-b` flag in our curl command and the file or just add a `"loggedin=1"` string. I'll go with the latter.

> `curl -u natas5:password -b "loggedin=1" http://natas5.natas.labs.overthewire.org`

Don't forget to change the `password`.



## level 7


This time we can go back to firefox. Logging in we see a form that requires us to submit a secret code. There is also another option to `View sourcecode`. After pressing `View sourcecode`, we see a PHP <? ?> tag for the POST request. It has a `include` section which looks interesting. Let's add that string to the end of our URL.

> `http://natas6.natas.labs.overthewire.org/includes/secret.inc`

And our secret is right there. Go back to the main page and enter the secret string for next level's password.



## level 8


In this level we are given two options which at first seem to be useless, but after opening the source code, we are reminded that the password is at `/etc/natas_webpass/natas8`.

By changing the query string (the data after the `?`) we can set the `page` variable on the server to the contents of any file we want.

> `http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8`



## level 9


This level involves a bit of reverse engineering. Looking at the `View sourcecode` we see that there is a string `3d3d516343746d4d6d6c315669563362` which is the result of the password going through an encoder function. If the string is different, you need to change it in the next step.

The encoder first encodes the secret in base64, then reverses the resulting string, then translates it from binary to hexadecimal. We can reverse it by doing the opposite steps to the encoded string we found.

In your terminal run this command

> `echo 3d3d516343746d4d6d6c315669563362 | xxd -p -r | tr -d '\n' | rev | base64 -d`

You can enter the result in your browser for the password.


## level 10


This time we are dealing with a unsanitized input vulnerability. As we can see in the sourcecode provided via `View sourcecode`, The input is passed to the server using the `passthru()` function. There are two ways of using this for our benefit, the intended way and the "easy way". I will list both and recommend you try the intended way since we will have to be doing the "easy way" for next level anyways.


### intended way

We can use the fact that there is no sanitization of inputs to our advantage to end the `grep` command early using a `;` and then we can use the `cat` command to read the file containing the password for `natas10`

> `curl -u natas9:password -X POST -d "needle=;cat /etc/natas_webpass/natas10;&submit=Search" http://natas9.natas.labs.overthewire.org`


## "easy way"

Another way to do this is using the fact that `grep` can process multiple files. This is also the "easy way" of doing it since it can be done through firefox without having to deal with special characters. The following input should get the password. It does however print the whole `dictionary.txt` which might take a second.

> `. /etc/natas_webpass/natas10`

## level 11

This level is meant to be an evolution of the last question with the intended way. As I said before we are just going to use the fact that `grep` can deal with multiple files.

> `. /etc/natas_webpass/natas10`

As before, it will print out the whole of `dictionary.txt` so it will take a bit longer to load the page.


## level 12

This level was more of a cryptography level than anything. There is a python script named `natas11.py` in this repo that you can use to get the new cookie we need to send to the server to get our password. I am going to explain how to do everything and then explain why it works.

> `curl -u natas11:UJdqkK1pTu6VLt9UHWAgRZz6sVUZ3lEk -c ./natas11 http://natas11.natas.labs.overthewire.org`

This will connect us to the server and also put the cookies in a file named `natas11` in the same directory. Compare the value after `data` with the one in the python code for the `cookie` variable. If it's different just replace it. Be careful of the URL safe version of some symbols, especially if you see `%3D`, just replace it with an equal sign `=`. After running the python code, replace the `value` after `data=` in the bottom command with what you get from it.

> `curl -u natas11:password -b "data=value" http://natas11.natas.labs.overthewire.org`


### explanation

We basically need to use the default values which are used to make the cookie for this level and do a XOR operation on each bit with the same index bit of the cookie we get from the server. This get's us the key used to encrypt the cookie. This is all due to the transitive property of the XOR operation. After getting the key, we need to figure out if the key was repeated or not, you can skip this since the key was repeated perfectly ten times and wasn't cut at the end, but for the sake of completeness I have done that in the python script. After finding the actual original key, we can use that to set the `showpassword` flag to `yes` by making a json array with the values we want and encrypting it using the same methods as the sourcecode. Sending this new cookie to the server we will get the password.