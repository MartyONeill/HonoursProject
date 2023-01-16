# User manual 

# Running the site
The instructions for running the site can be found in the readme.md

# Folder Structure

## Account
This folder is the django MVT application associated with all account functionalty - including register, sign in, edit accounts for Venue and Talent. 

## Algorithm
This folder contains all of the logic behind the mapping, recommenders - cosine and kmeans - and the preprocessing 

## level4_site 
This folder contains the framework helper functions used in the site, along with the settings and links to other file paths used in the system

## mezza 
This folder is the django MVT application associated with the system funcitonality that does not conform to the Talent/Venue types. Such as Events, recommedner system front end, home page, base pages etc

## static
Contains the satitic files used, in Mezzanine, only 2 static files are used for the images ofthe register page. 

## db
This SQLITE3 file contains the data needed to create the test environments used. This results in an example that can be used when created for the first time. Venues in Glasgow and Edinburgh, and Events assocaited with them are included for browse. It also includes some example profiles as seen in readme.txt

## manage.py 
conains the commands used to run and opperate the system



