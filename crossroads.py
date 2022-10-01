from shapely.geometry import Point, LineString
from shapely import affinity


class Lane:
    """
    Полоса сегмента перекрестка
    """
    width = 0  #
    type = "a"  # a d t
    direction = "in"  # in out rev
    availa = ""
    light = ""
    stop = 0


class Segment:
    """
    Сегмент перекрестка содержит полосы, светофоры
    """
    lanes = []
    crosswalk = 0
    lights = ""
    street = ""
    angle = 0

    width = 0
    left_intersection = 0
    right_intersection = 0

    def calc_width(self):
        """
        Пересчитывает ширину сегмента = сумма ширины полос

        :return: None
        """
        width = 0
        for ln in self.lanes:
            width += ln.width
        self.width = width

    def calc_cusp(self, sg2):
        """
        Вычисляет точку пересечения сегментов

        :param Segment sg2: Второй Сегмент
        :return: Point
        """
        o1 = self.width / 2
        bl1 = LineString([(-10, o1), (100, o1)])
        bl1 = affinity.rotate(bl1, self.angle, (0, 0))
        bl2 = LineString([(-10, -sg2.width / 2), (100, -sg2.width / 2)])
        bl2 = affinity.rotate(bl2, sg2.angle, (0, 0))
        ip = bl1.intersection(bl2)
        self.right_intersection = affinity.rotate(ip, -self.angle, (0, 0)).x
        sg2.left_intersection = affinity.rotate(ip, -sg2.angle, (0, 0)).x
        return ip


class CrosroadStyle:
    """
    Задает параметры отображения перекрестка
    """
    viewBox="-30 -30 60 60"
    segments_length = 20
#    lane_auto = "stroke: #000000;"
    asphalt_color = "darkgray"
    lane_median_strip = "stroke: #006600; stroke-linecap: round;"
    double_line_distance = 0.2
    line_style = "stroke: #ffffff; stroke-width: 0.1;"
    dash_line_style = "stroke-dasharray: 0.7 0.3;"
    rails_sleeper_width = 0.9  # Длина шпалы - Доля ширины полосы
    rails_gauge = 0.6  # Расстояние между рельсами - Доля ширины полосы
    rails_sleeper_style = "stroke: brown; stroke-dasharray: 0.2 0.5;"
    rails_style = "stroke: gray; stroke-width: 0.2;"
    crosswalk_margin= 5
    crosswalk_style="stroke: white; stroke-width: 3; stroke-dasharray: 0.5 0.5;"

"""    rails_color = -1
    median_strip_color = 255
    background_color = 255
"""

class Crossroad:
    """
    Класс определения перекрестка
    Содержит список сегментов и стили
    """
    segments = []
    style = CrosroadStyle()
    central_area=[]
    angle=0

    def recalc(self):
        sgs=self.segments
        sgs.sort(key=lambda x: x.angle)
        for sg in sgs: sg.calc_width()
        self.central_area=[]
        for i in range(len(sgs)):
            self.central_area.append(sgs[i].calc_cusp(sgs[0 if i == len(sgs) - 1 else i + 1]))
