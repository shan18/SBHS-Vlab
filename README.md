# SBHS Virtual Labs Server
![SBHS logo](logo.png)

 Please follow the steps below to set up the server code on your system:
 
 + Clone this repository.  
 `git clone https://github.com/FOSSEE/SBHS-Vlabs.git`  
If you have permission issues, make sure that you are added as a collaborator.
Contact rupakrokade@gmail.com

+ Install **pip** and **virtualenv**. These two packages need to be installed globally on your system.  
+ Setup a virtualenv in your system.  
To check which is the default python in your system:  
`python --version`
  + If Python 2.7 is the default in your system, type the command
  `virtualenv venv`
  + If Python 3.x is the default in your system, type the command  
  `virtualenv venv --python=python2.7`
+ Activate the virtualenv with `source venv/bin/activate`
+ Go into the project directory and install the dependencies.
```bash
cd SBHS-Vlabs/
pip install -r requirements.txt
```

+ Create and run the database migrations using the following commands  
```bash
python manage.py makemigrations tables
python manage.py makemigrations yaksh
python manage.py makemigrations
python manage.py migrate
```

+ Run the server with `python manage.py` runserver. Open **localhost:8000** in your browser.


### Instructions for setting up Apache
+ Make sure you have **Apache 2.4** installed on your system.

+ Install the ***mod-wsgi*** module.  
`sudo apt-get install libapache2-mod-wsgi`
+ Enable the module *(If not enabled already)*  
`sudo a2enmod wsgi`
+ Open the file **index.wsgi** in your favourite editor.  
Set the variable `path_to_venv` as the absolute path to your virtualenv  
Set the variable `path_to_project_root` as the absolute path to your project root directory.  
**Note the trailing slashes in both the path names.**
+ Copy the file *apache.conf* to the sites-available directory.  
`sudo cp apache.conf /etc/apache2/sites-available/002-sbhs.conf`  
+ Change the variables **python-path** and **python-home** to point to your **sbhs_server** directory and your **venv** respectively.
+ Change the path to your **index.wsgi** accordingly.
+ Once you're done with all this, enable this site and disable the existing default site.
```bash
sudo a2dissite 000-default.conf
sudo service apache2 reload
sudo a2ensite 002-sbhs.conf
sudo service apache2 reload
sudo service apache2 restart
```
+ Chown the entire project to set *www-data* as the group.  
`sudo chown -R yourusername:www-data sbhs/`

+ Apache needs write permissions to the **log** and **experiments** directory.  
```bash
mkdir -p log experiments
touch log/django-error.log
sudo chmod -R 775 log experiments
```

+ Reload Apache. Your site should be live now at **localhost/sbhs**  


### Instructions for creating a superuser
+ Open **sbhs_server/tables/models.py**. Go to **create_superuser()** function in class **UserManager**.  
Set the value of the **email** parameter with your desired email address.

+ Now create the superuser with the following command
```bash
python manage.py createsuperuser
```
Then enter the username and the password.
