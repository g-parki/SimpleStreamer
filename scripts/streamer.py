from cv2 import cv2
import os

class Streamer:
    """Class for serving stream either through generator or through local window"""

    CAMERA_DEFAULT= 2 #change depending on camera needs

    def __init__(self, camera: int = None):
        _camera_num = camera if camera is not None else Streamer.CAMERA_DEFAULT
        self.cap = cv2.VideoCapture(_camera_num)
        #self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc("m", "j", "p", "g"))
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc("M", "J", "P", "G"))
    
    def _use_camera(self) -> None:
        if self.cap.isOpened():
            self._read_frame()
            self.frame_en = cv2.imencode('.jpg', cv2.resize(self.frame, (720,405)))[1].tobytes()
        else:
            raise Exception("Camera not available.")

    def _read_frame(self) -> None:
        self.ret, self.frame = self.cap.read()
        if not self.ret:
            raise Exception("Frame not available.")

    def _unavailable(self):
        unavailable_img = cv2.imread(os.path.join(os.getcwd(), "scripts", "static", "unavailable.png"))
        unavailable_img_en = cv2.imencode('.jpg', unavailable_img)[1].tobytes()
        return (self._http_encoded(unavailable_img_en))
    
    def _http_encoded(self, frame):
        return (
            b'--frame\r\n'  
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )

    def next_frame(self):
        try:
            self._use_camera()
            return self._http_encoded(self.frame_en)
        except:
            print("Returned unavailable image.")
            return self._unavailable()
            
    def http_generate(self):
        """Yields image for streaming consumption"""
        while True:
            try:
                self._use_camera()
            except:
                yield self._unavailable()
                print("Returned unavailable image.")
                break

            self.key = cv2.waitKey(5) & 0xFF

            yield self._http_encoded(self.frame_en)
    
    def run_local_display(self):
        """Serves stream for local display in CV2 window"""

        window_name = 'Monitor'
        while True:
            if self.cap.isOpened():
                self._read_frame()
            else:
                raise Exception("Camera is not available")
            
            cv2.imshow(window_name, self.frame)

            self.key = cv2.waitKey(20) & 0xFF
            # Close window
            if (self.key == ord('q')) or \
                cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
        self.cap.release()
        return None

if __name__ == '__main__':
    local_stream = Streamer().run_local_display()