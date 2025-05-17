# Match Survey
## Acknowledgements
Inspiration for this project originated from efforts by Reddit user 
u/bearded_booty. Much of the setup and original rating details come from their 
efforts and experiences for surveys they generated for the St. Louis CITY SC 
and Arsenal FC subreddits.
## About
This contains a Python package to survey fans' about matches played by your 
favorite soccer club. Rating setup includes players that played, managerial 
decisions, referees, and other match elements. Data scraping includes modules 
for [FBRef](https://fbref.com/en/) and [FotMob](https://www.fotmob.com/). 
Surveys are generated using Google Cloud API for Forms, and includes some 
additional pieces for moving Forms to a Google Drive of your choice (after some 
setup in Google Cloud) and digesting survey results from Google Sheets. Some 
presentation modules help generate graphics for communicating results to your 
community of fans surveyed.

This is a work in progress, so some pieces are not fully functional just yet.

## References
### About Rating Systems in General
Users of this repo can encourage their community to rate in whatever way they 
wish, but fans frequently ask how to go about rating or how to interpret 
various rating values. Here I've compiled a small set of references to 
different rating systems that can help you communicate some structure for your
ratings setup. There are several links included and a brief idea behind them. 

One thing is common to each, the ratings give a point to debate with others.

- [results post from first survey for CITY from bearded_booty](https://www.reddit.com/r/stlouiscitysc/s/ZoOv1UgMcm) - 1-10, suggested to be based on how we feel. This is what we've been doing for a bit over a year now. These have been really fun to me, so it's difficult to pin down a specific style other than what our collective gut says.
- [SportMonks](https://www.sportmonks.com/blogs/player-ratings/#:~:text=Player%20ratings%20are%20a%20numerical,evaluate%20players%20at%20a%20glance.) - starts at 6.5 and states usage of 51 stats and range of 3-10.
- [WhoScored](https://www.whoscored.com/explanations) - starts at 6 and states usage of many stats with range 0-10. while not in depth, they do provide a nice graphic for volume of players between integer level ratings, near 55% of players land between 6-6.9, less than 0.4% below 4.9, and about double that percentage of players get in the 9.0-10 range.
- [Sofascore](https://corporate.sofascore.com/about/rating) - starts at 6.5, requires 10min play time, and considers many stats which some are listed at the linked page after scrolling for a bit. interesting range with minimum at 3, but as usual up to 10.
- [post from r/footballmanager](https://www.reddit.com/r/footballmanagergames/s/YHpldgsXvk) - seems that game and thread discussion doesn't reveal much, but might be interesting for some here.
- [CBS](https://www-cbssports-com.cdn.ampproject.org/v/s/www.cbssports.com/soccer/news/soccer-player-ratings-from-0-10-explained-performances-from-erling-haaland-ali-dia-geoff-hurst-and-more/amp/?amp_gsa=1&amp_js_v=a9&usqp=mq331AQIUAKwASCAAgM%3D#amp_tf=From%20%251%24s&aoh=17445630626796&referrer=https%3A%2F%2Fwww.google.com&ampshare=https%3A%2F%2Fwww.cbssports.com%2Fsoccer%2Fnews%2Fsoccer-player-ratings-from-0-10-explained-performances-from-erling-haaland-ali-dia-geoff-hurst-and-more%2F) - starts at 5 and range 0-10. Their ratings seem to include the context of a match, regulation vs cup match, for example. This link uses interpretation of their ratings to explain how their system works, and they provide an example player and match for each value.
- [FotMob](https://www.fotmob.com/faq) - starts at 6 and ranges 1-10 while using over a 100 stats. From the brief description, this probably resembles closest to what our community does, sort of.

## Google Cloud
When working with Google Forms, Drive, & Sheets, I needed to dig a ton, so here 
is a list of sites I found useful in getting things set up and working.
### Guides
- [v1 API](https://developers.google.com/discovery/v1/reference/apis)

- https://support.google.com/docs/thread/5796831/hi-can-i-import-questions-from-a-google-sheet-to-google-forms?hl=en
- https://developers.google.com/apps-script/reference/forms/form-app
- https://cloud.google.com/apis/docs/client-libraries-explained
- https://cloud.google.com/python/docs/reference
- https://developers.google.com/drive/api/guides/folder#python_1
- https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to
- https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment
- https://stackoverflow.com/questions/73218683/what-is-the-use-of-discovery-build-in-google-api

- https://github.com/googleapis/google-api-python-client/blob/main/docs/oauth.md
- https://docs.gspread.org/en/v5.7.0/user-guide.html
- https://console.cloud.google.com/auth/clients/643111483090-6iga4k6qk13jjtjcetps6ms0rindqijg.apps.googleusercontent.com?inv=1&invt=AbrsmA&project=city-reddit-polling
### For your Oauth2 key
- create key
- download json (by default it tries to save with .com suffix, so rename by adding .json to its ending)
