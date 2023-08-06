# automate-django
A python script to automate your django production,
It creates a boilerplate,
connects to urls.py, views.py, template files, css and runs the django server and opens the content in browser automatically and output the boilerplate project directly.


## steps for installing on mac, linux and windows:

### note: needs django=2.1 for running this script and python version 3 up

**install python3,

i hope it is installed on your computer 

if not goto https://python.org

**After python installation

first install virtualenv using pip

    pip3 install virtualenv
  
then create a virtual environment named 'env' lets say,

activate virtual environment 'env'

for mac:

    source env/bin/activate
   
for windows:

    env\Scripts\activate
    
install django after activation

    pip3 install django==2.1
    

install neccessary setup files

use:

    pip3 install automate_django


import package as shown below:

    from automate_django import automate_django as ad

    ad.create_project()
    
run your file using python3 filename.py

enter project name and application name and sit back:

your project will be running in your default browser

and automatically you will see website running in your default web browser

you can edit reuse code 

enjoy!!!
