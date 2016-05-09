# encoding: utf-8


class Blackground:
    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        offset_x = 50
        offset_y = 50
        frame_color = 255, 255, 255
        width, height = screen.get_size()
        frame_thickness = 2

        screen.draw_frame(frame_color, offset_x, offset_y, width - 2 * offset_x, height - 2 * offset_y, frame_thickness)
