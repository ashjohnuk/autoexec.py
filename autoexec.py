import xbmc, time, os, xbmcgui, subprocess, stat, shutil

ServerIP = "192.168.1.5" #add server or NAS ip address
ServerUN = "USERNAME" #add remote username
ServerPW = "PASSWORD" #add remote password
ServerFI = ["Downloads","Kodi","Media"] #add remote folder names

def alert(title, msg): 
	dialog = xbmcgui.Dialog()
	dialog.ok(title,msg)

def popup(title, msg):
	dialog = xbmcgui.Dialog()
	dialog.notification(title, msg, xbmcgui.NOTIFICATION_INFO, 5000) #NOTIFICATION_INFO #NOTIFICATION_WARNING #NOTIFICATION_ERROR
	time.sleep(3)

def Epopup(title, msg):
	dialog = xbmcgui.Dialog()
	dialog.notification(title, msg, xbmcgui.NOTIFICATION_ERROR, 5000) #NOTIFICATION_INFO #NOTIFICATION_WARNING #NOTIFICATION_ERROR
	time.sleep(3)

def deleteDefault():
	defaultList = ["/storage/tvshows","/storage/music","/storage/pictures","/storage/screenshots","/storage/videos"]
	for x in defaultList:
		if os.path.isdir(x): os.rmdir(x)

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
	time.sleep(2)
	deleteDefault()
	time.sleep(2)
	mountDrive(ServerFI)
else:
	alert("Unsuccessfull", "Unable to Find Server on "+ServerIP)
	dialog = xbmcgui.Dialog()
	d = dialog.input('Enter IP Address of server', type=xbmcgui.INPUT_IPADDRESS)
