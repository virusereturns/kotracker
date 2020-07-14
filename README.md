# KOTRACKER

Tournament Tracker for the RetroGamingLiveTV Knock-out One Night Only Tournaments. This project runs on django 3.0.8

# Requirements

* Python 3.8.3
* A database server (tested with postgres on heroku and locally)

# Settings

Soon

# Usage

From the `/` root of the web app you can access:
* All tournaments that have been created
* The admin for all tournaments
* A link to create a new tournament in the django admin

The first step is to create a Tournament in the django admin, and add some racers in the same screen. You can also add all the PBs for them. After that, the new tournament will appear in the main menu. You can access the "Overview URL" to show as a Browser Source on OBS, that will show all runners PB on a fancy way.

After this is done, the next step is to create the first round. On the main menu, pressing the "Create Next Round" link will take you to a screen where you can enter the times for the first round. After you're done, you can press save, and all runners will be ordered by the times you entered. You can then manually select which runners will be eliminated or indicate which ones have dropped from the tournament.

On each round, you can copy the "(Copy this URL in OBS)" link to create the Browser Source for the round that you just edited.

If any corrections need to be done to the tournament (un-eliminate, un-drop racers), you can access the "Edit Tournament" link from the edit round section.

# Special thanks

baldnate for the CSS styles
