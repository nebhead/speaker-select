# speaker-select

## Raspberry Pi based Speaker Selector using Python and Flask 
##### Also uses Bootstrap (http://getbootstrap.com/) and Ti-Ta Toggle (http://kleinejan.github.io/titatoggle/) 

This project was inspired by David Liu and his excellent speaker selector project (http://iceboundflame.com/projects/multi-room-audio-control-with-rpi).  I encourage you to check it out and get a rough idea of how this all works. 

This version of the speaker selector script is highly tuned to my particular setup.  I have only three sets of speakers, using the Niles SS4 speaker switch.  I've used relays that I purchased on Amazon.com (https://amzn.com/B00KTELP3I), which are great for this particular project.  If you want a fourth set of speakers to be added, you will need to add a couple relays to support this.    

Since my personal setup will use the living room speakers only, by default, 99% of the time I've set this up as "normally closed" on the relay.  The other three sets of relays can be normally open since they're more rarely used.  This will hopefully save the relays from getting worn out too quickly. 

To install: 
> sudo git clone https://github.com/nebhead/speaker-select.git

> sudo apt-get update && sudo apt-get install python-pip
> sudo pip install flask

To run: 
> sudo python pi-app.py
