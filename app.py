import tkinter as tk
import os
import PIL.Image, PIL.ImageTk
import cv2 as cv
import camera

class App:

    def __init__(self):
        self.canvas = None
        self.btn_toggleauto = None
        self.btn_class_one = None
        self.btn_class_two = None
        self.btn_train = None
        self.btn_reset = None
        self.counter_label = None
        self.model = None

        self.window = tk.Tk()
        self.window.title = "Biceps Curl Counter"

        self.counters = [1, 1]
        self.rep_counter = 0

        self.extended = False
        self.contracted = False
        self.last_prediction = 0

        self.counting_enabled = False

        self.camera = camera.Camera()

        self.init_gui()

        self.delay = 15
        self.update()

        self.window.attributes("-topmost", True)
        self.window.mainloop()

    def ini_gui(self):
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        self.btn_toggleauto = tk.Button(self.window, text="Toggle counting", width=50, command=self.counting_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_one = tk.Button(self.window, text="Extended", width=50, command=lambda: self.save_for_class(1))
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_two = tk.Button(self.window, text="Contracted", width=50, command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

        self.btn_train = tk.Button(self.window, text="Train model", width=50, command=lambda: self.model.train_model(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_reset = tk.Button(self.window, text="Reset", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)

        self.counter_label = tk.Label(self.window, text=f"{self.rep_counter}")
        self.counter_label.config(font=("Arial", 24))
        self.counter_label.pack(anchor=tk.CENTER, expand=True)

    def update(self):
        pass

    def predict(self):
        pass

    def counting_toggle(self):
        self.counting_enabled = not self.counting_enabled

    def save_for_class(self, class_number: int):
        ret, frame = self.camera.get_frame()

        if not os.path.exists("1"):
            os.mkdir("1")
        if not os.path.exists("2"):
            os.mkdir("2")

        img_path = f"{class_number}/frame{self.counters[class_number - 1]}.jpg"
        cv.imwrite(img_path, cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
        img = PIL.Image.open(img_path)
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save(img_path)

        self.counters[class_number - 1] += 1

    def reset(self):
        self.rep_counter = 0
