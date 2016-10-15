sopel-quote (fork)
============

A quote module for sopel, an irc bot written in python. This fork only supports MySQL as the datastore for IRC quotes. I used to run an eggdrop which used to use MySQL to store IRC quotes. sopel plus this module made the transition pretty easy! 

This is a somewhat custom module, so I've removed a lot of code I didn't need. I'm not saying it's clean code, but it works. 

The plugin saves the following to the database:
* IRC nick of who submitted the quote
* The hostmask of the IRC nick who submitted the quote
* The quote itself
* The channel the quote was submitted from
* The timestamp in UNIX EPOCH

## getting started

Run the `quotes.sql` file in your MySQL to setup the table structure. 

Add this to your default.cfg file:

    [quote]
    datasource = mysql
    user = YOUR_USERNAME
    password = YOUR_PASSWORD
    host = YOUR_HOST
    database = YOUR_DATABASE
    
I didn't like how the original plugin used subcommands, so this fork changed the commands. 
Valid commands in this fork are below. Replace the ! with your sopel prefix (defaults to `.`):
* **!q** or **!quote** - gets a random quote from the database
* **!addq** or **!addquote** - adds a new quote
* **!delq** or **!delquote** - deletes a quote. **Only the bot owner, or quote owner can delete the quote**
* **!findq** or **!findquote** - Find a quote that contains the search term
* **!getq** or **!getquote** - Get the quote from the database that matches the ID provided
* **!lastq** or **!lastquote** - Get the last quote submitted to the database

The original sopel-quote project can be found here: https://github.com/gehsekky/sopel-quote
