from Tools import tools_v000 as tools
from MyHours import myhours as m
from AzureDevOps import azuredevops as a
import os
from os.path import dirname
import time
import tkinter as tk
from tkinter import messagebox

# False : If you have already start the clock => just update after. => Default value is True
isStartMyHoursNeeded = True

# -8 for the name of this project StartPBI
# save_path = dirname(__file__)[ : -8]
save_path = os.path.dirname(os.path.abspath("__file__"))
propertiesFolder_path = save_path + "/"+ "Properties"

a.save_path = tools.readProperty(propertiesFolder_path, 'StartPBI', 'save_path=')
a.boards = tools.readProperty(propertiesFolder_path, 'StartPBI', 'boards=')
a.pbi = tools.readProperty(propertiesFolder_path, 'StartPBI', 'pbi=')








# Open Browser
tools.openBrowserChrome()

# MyHours part
m.connectToMyTimeTrack()

# afficher une popup expliquant qu'il faut se connecter une première fois
# Et installer l'extension chrome pour retenir les users et password
def show_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Information", "Please connect for the first time and install the Chrome extension to remember the users and passwords.")
    root.destroy()


print ("Test if we need to wait the page of the user / password")
if tools.waitLoadingPageByID2(5, 'email-label') :
    # show_popup()
    # print ("Need to wait the page of the password")
    # tools.waitLoadingPageByID2(10, 'email-label')
    # time.sleep(30)
    m.enterCredentials2()

time.sleep(1)

# Force refresh the page
tools.driver.refresh()

m.startTrack2()






a.connectToAzureDevOpsInsim(a.boards, a.pbi, a.userInsim, a.userInsimPassword)

time.sleep(1)

a.recoverPBIInformation(a.boards)

# # Create folder link to this JIRA
a.createFolderPBI(a.pbi)
a.createFileInto(a.boards, a.pbi, a.pbiTitle, a.description_text, a.pbi, a.pbi + "_Comment_v001")

# # Update MyHours
m.connectToMyTimeTrack()

print ("Test if we need to wait the page of the user / password")
if tools.waitLoadingPageByID2(5, 'email-label') :
    m.enterCredentials2()

time.sleep(1)

# Force refresh the page
tools.driver.refresh()

m.startTrackWithDescription2(a.pbi, a.pbi + ' - ' + a.pbiTitle, a.epic_link)
time.sleep(1)

# # 
tools.openFolder(a.save_path + a.pbi)
tools.openFile(a.save_path + a.pbi + '/' + a.pbi + '_Comment_v001.txt')

# Exit Chrome
tools.driver.quit()