Have you ever had prolems in your discord group of people abusing music bot?

Luckily i have a solution for that!

Here we have a Flask based web application with following feature:
- Users can submit music bot request form
- Admin can Approve and Decline requests
- Requests are automatically updated on users dashboard

Instead of chaos/arguing/rage kicking/rage banning in voice channels because somebody else wanted to play music, 
you now have a structured music scheduling which users can follow.

-Setup-

```
git clone https://github.com/henkka008/discord_music_bot_request_form.git
cd discord_music_bot_request_form
python -m venv env
source env/bin/activate
pip install -r requirements.txt

Create .env file and setup the following:
SECRET_KEY=<CREATE SOMETHING HERE>
ADMIN_INVITE_CODE=<THIS WILL BE THE INVITE CODE THAT IS REQUIRED TO CREATE ADMIN USER>

Then run the app:
python3 app.py
http://127.0.0.1:5000

```
> This started as a joke idea — but the real goal was practicing building full-stack Python applications.
