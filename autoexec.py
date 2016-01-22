import xbmc, time, os, xbmcgui, shutil

ServerIP = xbmcgui.Dialog().input('Enter the IP address of the server', type=xbmcgui.INPUT_IPADDRESS)
ServerUN = xbmcgui.Dialog().input('Enter the username for server', type=xbmcgui.INPUT_ALPHANUM)
ServerPW = xbmcgui.Dialog().input('Enter the password for server', type=xbmcgui.INPUT_ALPHANUM)
ServerFI = ["Downloads","Kodi","Media"]

def alert(title, msg): 
	dialog = xbmcgui.Dialog()
	dialog.ok(title,msg)

def popup(title, msg):
	dialog = xbmcgui.Dialog()
	time.sleep(3)
	dialog.notification(title, msg, xbmcgui.NOTIFICATION_INFO, 5000)
	time.sleep(3)

def Epopup(title, msg):
	dialog = xbmcgui.Dialog()
	time.sleep(3)
	dialog.notification(title, msg, xbmcgui.NOTIFICATION_ERROR, 5000)
	time.sleep(3)

def Wpopup(title, msg):
	dialog = xbmcgui.Dialog()
	time.sleep(3)
	dialog.notification(title, msg, xbmcgui.NOTIFICATION_WARNING, 5000)
	time.sleep(3)

def deleteDefault():
	defaultList = ["/storage/tvshows","/storage/music","/storage/pictures","/storage/screenshots","/storage/videos","/storage/downloads","/storage/emulators","/storage/recordings"]
	for x in defaultList:
		if os.path.isdir(x):
			os.rmdir(x)
			Wpopup("Deleted default folder",x)

def rebootpopup(folder):
	dialog = xbmcgui.Dialog()
	i = dialog.yesno("Network Error","Unable to find \""+folder+"\" on: "+ServerIP+"\nReboot this machine?")
	if i == 1: os.system("reboot now") 

def mountDrive(FOLDERS):
	for x in FOLDERS:
		a = "mount -t cifs -o username="+ServerUN+",password="+ServerPW+" '//"+ServerIP+"/"+x+"' '/storage/"+x+"'"
		if os.path.isdir("/storage/"+x): 
			os.system(a)
			if os.path.ismount("/storage/"+x): 
				popup("Successfully mounted", x)
			else:
				Epopup("Unable to mount", x)
				shutil.rmtree("/storage/"+x)
				rebootpopup(x)
		else:
			os.makedirs("/storage/"+x)
			os.system(a)
			if os.path.ismount("/storage/"+x): 
				popup("Successfully mounted and created", x)
			else:
				Epopup("Unable to mount ", x)
				shutil.rmtree("/storage/"+x)
				rebootpopup(x)


if os.system("ping -c 1 "+ServerIP) == 0:
	deleteDefault()
	mountDrive(ServerFI)
else:
	alert("Unsuccessfull", "Unable to find the server on "+ServerIP)
