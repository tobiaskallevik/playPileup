<h1 align="center">PlayPileup Backend</h3>


Backend django server using DRF to provide API endpoints for the PlayPileup project

# 🏁 Getting Started

Create a .env file and add the following:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=youremailpassword
```

## If not using the provided dev container
Install the dependencies from the [requirements file](./requirements.txt).
Install cron using:
```
sudo apt-get install -y cron
```
The backend is developed for linux machines, but can be made to work on windows with some tweaks. 

# 🔧 Running the tests <a name = "tests"></a>

The different tests are located in the [tests.py file](./tests.py).

Run all test: 
```
python manage.py test
```  
Run spesific test:

```
python manage.py test -k nameoftest
```  