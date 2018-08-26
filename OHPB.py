#libraries
from gpiozero import Button
from picamera import PiCamera
from time import gmtime, strftime, sleep
##this will allow us to use all of the overlay functions defined in the overlay_functions.py file from within our allseeingpi.py file
from overlay_functions import *
##this gives the resources to make a gui
from guizero import App, PushButton, Text, Picture
#pulling in watermark functions
#from add_WM import recent
import os
#functions for the commands to execute
def next_overlay():
    global overlay
    overlay = next(all_overlays)
    preview_overlay(camera, overlay)
##function explination for overlay
##First, we have to declare that we want to use the global variable, overlay. This means that when we change the overlay, that value is saved so that we can access it
##and use it from anywhere, and the change isn’t lost when we exit this function. The second line gets the next overlay from the list of all_overlays
##(defined within the overlay_functions.py file), and sets this as the current overlay. Then, the function preview_overlay() is called to display the new overlay.

##new
def wm(input_image_path,
                    output_image_path,
                    watermark_image_path,
                    position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    width, height = base_image.size
 
    transparent = Image.new('RGBA', (width, height), (0,0,0,0))
    transparent.paste(base_image, (0,0))
    transparent.paste(watermark, position, mask=watermark)
    transparent.show()
    transparent.save(output_image_path)

def take_picture():
    #added to prevent overwritting previous picture
    global output
    #gmtime() and no %S
    #modified to fit the needs of OHPB 8/25/18
    #the "~" allows for the home directory of the current user and if the folder_creation.sh file was run, the previous directories should be there.
    output = strftime("~Documents/OHPB/images/image-%d-%m %H:%M:%S.png",)
    #this is an example of "scoping"
    #if we only created it within the take_picture() function, once the function finished executing, the variable would no longer exist.
    #By declaring that we are talking about the global version of the output variable, we are telling the program that we want to use the variable output which we created
    #in the main part of the program. This means that once the function exits, the variable output with the location of the saved picture will still exist.
    #We need to have a permanent record where the picture was saved because it is used in other places within the program.
    
    ##this was added to include a count down due to having to push a buttong that could easily take you out of the overlay. Ability to have the count down came from
    ##https://www.meccanismocomplesso.org/en/picamera-python-aggiungiamo-testi-sulle-immagini-e-video/ and was added on 8/24/18
    camera.annotate_text_size = 160
    sleep(1)
    camera.annotate_text= "3"
    sleep(1)
    camera.annotate_text= "2"
    sleep(1)
    camera.annotate_text= "1"
    sleep(1)
    camera.annotate_text = ""
    ##
    camera.capture(output)
    camera.stop_preview()
    remove_overlays(camera)         # Added to remove the overlay
    output_overlay(output, overlay) # Merges the photo and the overlay
    
    ##This was added on 8/21 from using code found on Stack Overflow https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder-using-python/39327156
    filepath = '~/Documents/OHPB/images'
    files = sorted([
        f for f in os.listdir(filepath) if f.startswith('image')])

    recent = files[-1]
    print (recent)
    
    ##MODIFIED ON 8/25 TO WORK WITH AUTO CONFIG
    ##this comes from the code I created in Atlanta during Picademy. The ".format" was an idea I got from Matt Buckley (@MrBuckley98) but instead of using a numbering system
    ##I am pulling in the identical name of the newly created file. I also made variables for the file paths which is unnecessary but oh well.
    base = '~/Documents/OHPB/images/{}'.format(recent)
    destination = '~/Documents/OHPB/wm/{}'.format(recent)
    wm(base, destination, '~/Documents/OHPB/wm/REPLACE_WITH_YOUR_FILENAME.png', position=(0,0))
    
    
    #added to put in latest gif option for GUI
    size = 400, 480
    gif_img = Image.open(output)
    gif_img.thumbnail(size, Image.ANTIALIAS)
    gif_img.save(latest_photo, 'gif')
    your_pic.set(latest_photo)

##added to put items in the GUI
def new_picture():
    camera.start_preview(alpha=128)
    preview_overlay(camera, overlay)

#This was used to test buttons before the actual take a picture function was written
##def next_overlay():
##    print("Next overlay")
##def take_picture():
##    print("Take a picture")

#naming and assigning buttons
next_overlay_btn = Button(23)
take_pic_btn = Button(25)
#code for picture naming conventions, gmtime was after the comma but to get local time, you can just delete it and it will take the time from the pi
#might need to add in seconds due to multiple pictures being taken in a minute? The main parts referenced above were removed and added to the fucntion as instructed.
#the "" is now in reference to the global output
output =""
##Modified on 8/25/18 to work with auto config
latest_photo = '~/Documents/OHPB/gifs/latest.gif'


#assiging commands to buttons
next_overlay_btn.when_pressed = next_overlay
take_pic_btn.when_pressed = take_picture

#addition of camera fetures
camera = PiCamera()
#used HD resolution but can be turned down if needed (800 x 480), created overlays MUST MATCH CAMERA RESOLUTION! (1920x1080
camera.resolution = (800, 480)
#unmirrors the image to make alignment with overlays better
camera.hflip = True
#comment this out to remove transparancy
#camera.start_preview(alpha=255)

#gui creation
##app: tells the button to add itself to the app.
##new_picture: this is the command. When the button is pushed, it will call the function new_picture() (which we haven’t written yet!)
##text="New picture": this is the text which will appear on the button

## Modified on 8/25/18 replace with revelant information
app = App("School Name or Mascot's Open House", 800, 480)
message = Text(app, "Welcome Back!")
your_pic = Picture(app, latest_photo)
new_pic = PushButton(app, new_picture, text="New picture")
app.display()



    
##EXTRA STUFF
##You can make your own overlays, or use the ready-made ones we have provided for you to download.
##If you are creating your own overlays, make sure that they are saved at 800 × 480 resolution as PNG files, with the background set to transparent.



