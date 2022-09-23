
class lane:
    width = 0  #
    type = "a"  # a d t
    direction = "in"  # in out rev
    availa = ()
    light = 0
    stop = 0


class segment:
    lanes = []
    crosswalk = 0
    lights = ()
    street = ""


class crossroad:
    segments = []
