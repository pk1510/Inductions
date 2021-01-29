touch /root/account_create.sh                                     # create a file named account_create to create accounts and home directories 
chmod 700 /root/account_create.sh
vi /root/account_create.sh

# Task 1
#!/bin/bash                                           


set -x


function createAccount() {
echo -sp "Password: "
read pass_var
echo 
while [ "$pass_var" == *":"* -o ${#pass_var} -lt 6 ]     # password should be of atleast 6 characters for strength and should not contain ":" symbol as it is the field separator in /etc/passwd file                               
do
echo "Password should not contain \":\" character and it should be of minimum 6 characters"
echo "enter a valid password"
read pass_var
done

useradd -m -p $pass_var $user_var       # user_var is a global variable , -m is used to create home directory
}

if [ "$(id -u)" -eq 0 ]                              # checking for root user 
then
for user_var in ChiefCommander ArmyGeneral NavyMarshal AirForceChief Army{1..50} Navy{1..50} AirForce{1..50}  

do
createAccount
done 

else
echo "Only root may add an user to the system"
exit 0
fi
# save the file

touch /root/access_permit.sh                         # create a file named access_permit to modify access rights 
chmod 700 /root/access_permit.sh
vi /root/access_permit.sh

#Task 2
#!/bin/bash
set -x

function accessPermission() {                              
if [ "$(id -u)" -eq 0 ]                                      # root user can only change groups
then
groupadd Chief_Army                                          # forming three separate groups of ChiefCommander and each troop chiefs
usermod -a -G Chief_Army ChiefCommander                      # -G to change the primary group
usermod -a -G Chief_Army ArmyGeneral

groupadd Chief_Navy
usermod -a -G Chief_Navy ChiefCommander
usermod -a -G Chief_Navy NavyMarshal

groupadd Chief_AirForce 
usermod -a -G Chief_AirForce ChiefCommander
usermod -a -G Chief_AirForce AirForceChief

for i in Army{1..50}
do
chgrp -R Chief_Army /home/$i                        # changing the group ownership of the directory to the corresponding troop chief ,chiefcommander group 
chmod -R 770 /home/$i                               # 770 octal number ensures access to the user as well as the group members which is chiefcommander and the troop chief
done                                                # using -R option to ensure access for all sub directories too

for i in Navy{1..50}
do
chgrp -R Chief_Navy /home/$i
chmod -R 770 /home/$i
done

for i in AirForce{1..50}
do
chgrp -R Chief_AirForce /home/$i
chmod -R 770 /home/$i
done

chgrp -R Chief_Army /home/ArmyGeneral           # similarly we change the group ownership of the troop chief's directory to the group having the corresponding trrop chief
chmod -R 770 /home/ArmyGeneral                  # so here one of the members of the group is the user itself. thus only chief commander has access to this directory other than the user

chgrp -R Chief_Marshal /home/NavyMarshal
chmod -R 770 /home/NavyMarshal

chgrp -R Chief_AirForce /home/AirForceChief
chmod -R 770 /home/AirForceChief

chmod -R 700 /home/ChiefCommander                # 700 octal number for the chief commander's directory ensures access only to the user
else
echo "only root can perform this task"
exit 0
fi
}

accessPermission

#save the file

touch /root/post_allot.sh                       # create a file named post_allot to auto-update the post in each of the troop's file
chmod 700 /root/post_allot.sh
vi /root/post_allot.sh

#Task 3                                              
#!/bin/bash
set -x
if [ "$(id -u)" -eq 0 ]                           # checking for root user
then

for i in Army{1..50} Navy{1..50} AirForce{1..50}
do
if [ -e "/home/$i/post_alloted.txt" ]                 # if the file already exists, then recreating it would erase the data
then 
break                                                 # breaks out of the if  loop
else
touch /home/$i/post_alloted.txt
awk ' BEGIN { printf "%-16s %-24s" , "Date","Post" } ' /home/$i/post_alloted.txt       #creating a file with two columns in each troop member's directory
fi
done

function allotPost() {
cur_date=$(date +"%Y-%m-%d")                             # 
for i in Army{1..50} Navy{1..50} AirForce{1..50}
do

grep "$cur_date"* position.log | awk '{if($2==$i){ printf "%-16s %-12s %-12s" , "$cur_date",$3,$4 }} ' >> /home/$i/post_alloted.txt     # matching the logfile for the current date and storing the name of the troop members in an array indexed with the date. 
                                                                                                                                       # printing the location when the troop member stored in i matches the array
done
}
allotPost
00 00 * * * autoschedule                     # use crontab to schedule it exactly at 12 am


else 
echo "only root can perform this task"
exit 0
fi


#save the file


touch /root/attendance_take.sh             # create a file named attendance_take to auto-update attendance file in troop chief's directory
chmod 700 /root/attendance_take.sh
vi /root/attendance_take.sh

# Task 4                                                        
#!/bin/bash
set -x
if [ "$(id -u)" -eq 0 ]
then

for i in ArmyGeneral NavyMarshal AirForceChief
do
if [ -e "/home/$i/attendance_record.txt" ]    # recreating a file erases data
then
break
else
touch /home/$i/attendance_record.txt
awk ' BEGIN { printf "%-16s %-15s" , "Date","Soldier" } '
fi
done


function takeAttendance() {
now_date=$(date +"%Y-%m-%d")
for i in ArmyGeneral{1..50} NavyMarshal{1..50} AirForceChief{1..50}
do

case $i in 
 *"Army"* )
      file_name='/home/ArmyGeneral/attendance_record.txt' ;;
 *"Navy"* )
      file_name='/home/NavyMarshal/attendance_record.txt' ;;
 *"AirForce"* )
      file_name='/home/AirForceChief/attendance_record.txt ;;
  esac    
grep "$now_date"* attendance.log | awk '/YES/ {if($2==$i){ printf "%-16s %-15s" , "$now_date",$2 }} ' >> $file_name     # grep displays the output as input to awk and awk writes in the file

done



}
takeAttendance
00 06 * * * attendance          # use crontab to auto update

else
echo "only root can perform this task"
exit 0
fi
#save the file

touch /root/disp_attendance.sh             # create a file named disp_attendance to auto-update attendance file in troop chief's directory
chmod 700 /root/disp_attendance.sh
vi /root/disp_attendance.sh


# Task 5                                                     #script run by troop chief as user
#!/bin/bash
set -x


u="$USER"                          # to check who is the current user

function display() {
read com 
if [ "$com" -eq "record[1-7]" ]
then
case $com in
 *"1" )
    date_var=$(date -d "last sunday - 6 days" '%Y-%m-%d') ;;   # stores the date
 *"2" )
    date_var=$(date -d "last sunday - 5 days " '%Y-%m-%d') ;;   
 *"3" )
    date_var=$(date -d "last sunday - 4 days" '%Y-%m-%d') ;;
 *"4" )
    date_var=$(date -d "last sunday - 3 days" '%Y-%m-%d') ;;
 *"5" )
    date_var=$(date -d "last sunday - 2 days" '%Y-%m-%d') ;;
 *"6" )
    date_var=$(date -d "last sunday - 1 day" '%Y-%m-%d') ;;
 *"7" )
    date_var=$(date -d "last sunday" '%Y-%m-%d') ;;
esac
else
exit 0
fi
display
grep "$date_var" /home/$u/attendance_record.txt      # displays the record
}
#save the file

touch /root/attendance_update.sh                     # create a file named attendance_update to update each troop's attendance in chief commander's directory
chmod 700 /root/attendance_update.sh
vi /root/attendance_update.sh



# Hackerrank task 1
#!/bin/bash
set -x
date_now=$(date +"%Y-%m-%d")

if [ "$(id -u)" -eq 0 ]                                      # checking for the root user
then
if [ -e "/home/ChiefCommander/attendance_report.txt" ]
then
break
else 
touch /home/ChiefCommander/attendance_report.txt
awk ' BEGIN { printf "%-16s %-10s %-10s %-14s" , "Date","Army","Navy","AirForce" }
fi

paste /home/ArmyGeneral/attendance_record.txt /home/NavyMarshal/attendance_record.txt /home/AirForceChief/attendance_record.txt | grep "$date_now" | awk ' { print $1,$2,$4,$6 } ' /home/ChiefCommander/attendance_report.txt     # using paste command to paste directly from troop chief's files
else
echo "Only root can create this file"
exit 0
fi
05 06 * * * finalattendance            # auto updation at 6 05 am because at 6 am only the other three files will start updating
#save the file

touch /root/near.sh          # create a file named near to print the nearest 10 army soldiers 
chmod 700 /root/near.sh
vi /root/near.sh

# Hackerrank task 2

#!/bin/bash
set -x

if [ "$(id -u)" -eq 0 ]
then

function calcDistance() {                                   # function to calculate distance using latitude and longitude. note that N and E shld be replaced with + sign
lat1=$(( scale=4;28.7041*3.14/180 )) | bc -l
long1=$(( scale=4;77.1025*3.14/180 )) | bc -l
ind_ex=0
for i in "${lat_loc[@]}"                                       # store all the latitudes in an array
do

long_loc=$( grep *"$i" /root/dummy.txt | awk ' { print $4 } ' )      # get the corresponding longitude
long=$(( scale=4; long1-long_loc )) | bc -l
dist=$(( s(lat1)*s(i) + c(lat1)*c(i)*c(long) )) | bc -l

if [ "$dist" -gt 1 ]
then
dist=1
fi

p=$(( scale=5; sqrt(1-dist*dist)/dist )) | bc -l
dist_final[$ind_ex]=$(( a(dist) )) | bc -l
ind_ex=$(( ind_ex + 1 ))                                    # store corresponding distances in an array
done

grep "$date_present" /root/dummy.txt | awk ' { print $NF=$dist_final } ' /root/dummy.txt     # write the fifth column using the array
}



date_present=$(date +"%Y-%m-%d")
if [ "$(id -u)" -eq 0 ]                               # checking for root user
then
if [ -e "/home/ChiefCommander/nearest10.txt" ]
then 
break
else
touch /root/dummy.txt                                     # create a dummy text file for rough work
awk ' BEGIN { printf "%-10s %-10s %-13s %-13s %-13s" , "Date","armyname","latitude","longitude","Distance" } ' /root/dummy.txt   # create a column called distance 
touch /home/ChiefCommander/nearest10.txt
awk ' BEGIN { printf "%-16s %-12s" , "Date","ArmySoldier" } ' /home/ChiefCommander/nearest10.txt         # create nearest10 file
fi

 
awk 'NR==FNR{a[$1]=$2;next} $2 in a { printf "$date_present" , $2,$3,$4 } ' /home/ArmyGeneral/attendance_record.txt position.log | grep "$date_present"* >> /root/dummy.txt    # get the corresponding post of each army member who was present today
sed -i 's/N°/+/g' /root/dummy.txt             # replace N and E with + to pass the values to the function
sed -i 's/E°/+/g' /root/dummy.txt

count=$( grep "$date_present" /root/dummy.txt | wc -l )
if [ "$count" -le 10 ]                                      # if number of present is less than or equal to ten then they are the nearest 10 soliders
then 
awk ' { print $1,$2 } ' /root/dummy.txt >> /home/ChiefCommander/nearest10.txt
else
lat_loc=$( grep "$date_present" /root/dummy.txt | awk ' { print $3 } ' )         # store the latitude values as an array      
calcDistance 
sort -k5 -n /root/dummy.txt                                  # sort the dummy file wrt to the distance from delhi
grep "$date_present" /root/dummy.txt | awk 'NR==1,NR==10{ print $1,$2 } ' /root/dummy.txt >> /home/ChiefCommander/nearest10.txt   #print the first 10 entries onto the file nearest10 
fi

else
echo "only root can do this task"
exit 0
fi
05 06 * * * nearest            
#save the file


touch ~/.bashrc                                # save the aliases in .bashrc 
vim ~/.bashrc
alias userGenerate='cd /root/account_create.sh'
alias permit='cd /root/access_permit.sh'
alias autoSchedule='cd /root/post_allot.sh'
alias attendance='cd /root/attendance_take.sh'
alias record='cd /root/disp_attendance.sh'
alias finalattendance='cd /root/attendance_update'
alias nearest='cd /root/near.sh'