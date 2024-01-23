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

On each round, you can copy the "(Copy this URL in OBS)" link to create the Browser Source for the round that you just edited.

If any corrections need to be done to the tournament (un-eliminate, un-drop racers), you can access the "Edit Tournament" link from the edit round section.

# Special thanks

wintery-mix for the CSS styles
