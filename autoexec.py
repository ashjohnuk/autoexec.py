import xbmc, time, os, xbmcgui, shutil

ServerIP = "192.168.1.5" #xbmcgui.Dialog().input('Enter the IP address of the server', type=xbmcgui.INPUT_IPADDRESS)
ServerUN = "USERNAME" #xbmcgui.Dialog().input('Enter the username for server', type=xbmcgui.INPUT_ALPHANUM)
ServerPW = "PASSWORD" #xbmcgui.Dialog().input('Enter the password for server', type=xbmcgui.INPUT_ALPHANUM)
ServerFI = ["Downloads","Kodi","Media"] # Add remote folders here

'''
Start of functions
'''
def alert(title, msg): 
	dialog = xbmcgui.Dialog()
	dialog.ok(title,msg)

def popup(title, msg):
	dialog = xbmcgui.Dialog()
	dialog.notification(title, msg, xbmcgui.NOTIFICATION_INFO, 3000)
	
def Epopup(title, msg):
	dialog = xbmcgui.Dialog()
	dialog.notification(title, msg, xbmcgui.NOTIFICATION_ERROR, 3000)
	
def Wpopup(title, msg):
	dialog = xbmcgui.Dialog()
	dialog.notification(title, msg, xbmcgui.NOTIFICATION_WARNING, 3000)
	
def deleteDefault():
	defaultList = ["/storage/tvshows","/storage/music","/storage/pictures","/storage/screenshots","/storage/videos","/storage/downloads","/storage/emulators","/storage/recordings"]
	for x in defaultList:
		if os.path.isdir(x):
			os.rmdir(x)
			Wpopup("Deleted default folder",x)

def rebootpopup(folder):
	dialog = xbmcgui.Dialog()
	i = dialog.yesno("Network Error","Unable to find \""+folder+"\" on: "+ServerIP+"\nRestart Kodi?")
	if i == 1:
		xbmc.executebuiltin( " RestartApp " )
		exit(0)

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

def ReloadKodiSkin():
	time.sleep(6)
	xbmc.executebuiltin( " ReloadSkin() " )
	dialog = xbmcgui.Dialog()
	dialog.notification("Kodi Skin","Refreshed", xbmcgui.NOTIFICATION_INFO, 2000)

def runScript():
	deleteDefault()
	time.sleep(3)
	mountDrive(ServerFI)
	time.sleep(3)
	ReloadKodiSkin()	
'''
End of functions
'''
xbmcgui.Dialog().notification("Kodi network mount", "Loading...", xbmcgui.NOTIFICATION_INFO, 10000)

while not os.system("ping -c 1 "+ServerIP) == 0:
	time.sleep(3)
else:
	runScript()
	exit(0)
