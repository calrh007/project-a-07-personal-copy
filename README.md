# Exercise Gamification

**Are you looking for a way to stay motivated, keep up with personal workout goals, and keep track of those gains? :muscle: :running_woman: :weight_lifting_man:**

Through our web application, you can easily record all your workouts and associated workout information!  
Access all your stored workout information all on one website.  

:desktop_computer: Take a look at our project: https://project-a-07.herokuapp.com 

*Created by Ashley Crawford, Drew Goldman, Cal Hartzell, Kieran Humphreys, and Jennifer Tcheou.*

## Description

Our web app enables users to not only record their own workouts but also earn achievements and badges and compete with other users through our leaderboard system. 

**:star2: Check out a list of all our features :star2:**
- Ability to record all information associated with your workouts :fountain_pen:
- Add custom workouts if your workout is not already in our system :pushpin:
- View a list of all your recorded workouts and associated workout information :spiral_notepad:
- Manage already recorded workouts through editing or deleting them :memo: 
- View the weather on the day of your recorded workouts :sun_behind_small_cloud:
- See your overall workout summaries and filter by timeframe :date:
- Gain points and badges for reaching achievements :dart:
- Check out how you compare to other users on the sitewide leaderboard :medal_sports: 
- Edit and change your username and zipcode :round_pushpin:

To use this web application, please first log-in using your Google account.
If you want to add a workout that you have completed, head on over to the "Add Workout" tab to add your workout. 
If you do not see your workout within the dropdown menu, click on "Desired workout not available?" to learn more about how you can add a custom workout. 
See all your workouts under "My Workouts" and a summary of all your workouts under "Workout Summaries".

## Used Packages & Citations

We built this project using [Django](https://www.djangoproject.com) + [Bootstrap](https://getbootstrap.com) along with additional Python and Django packages:
- [gunicorn](https://gunicorn.org)
- [django-heroku](https://github.com/heroku/django-heroku)
- [django-allauth](https://www.intenct.nl/projects/django-allauth/)
- [django-measurement](django-measurement)
- [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
- [m26](https://pypi.org/project/m26/)
- [Pillow](https://python-pillow.org)
- [pgeocode](pgeocode)

In addition to the packages listed above, we incorporated a weather API to gather the information on the weather on the day of each workout.  
:link: https://openweathermap.org/api

We modified a free HTML template as a home page: 
:link: https://www.free-css.com/free-css-templates/page250/runner-onepage

Code citations are included included at the beginning of the respective files in the following format:
```
/***************************************************************************************
*  REFERENCES
*  Title: <title of program/source code>
*  Author: <author(s) names>
*  Date: <date>
*  Code version: <code version>
*  URL: <where it's located>
*  Software License: <license software is released under>
*
*  Title: ....
*
***************************************************************************************/
```