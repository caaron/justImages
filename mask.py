import cv2
import numpy as np

from time import sleep

from threading import Timer


class RepeatingTimer(object):
    """
    USAGE:
    from time import sleep
    r = RepeatingTimer(_print, 0.5, "hello")
    r.start(); sleep(2); r.interval = 0.05; sleep(2); r.stop()
    """

    def __init__(self, function, interval, *args, **kwargs):
        super(RepeatingTimer, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.function = function
        self.interval = interval

    def start(self):
        self.callback()

    def stop(self):
        self.interval = False

    def callback(self):
        if self.interval:
            self.function(*self.args, **self.kwargs)
            Timer(self.interval, self.callback, ).start()

class RepeatingTimer(Timer):
    """
    See: https://hg.python.org/cpython/file/2.7/Lib/threading.py#l1079
    """

    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            self.function(*self.args, **self.kwargs)

        self.finished.set()

#print(cv2.__version__)
def mask(image,bitmask):
    overlay = image.copy()
    output = image.copy()

    h, w, c = image.shape
    color = (0, 0, 255)
    rects = []
    rects.append(((0,0), (int(w/2), int(h/2))))
    rects.append(((0,int(h/2)), (int(w/2), h)))
    rects.append(((int(w/2),0), (w, int(h/2))))
    rects.append(((int(w/2),int(h/2)), (w, h)))

    alpha = 1
    for i in range(0,4):
        if int(bitmask) & int(1<<i) != 0:
            p1 = rects[i][0]
            p2 = rects[i][1]
            cv2.rectangle(overlay, p1, p2, color, -1)
    cv2.addWeighted(overlay, alpha, output, 1-alpha, 0, output)
    return output

def show(image):
    cv2.imshow("Output", image)
    cv2.waitKey(10)


def removebitFromMask(mask):
    idx = np.random.randint(0, 4)
    while (1 << idx) & mask == 0:
        idx = np.random.randint(0, 4)
    imask = 0b1111 ^ (1 << idx)
    mask = mask & imask
    return mask

def doNothing():
    pass

def timedReveal(image):
    imgmask = 0b1111
#    start_time = time.time()
    tmr = Timer(1,doNothing)
    tmr.start()
    for i in range(0,4):
        output = mask(image, imgmask)
        show(output)
        sleep(1)
        imgmask = removebitFromMask(imgmask)
        tmr = Timer(1,doNothing)

    cv2.imshow("Output", image)
    cv2.waitKey(0)


if __name__ == "__main__":
    image = cv2.imread("j0.jpg")
#    output = mask(image,0b1100)
#    show(output)
    timedReveal(image)
    print("all done")
