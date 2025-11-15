python flask backend implemenation for climate  control AC and CT
<img width="1843" height="862" alt="image" src="https://github.com/user-attachments/assets/8ca427fc-bad9-4c28-8dcf-032732fd927f" />
Python scriota are set to be run automatically at bootup. Sercices can be checked by running:
sudo systemctl status climate.service
sudo systemctl status temp.service

For consiguring the services the following commands must be run:
  - sudo systemctl deamon-reload - ensure tha that the added/changed service is registered  
  - sudo systemctl enable "your_service".service - enabling the service to be loaded
  - after that the service can be started/stopped/restarted or get the status in the clasic way by using systemctl command

temp.service will be delay by 30s as the GPIO/DHT22 must be sure that are right initilized after startup sequence.
