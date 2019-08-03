# Setup Instructions

Get the the credentials json file and save it as `firebase.secret`

Create a file called `databaseurl.secret` with the firebase realtime endpoint (e.g. https://project.firebaseio.com/)

Create a virtual environment and install requirements.txt: `pip install -r requirements.txt`

Set `DEBUG` and `PRODUCTION` in the settings package to the correct values

Update `BAUDRATE` in the settings package if needed

If a permission error is thrown on run, use `sudo chmod 777 /dev/tty[A-Za-z]*` to fix the problem