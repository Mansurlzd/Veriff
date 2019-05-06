# VeriffTask
Usage:
Clone the repository
### Install **pip** first

    sudo apt-get install python3-pip

### Then install **virtualenv** using pip3

    sudo pip3 install virtualenv 

### Now create a virtual environment 

    virtualenv venv 

>you can use any name insted of **venv**

You can start the application as by running:
```
$ python app.py
```
Make sure port 5000 is open
###Overview of application:
Applications detects 18 faces in 2.97 sec,2,69 for 6 faces and etc.
Latency could be due to reading the image and converting operations and saving in the  buffer,these operations decrease the speed.
Throughput is normal,but it could be better when testing  pictures increasing accuracy percentages.
Additional features can be done for speedy detection,saving images and indexing or register faces and predict them fast.
