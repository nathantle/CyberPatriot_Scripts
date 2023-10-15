@echo off
echo "Showing list of admins"
net localgroup "Administrators"

echo "Showing list of users"
net users

echo echo on > %UserProfile%\Desktop\eatUsers.bat
echo net user user1 Cyb3rP@triot24$ >> %UserProfile%\Desktop\eatUsers.bat
echo net user user2 Cyb3rP@triot24$ >> %UserProfile%\Desktop\eatUsers.bat
echo net user user3 Cyb3rP@triot24$ >> %UserProfile%\Desktop\eatUsers.bat
echo net user user4 Cyb3rP@triot24$ >> %UserProfile%\Desktop\eatUsers.bat
echo net user user5 Cyb3rP@triot24$ >> %UserProfile%\Desktop\eatUsers.bat
echo net user user6 /delete >> %UserProfile%\Desktop\eatUsers.bat
echo net user user6 /delete >> %UserProfile%\Desktop\eatUsers.bat
echo net user user7 /delete >> %UserProfile%\Desktop\eatUsers.bat
echo net user user8 /delete >> %UserProfile%\Desktop\eatUsers.bat
echo net user user9 /delete >> %UserProfile%\Desktop\eatUsers.bat
echo net user user10 /delete >> %UserProfile%\Desktop\eatUsers.bat

echo rem >> %UserProfile%\Desktop\eatUsers.bat
echo.
notepad %UserProfile%\Desktop\eatUsers.bat

echo.
pause

call %UserProfile%\Desktop\eatUsers.bat

@echo off
pause cls

secedit /export /cfg %TEMP%\local.cfg > nul
echo.
echo Use NOTEPAD to edit the security file.
echo Look for and change the following lines.
echo DO NOT close NOTEPAD until instructed.
echo.
echo MinimumPasswordAge     --- Change to 1
@START NOTEPAD %TEMP%\local.cfg
@rem pause
echo MaximumPasswordAge     --- Change to 90
@rem pause
echo MinimumPasswordLength  --- Change to 8
@rem pause
echo PasswordComplexity     --- Change to 1
@rem pause
echo PasswordHistorySize    --- Change to 5
@rem pause
echo LockoutBadCount        --- Change to 10
@rem pause
echo EnableGuestAccount     --- Change to 0
@rem pause
echo.
echo Audit Policy settings are 1 for success, 2 for failure, 3 for both
echo AuditSystemEvents      --- Change to 3
@rem pause
echo AuditLogonEvents       --- Change to 2
@rem pause
echo AuditObjectAccess      --- Change to 3
@rem pause
echo AuditPrivilegeUse      --- Change to 3
@rem pause
echo AuditPolicyChange      --- Change to 3
@rem pause
echo AuditAccountManage     --- Change to 3
@rem pause
echo AuditProcessTracking   --- Change to 3
@rem pause
echo AuditDSAccess          --- Change to 3
@rem pause
echo AuditAccountLogon      --- Change to 2
@rem pause
echo MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\DisableCAD      --- Change to 4,0
pause
echo.
echo Now save your changes and exit (File/Save, File/Exit)
pause
echo.
echo Applying your changes
secedit /configure /db %windir%\security\local.sdb /cfg %TEMP%\local.cfg /areas SECURITYPOLICY
echo Changes applied
@START NOTEPAD %windir%\security\logs\scesrv.log
pause
cls