## Stats-Website
This application is a elo tracker to track player elo rating for company/office games. This app was creating using Django for both the frontend and backend. 

## Run using Docker
1. docker-compose build
2. docker-compose up

#### To run the server
1. python3 manage.py runserver

#### To initialize database
1. python3 manage.py makemigrations
2. python3 manage.py migrate

## Implementation
Working Features:
    - User registration
    - User login
    - User password reset
    - Company registration
    - Creating a new game
    - Recording the results of a match
    - Viewing results 
    - Viewing player profile
    - Tracking player elo changes per win/loss 
    - Leaderboard to display rankings
    - Separating games so only users of that company can view them
    - Implementing admin previleges for company admins
    - Creating/updating/deleting upcoming matches
    - Email notification of upcoming matches
    - Ability to filter the upcoming games a user views based on game type or date

Unfinished Features:
	- Match making based on elo
	- Ability to sign up teams

## Run
http://0.0.0.0:8000/
