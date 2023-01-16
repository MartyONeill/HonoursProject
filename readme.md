# Guidance

This is the source code for Mezzanine. The project developed for Marty O'Neill's 4th year dissertation project. Supervised by Christos Anagnostopoulos, this was completed as part submission of the honours requirements. 

The method for installing and running Mezzanine can be found in Manual.txt.

The database is prepopulated with a test environment utilising both recommender systems. This can be seen when navigating to:
	- Glasgow
	- Edinburgh 

Example profiles have been made:

## Talent
username: JohnTheDJ
password: Talent1234

## Venue
username: FratelliSarti
password: Veune1234


There is a system lag when searching the map, within 10-15 seconds the system should continue operating normally.



# Deploying the site 

Mezzanine is build using Python 3.7.4

The chosen terminal for use was Anaconda Powershell Prompt (anacodna3)

Steps
## navigate to the directory - 2335418o

## Create a virtual environment, this can be done in anaconda with command
        conda create -n *your_chosen_enironment_name*

## Run the command in the directory:
        pip instal -r requirements.txt

## Run the corresponding Django DataBase migration commands:
        python manage.py makemigrations
        python manage.py migrate

## Finally, input the running command:
        python manage.py runserver

Once these steps have been completed, navigate to : http://localhost:8000