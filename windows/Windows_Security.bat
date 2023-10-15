@echo off
echo "This should only have valid administrators"
net localgroup "Administrators"

echo "This should only have valid users"
net users

echo echo on > %UserProfile%\Desktop\_setpasswords.bat
echo net user username1 Cyb3rP@triot >> %UserProfile%\Desktop\_setpasswords.bat
echo net user username2 Cyb3rP@triot >> %UserProfile%\Desktop\_setpasswords.bat
echo net user username3 Cyb3rP@triot >> %UserProfile%\Desktop\_setpasswords.bat
echo net user username4 Cyb3rP@triot >> %UserProfile%\Desktop\_setpasswords.bat
echo net user username5 Cyb3rP@triot >> %UserProfile%\Desktop\_setpasswords.bat
echo net user username6 Cyb3rP@triot >> %UserProfile%\Desktop\_setpasswords.bat
echo net user username7 Cyb3rP@triot >> %UserProfile%\Desktop\_setpasswords.bat
echo net user username8 Cyb3rP@triot >> %UserProfile%\Desktop\_setpasswords.bat
echo net user username9 Cyb3rP@triot >> %UserProfile%\Desktop\_setpasswords.bat
echo net user username10 Cyb3rP@triot >> %UserProfile%\Desktop\_setpasswords.bat
echo rem >> %UserProfile%\Desktop\_setpassword.bat

echo "This should only have valid administrators"
net localgroup "Administrators"

echo "This should only have valid users"
net users

echo echo on > %UserProfile%\Desktop\_delUsers.bat
echo net user username11 /delete >> %UserProfile%\Destkop\_delUsers.bat
echo net user username12 /delete >> %UserProfile%\Destkop\_delUsers.bat
echo net user username13 /delete >> %UserProfile%\Destkop\_delUsers.bat
echo net user username14 /delete >> %UserProfile%\Destkop\_delUsers.bat
echo pause >> %UserProfile%\Desktop\_setpasswords.bat

notepad %UserProfile%\Desktop\_setPasswords.bat
echo.
pause
call %UserProfile%\Desktop\_setpasswords.bat
call %userProfile%\Desktop\_delUsers.bat
