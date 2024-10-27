@echo off

echo "Turn on hidden files and folders"
control folders

echo "Enable firewall"
netsh advfirewall set allprofiles state on

echo "Showing all administrators"
net localgroup Administrators

echo "Showing all users (including administrators)"
net users

secedit /export /cfg %TEMP%\local.cfg
START NOTEPAD %TEMP%\local.cfg
secedit /configure /db %windir%\security\local.sdb /cfg %TEMP%\localcfg /areas SECURITYPOLICY

echo "Remove bad programs and features"
appwiz.cpl

echo "Stopping and disabling bad services"
sc stop telnet
sc config telnet start= disabled

sc stop snmptrap
sc config snmptrap start= disabled

sc stop remoteregistry
sc config remoteregistry start= disabled