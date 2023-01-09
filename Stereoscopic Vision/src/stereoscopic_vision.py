from camera import Camera

class StereoscopicVision:
    def __init__(self, cam1: Camera, cam2: Camera) -> None:
        self.cam1 = cam1
        self.cam2 = cam2 

    def run(self):
        self.cam1.run()
        self.cam2.run()