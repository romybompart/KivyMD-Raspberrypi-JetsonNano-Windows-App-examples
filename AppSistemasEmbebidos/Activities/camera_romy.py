from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import face_recognition
import pickle

class KivyCamera(Image):

    event = None
    HAAR_CASCADE_XML_FILE_FACE = "haarcascade_frontalface_default.xml"
    ENCODING_PICKLE = "encodings.pickle"

    def __init__(self, capture, fps=60, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.start(fps)
        self.data = pickle.loads(open(self.ENCODING_PICKLE,"rb").read())
        self.face_cascade = cv2.CascadeClassifier(self.HAAR_CASCADE_XML_FILE_FACE)
        self._mode = True

    def mode(self, value):
         self._mode = value
    
    def start(self, fps):
       self.event = Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        self.event.cancel()

    def update(self, dt):
        ret, image = self.capture.read()
        if ret:

            grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            detected_faces = self.face_cascade.detectMultiScale(grayscale_image, 1.3, 5)

            if self._mode:
                for (x_pos, y_pos, width, height) in detected_faces:
                    cv2.rectangle(image, (x_pos, y_pos), (x_pos + width, y_pos + height), (80, 224, 51), 2)
            else:
                boxes = [(y, x + w, y + h, x) for (x, y, w, h) in detected_faces]
                encodings = face_recognition.face_encodings(image, boxes)
                names = []

                for encoding in encodings:
                    # attempt to match each face in the input image to our known
                    # encodings
                    matches = face_recognition.compare_faces(self.data["encodings"],
                        encoding)
                    name = "Unknown"

                    # check to see if we have found a match
                    if True in matches:
                        # find the indexes of all matched faces then initialize a
                        # dictionary to count the total number of times each face
                        # was matched
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}

                        # loop over the matched indexes and maintain a count for
                        # each recognized face face
                        for i in matchedIdxs:
                            name = self.data["names"][i]
                            counts[name] = counts.get(name, 0) + 1

                        # determine the recognized face with the largest number
                        # of votes (note: in the event of an unlikely tie Python
                        # will select first entry in the dictionary)
                        name = max(counts, key=counts.get)

                    # update the list of names
                    names.append(name)

                # loop over the recognized faces
                for ((top, right, bottom, left), name) in zip(boxes, names):
                    # draw the predicted face name on the image
                    cv2.rectangle(image, (left, top), (right, bottom),
                        (80, 224, 51), 2)
                    y = top - 15 if top - 15 > 15 else top + 15
                    cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (80, 224, 51), 2)


            # convert it to texture
            buf1 = cv2.flip(image, 0)
            # buf = buf1.tostring()
            buf = buf1.tobytes() 
            image_texture = Texture.create(
                size=(image.shape[1], image.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()