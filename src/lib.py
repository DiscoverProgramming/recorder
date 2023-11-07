from threading import Thread
import pyautogui
import time
import msvcrt
import cv2
import os
import sys

class lib:
    def __init__(self, delay: float, start_index: int, dir: str, interval: float):
        self.stop = False
        self.allow = True
        self.delay = delay # The delay before taking another screenshot. (Seconds)
        self.index = start_index # The starting index of the image name.
        self.dir = dir # Image Directory Output.
        self.interval = interval # How long to show each frame on video output. (Seconds)

    def get_input(self):
        print("Press the \'S\' key to stop capturing")
        while True:
            if not self.stop:
                if msvcrt.getch().decode('ascii') == 's': # Check if s is pressed, if True, stop the program from capturing.
                    self.stop = True
                    print("Capture Stopped.")
                    self.get_input()
            else:
                print("Press \'C\' to compile and quit the program. Press \'Q\' to quit the program without compiling.")
                if msvcrt.getch().decode('ascii') == 'c': # Check if c is pressed after s, if True, compile all the pictures into a video.
                    self.compile()
                    break
                elif msvcrt.getch().decode('ascii') == 'q': # Check if q is pressed after s, if True, quit the program without compiling.
                    break

    # Function to generate the picture name.

    def get_filename(self) -> int:
        self.index += 1
        return self.index - 1
    
    # Function to run by a thread to wait after each picture is taken.

    def wait(self):
        self.allow = False
        time.sleep(self.delay)
        self.allow = True

    # Function to capture screenshots until stop is True.
        
    def capture(self):
        while True:
            if not self.stop: # Verify that stop is false.
                if self.allow: # If interval wait time is finished, continue
                    pyautogui.screenshot(self.dir + str(self.get_filename()) + '.png') # Take a screenshot.
                    # print('Captured Screenshot-' + str(self.index))
                    Thread(target=self.wait).start() # Create a interval wait time thread before taking another screenshot.
            else: # If stop is True, output "Capture Ended." and stop the function.
                break

    # Function to compile all the screenshots into a video.

    def compile(self):

        print("Compiling... this may take a couple minutes.")

        # Create a list containing all the image directorys.
        images = [img for img in os.listdir(self.dir) if img.endswith(".png")]
        images_int = [int(img.replace('.png', '')) for img in images]
        images_int.sort()

        list = []

        for i in range(len(images)):
            for j in range(len(images)):
                if (str(images_int[i]) + '.png') == images[j]:
                    list.append(images[j])
            
        images = list
        # Create a frame to get the width and height of the screenshot.
        frame = cv2.imread(os.path.join(self.dir, images[0]))
        height, width, layers = frame.shape

        # Create a VideoWriter to compile the images to a video.
        video = cv2.VideoWriter("..\\vid\\video.mp4", 0, 1 / self.interval, (width,height))

        # Run a for loop to iterate through all the images in a list and write them to the file.
        for image in images:
            video.write(cv2.imread(os.path.join(self.dir, image)))

        # Call the destroyAllWindows() function and release() function.

        cv2.destroyAllWindows()
        video.release()

        print("Compilation Completed!")

        # Close the program.

        sys.exit()

    # Main function to run.

    def run(self):
        Thread(target=self.get_input).start()
        Thread(target=self.capture).start()
