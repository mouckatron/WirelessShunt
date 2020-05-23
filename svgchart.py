import math

class SVGChart:

    _X_GRID_OFFSET = 20
    _Y_GRID_OFFSET = 30

    def __init__(self, data, size=(100,100), show_zero=False):
        self.size = size
        self.stroke_color = '#0074d9'
        self.stroke_width = '1'
        self.data = data
        self.show_zero = show_zero
        self.__x_spacing = 1
        self.__y_spacing = 1
        self.__max_point = 1
        self.__min_point = 0

    def get_points(self):
        points = []

        self.__max_point = max(self.data)
        self.__min_point = min(self.data)

        if self.show_zero:
            if self.__max_point < 0.0:
                self.__max_point = 0.0
            elif self.__min_point > 0.0:
                self.__min_point = 0.0

        self.__x_spacing = math.floor(self.size[0] / len(self.data))
        self.__y_spacing = self.size[1] / (self.__max_point - self.__min_point)

        print("max_point: %s", self.__max_point)
        print("min_point: %s", self.__min_point)
        print("x_spacing: %s", self.__x_spacing)
        print("y_spacing: %s", self.__y_spacing)

        x = SVGChart._X_GRID_OFFSET
        for y in self.data:
            points.append(
                '{},{}'.format(x, ((self.__max_point - y) * self.__y_spacing)))
            x += self.__x_spacing

        return ' '.join(points)

    def _get_x_labels(self):
        spacing = (len(self.data) / 4) * self.__x_spacing
        return '''<text x="{}" y="{y_pos}">-60</text>
  <text x="{}" y="{y_pos}">-45</text>
  <text x="{}" y="{y_pos}">-30</text>
  <text x="{}" y="{y_pos}">-15</text>
  <text x="{}" y="{y_pos}">now</text>
'''.format(SVGChart._X_GRID_OFFSET - 5,
           SVGChart._X_GRID_OFFSET + spacing - 5,
           SVGChart._X_GRID_OFFSET + (spacing *2) - 5,
           SVGChart._X_GRID_OFFSET + (spacing *3) - 5,
           SVGChart._X_GRID_OFFSET + (spacing *4) - 5,
           y_pos=self.size[1] + (SVGChart._Y_GRID_OFFSET / 2))

    def _get_y_labels(self):
        multiplier = 5 / (self.__max_point - self.__min_point)
        lines = []
        # for x in range(5):
        #     lines.append('<text x="{x_pos}" y="">{}</text>'.format((self.__min_point * multiplier), x_pos=(SVGChart._Y_GRID_OFFSET / 2)))
        lines.append('<text x="{x_pos}" y="0">{}</text>'.format(self.__max_point, x_pos=(SVGChart._Y_GRID_OFFSET / 2)))
        lines.append('<text x="{x_pos}" y="{draw_height}">{}</text>'.format(self.__min_point, x_pos=(SVGChart._Y_GRID_OFFSET / 2), draw_height=self.size[1]))

        return ''.join(lines)

    def __str__(self):
        return '''<svg viewBox="0 0 {width} {height}">
<g style="stroke:#ccc;stroke-dasharray:0;stroke-width:1;">
  <line x1="{x_offset}" y1="0" x2="{x_offset}" y2="{draw_height}"></line>
</g>
<g style="stroke:#ccc;stroke-dasharray:0;stroke-width:1;">
  <line x1="{x_offset}" x2="{width}" y1="{draw_height}" y2="{draw_height}"></line>
</g>
  <g class="labels x-labels">
{x_labels}
</g>
<g class="labels y-labels">
{y_labels}
</g>
<polyline fill="none" stroke="{stroke_color}" stroke-width="{stroke_width}" points="{points}"/></svg>'''.format(
                 width=(SVGChart._X_GRID_OFFSET + self.size[0]),
                 height=(SVGChart._Y_GRID_OFFSET + self.size[1]),
                 x_offset=SVGChart._X_GRID_OFFSET,
                 draw_width=self.size[0],
                 draw_height=self.size[1],
                 stroke_color=self.stroke_color,
                 stroke_width=self.stroke_width,
                 points=self.get_points(),
                 x_labels=self._get_x_labels(),
                 y_labels=self._get_y_labels())
