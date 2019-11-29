OpenREM in a Docker image
OpenREM

Containerisation by Chris Williams

Windows 10 setup instructions:
Administration access required!

 - install docker for windows
 - run docker for windows
 - ensure the NAT range is 10.0.75.* (if it isn't, change to this range or adjust other settings as required)
 - pull this project from github
 - pull the modOpenRem folder from github, rename to openrem/app/openrem
 - manually edit the following files in the config directory as appropriate: local_settings.py orthanc.json
 - navigate to project folder
 - in powershell, run the command docker-compose up
 - in a new powershell window: >docker exec -it openremserve_web_1 /var/dose/initialise.sh
 - Add the superuser account details
 - Navigate to the webserver (should be at 10.0.75:8080)


To backup the database:
 - TODO

Firewall and port mapping:

Allow incoming DICOM data exchanges on port 104:
Add windows firewall rule to allow incoming connections on port 104
netsh interface portproxy add v4tov4 listenport=104 connectaddress=10.0.75.2 connectport=104

Allow external connections to the webserver:
Add windows firewall rule to allow incoming connections on port 8000
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8000 connectaddress=10.0.75.2 connectport=8000

Allow remote access to postgres database (important if installation is a gathering point rather than a standalone)
Add windows firewall rule to allow incoming connections on port 5432
netsh interface portproxy add v4tov4 listenport=5432 connectaddress=10.0.75.2 connectport=5432

netsh interface portproxy add v4tov4 listenaddress=10.80.8.57 listenport=104 connectaddress=10.0.75.2 connectport=104
netsh interface portproxy add v4tov4 listenaddress=10.80.8.57 listenport=80 connectaddress=10.0.75.2 connectport=8080
netsh interface portproxy add v4tov4 listenaddress=10.80.8.57 listenport=8080 connectaddress=10.0.75.2 connectport=8080
netsh interface portproxy add v4tov4 listenport=5432 listenaddress=10.80.8.53 connectaddress=10.0.75.2 connectport=5432

netsh interface portproxy delete v4tov4 listenport=5432


TODO:
 - Amalgamate logs in a useful directory
 - Restructure some of the config files
 - Database backup method
 - Find a way to send Orthanc requests to process images directly to rabbitmq
 - Move to an alpine python distribution