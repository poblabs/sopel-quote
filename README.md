sopel-quote (fork)
============

A quote module for sopel, an irc bot written in python. This fork only supports MySQL as the datastore for IRC quotes. I used to run an eggdrop which used to use MySQL to store IRC quotes. sopel plus this module made the transition pretty easy! 

This is a somewhat custom module, so I've removed a lot of code I didn't need. I'm not saying it's clean code, but it works. 

## getting started

Add this to your default.cfg file:

    [quote]
    datasource = mysql
    user = YOUR_USERNAME
    password = YOUR_PASSWORD
    host = YOUR_HOST
    database = YOUR_DATABASE

The original sopel-quote project can be found here: https://github.com/gehsekky/sopel-quote
