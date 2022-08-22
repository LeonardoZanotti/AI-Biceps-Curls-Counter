import cv2 as cv
import logging

logger = logging.getLogger('ftpuploader')
logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

class Camera:

    def __init__(self):
        try:
            self.camera = cv.VideoCapture(0)
            self.camera.open('https://192.168.0.7:8080/video')  # IP Webcam app on PlayStore
            if not self.camera.isOpened:
                raise ValueError("Camera not found!")
        except Exception as e:
            logger.error(f"An exception occurred: {e}")
            exit(400)

        self.width = self.camera.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera.get(cv.CAP_PROP_FRAME_HEIGHT) // 1.5
        logger.info(f"Camera started with dimensions: {self.width, self.height}",)

    def __del__(self):
        if self.camera.isOpened:
            self.camera.release()

    def get_frame(self):
        if self.camera.isOpened:
            ret, frame = self.camera.read()

            if ret:
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return None
