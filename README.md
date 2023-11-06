# Changing-computer-volume-with-hand-movements-computervision

This is a computer vision project that allows the user to adjust their computer audio using their hands (image capture through webcam).
The model that captures the image from the webcam, detects the hands on the image, and draw the circles around the hand's landmarks
were all taken care of with the help of cv2 and mediapipe packages. And to adjust the volume controls it was used the [pycaw]([https://ooiale.github.io/How-Cool-Is-ChatGPT-and-the-importance-of-Prompt-Engineering/](https://github.com/AndreMiras/pycaw)https://github.com/AndreMiras/pycaw) module.

The idea of this project is to detect the tip of the thumb and index fingers on the webcam, then draw a line connecting these two points.
based on how spaced out these two fingers are, the model will adjust the volume of the computer proportionally.
For example, when the two fingers get further away, the volume increases and then they come closer, the volume decreases.

I don't see any convenient uses for this as it is very unreliable and not practical. Nowadays it is even possible to adjust the volume through keyboard keys in some computers
which is quite handful.
However, there are many useful applications of these kind of projects through motion control and this one is just a basic one for starters! 
