# encoding: utf-8


class Blackground:
    def __init__(self, pix_x, pix_y, width, height):
        self.width = width
        self.pix_y = pix_y
        self.pix_x = pix_x
        self.height = height

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        frame_thickness = 2
        frame_color = (255, 255, 255)

        screen.draw_frame(frame_color, self.pix_x, self.pix_y, self.width, self.height, frame_thickness)
