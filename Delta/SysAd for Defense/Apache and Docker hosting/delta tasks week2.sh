sudo apt-get update
sudo apt-get install -y apache2
sudo systemctl start apache2
sudo a2enmod rewrite
sudo systemctl restart apache2                                      # enabling rewrite module

sudo mkdir -p /var/www/html/soldier.io                                                              # making a directory soldier.io
sudo chown _R $USER:$USER /var/www/html/soldier.io
sudo chmod -R 750 /var/www/html
sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/backup.conf      #copying the conf file to another file
sudo nano /etc/apache2/sites-available/backup.conf

<VirtualHost *:80>
    ServerName soldier.io                                                                            # changing the server name and document root and giving permission
    DocumentRoot /var/www/html/soldier.io
    
    <Directory /var/www/html>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Require all granted
    </Directory>

   # only modifying this block . . .
</VirtualHost>
#save the file
sudo a2dissite 000-default.conf
sudo a2ensite backup.conf                                                                                 #disabling conf file and enabling backup file
sudo systemctl restart apache2


sudo nano /var/www/html/.htaccess                                                # writing the rewrites in .htaccess file

RewriteEngine on

RewriteCond %{HTTP_USER_AGENT} "USER_AGENT"                                       #matching with the useragent string 
RewriteRule ^(www.soldier.io | soldier | soldier.io)$ /var/www/html/soldier.io/ChiefCommander/index.php [NC]           

RewriteCond %{HTTP_USER_AGENT} !"USER_AGENT"
RewriteRule ^(www.soldier.io|soldier|soldier.io)$ /var/www/html/soldier.io/$USER/index.php [NC]
#save the file



sudo systemctl restart apache2
 

sudo vim /root/createWebpage.sh
                                                  # creates .php files in each directory and adds content

#!/bin/bash


for i in Army{1..50} Navy{1..50} AirForce{1..50} ArmyGeneral NavyMarshal AirForceChief
do
export i                                                  # used to export username across multiple scripts
sudo mkdir /var/www/html/soldier.io/$i                    #creating a directory with each username
sudo chown _R $USER:$USER /var/www/html/soldier.io/$i     # access rights
sudo nano /var/www/html/soldier.io/$i/index.php         

<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>profile</title>
  </head>
  <body>
    <?php
       echo "$i";                                               # printing the username
    ?>
    
  </body>
</html>
#save the file
done


sudo mkdir -p /var/www/html/soldier.io/ChiefCommander                 #making directory for the chiefcommander
sudo nano /var/www/html/soldier.io/ChiefCommander/index.php

<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>attendance report</title>
  </head>
  <body>
    <?php
       $myfile = fopen("/ChiefCommander/attendance_report.txt", "r") ;                   # displaying attendance
       echo fread($myfile,filesize("/ChiefCommander/attendance_report.txt"));
       fclose($myfile);
       
    ?>
    
  </body>
</html>

# save both the files
                              
touch ~/.bashrc                                # save the aliases in .bashrc 
vim ~/.bashrc
alias createWebpage='source /root/createWebpage.sh'
# save and close the file



vim /root/alias.sh
userGenerate
permit
autoSchedule
attendance
record
finalattendance
nearest
createWebpage
#save the file

#task2


sudo mkdir -p /root/dockerfiles
sudo chown -R $USER:$USER /root/dockerfiles
sudo nano /root/dockerfiles/Dockerfile

#into the file
FROM ubuntu:16.04

ADD  ~/.bashrc /root/alias.sh /var/spool/cron/crontabs /root/createWebpage.sh /root/account_create.sh /root/access_permit.sh /root/post_allot.sh /root/attendance_take.sh /root/disp_attendance.sh /root/attendance_update /root/near.sh position.log attendance.log /

#scripts of last week's tasks,alias.sh,~/.bashrc,cronjob file,this week task 1 is added in root directory of docker filesystem

RUN sudo apt-get update                                                                         &&\     
    sudo apt-get install -y apache2                                                                &&\
    sudo systemctl start apache2                                                                &&\
    sudo a2enmod rewrite                                                                        &&\
    sudo systemctl restart apache2                                                                                          # enabling rewrite module

    sudo mkdir -p /var/www/html/soldier.io                                                      &&\                            # making a directory soldier.io
    sudo chown _R $USER:$USER /var/www/html/soldier.io                                          &&\
    sudo chmod -R 750 /var/www/html                                                             &&\
    sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/backup.conf  &&\    #copying the conf file to another file
    sudo nano /etc/apache2/sites-available/backup.conf                                          &&\

    <VirtualHost *:80>
        ServerName soldier.io                                                                            # changing the server name and document root and giving permission
        DocumentRoot /var/www/html/soldier.io
    
        <Directory /var/www/html>
            Options Indexes FollowSymLinks MultiViews
            AllowOverride All
            Require all granted
        </Directory>

   # only modifying this block . . .
    </VirtualHost>                                                                                 
#save the file
    sudo a2dissite 000-default.conf                                                                  &&\
    sudo a2ensite backup.conf                                                                        &&\         #disabling conf file and enabling backup file
    sudo systemctl restart apache2                                                                   &&\

    sudo nano /var/www/html/.htaccess                                                                &&\                           # writing the rewrites in .htaccess file

    RewriteEngine on

    RewriteCond %{HTTP_USER_AGENT} "USER_AGENT"                                       #matching with the useragent string 
    RewriteRule ^(www.soldier.io | soldier | soldier.io)$ /var/www/html/soldier.io/ChiefCommander/index.php [NC]           

    RewriteCond %{HTTP_USER_AGENT} !"USER_AGENT"
    RewriteRule ^(www.soldier.io|soldier|soldier.io)$ /var/www/html/soldier.io/$USER/index.php [NC]
    #save the file



    sudo systemctl restart apache2                                                                   &&\
    sudo chmod +x alias.sh                                                            

ENTRYPOINT ["alias.sh"]
#save the file

docker build -t Sysadbackup /root/dockerfiles


# task 3 hacker mode

sudo mysql -u SysAd -p                                                          
     #type in the password
sudo nano /root/ChiefCommander/soldier_complaints.sql                     #create a sql file

#into the file
CREATE DATABASE complaints;
USE complaints;
CREATE TABLE Hygiene ( id smallint unsigned NOT NULL AUTO_INCREMENT, username varchar(20) not null, complaint varchar(255) not null, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP(), PRIMARY KEY (id) );

#save the file



# task 4 hacker mode 

sudo mkdir -p /var/www/html/complaints.io                                                              # making a directory soldier.io
sudo chown _R $USER:$USER /var/www/html/complaints.io
sudo chmod -R 750 /var/www/html
sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/backup1.conf      #copying the conf file to another file
sudo nano /etc/apache2/sites-available/backup1.conf

<VirtualHost *:80>
    ServerName complaints.io                                                                            # changing the server name and document root and giving permission
    DocumentRoot /var/www/html/complaints.io
    
    <Directory /var/www/html>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Require all granted
    </Directory>

   # only modifying this block . . .
</VirtualHost>
#save the file
sudo a2ensite backup1.conf                                                                                 #disabling conf file and enabling backup file
sudo systemctl restart apache2

sudo nano /var/www/html/.htaccess                                                # writing the rewrites in .htaccess file

RewriteEngine on

RewriteCond %{HTTP_USER_AGENT} "USER_AGENT"                                       #matching with the useragent string 
RewriteRule ^(www.soldier.io | soldier | soldier.io)$ /var/www/html/soldier.io/ChiefCommander/index.php [NC]           

RewriteCond %{HTTP_USER_AGENT} !"USER_AGENT"
RewriteRule ^(www.soldier.io|soldier|soldier.io)$ /var/www/html/soldier.io/$USER/index.php [NC]

RewriteRule ^(www.complaints.io|complaints|complaints.io)$ /var/www/html/complaints.io/complaint.php [NC]

#save the file

sudo nano /root/connect.php

<?php
   $conn = mysqli_connect('complaints.io', 'SysAd', 'password', 'complaints');                                  # creating a file to connect to the database
   if(!$conn)
      echo 'Connection Error: ' . mysqli_connect_error();
?>
#save the file

sudo nano /var/www/complaint.io/complaint.php                                                                   #the php webpage
 
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Complaint</title>
  </head>
  <body>
    
        <form action="complaint.php" method="POST">
                 Username:  <input type="text" name="username"><br>                                      #using post command
                 Complaint: <input type="text" name="complaint"><br>                                     # printing the username
                 <input type="submit">
        </form>
        
        <?php 
             include '/root/complaint.php';
             $User = %{HTTP_USER};
             $Username = $_POST["username"];
             $Complaint = $_POST["complaint"];
             $sql = "INSERT INTO Hygiene VALUES ('$Username', '$Complaint', DEFAULT);
             mysqli_query($conn, $sql);
             echo "your complaint is registered successfully";
        ?>
  </body>
</html>
# save the file


# task 5 hackermode


sudo nano /root/ChiefCommander/reverse.sh                    #script to reverse proxy
 
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_balancer
sudo a2enmod lbmethod_byrequests
sudo systemctl restart apache2

sudo nano /etc/apache2/sites-available/000-default.conf

<VirtualHost *:80>
<Proxy balancer://mycluster>
    BalancerMember http://<IP address>:8080
    BalancerMember http://<IP address>:8081
    #....for all soldiers
</Proxy>

    ProxyPreserveHost On

    ProxyPass / balancer://mycluster/
    ProxyPassReverse / http://complaint.io:3333              #reversing port for all soldiers to por 3333
</VirtualHost>
# save the file
sudo systemctl restart apache2
#save the file

sudo mkdir -p /root/DOCKERFILES
sudo chown -R $USER:$USER /root/DOCKERFILES
sudo nano /root/dockerfiles/Dockerfile

#into the file
FROM ubuntu:16.04

ADD /root/ChiefCommander/soldier_complaints.sql /root/ChiefCommander/reverse.sh  /root         # creating dockerfile
RUN chmod +x /root/ChiefCommander/reverse.sh && /root/ChiefCommander/reverse.sh                #program to run reverseproxy

ENTRYPOINT ["cd", "/root/ChiefCommander/soldier_complaints.sql"]                                 #application for chief to check the complaints
 
#save the file

docker build -t complaint_app /root/DOCKERFILES
docker run --name complaint_application:1.0 -p 3333:80 -p 50000:50000 complaint_app                  # running the container with hostport 3333 connected to container port

# save the file

 