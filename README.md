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

We built this project using Django + Bootstrap along with additional Python and Django packages:
- gunicorn
- django-heroku
- django-allauth
- django-measurement
- django-crispy-forms
- m26
- Pillow
- pgeocode

In addition to the packages listed above, we incorporated a weather API to gather the information on the weather for each workout.
Link to API: https://openweathermap.org/api
