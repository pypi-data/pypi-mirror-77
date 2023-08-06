# cockli-gen

A tool to randomly create [cock.li](https://cock.li) email addresses on the commandline.

***Usage***

```  
grrfe@feowo:~$ cockligen --help
usage: cockli-gen [-h] [-d DOMAIN] [-p PASSWORD_LENGTH]
                  [-mil MINIMUM_USERNAME_LENGTH]
                  [-mal MAXIMUM_USERNAME_LENGTH] [-s SIMPLE]

Create a random cock.li mail address

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Select one of cock.li's many domains; default =
                        cock.li
  -p PASSWORD_LENGTH, --password-length PASSWORD_LENGTH
                        Override the default password length; default = 32,
                        min = 8, max = 255
  -mil MINIMUM_USERNAME_LENGTH, --minimum-username-length MINIMUM_USERNAME_LENGTH
                        Override the default minimum username length; default
                        = 10, min = 1
  -mal MAXIMUM_USERNAME_LENGTH, --maximum-username-length MAXIMUM_USERNAME_LENGTH
                        Override the default maximum username length; default
                        = 16, max = 32
  -s SIMPLE, --simple SIMPLE
                        Simple output, username:password
```