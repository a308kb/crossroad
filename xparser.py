import crossroads
from bs4 import BeautifulSoup as Soup
import lxml


def parse(xml: str) -> crossroads.Crossroad:
    cr = crossroads.Crossroad()
    s = Soup(xml, "xml")
    root = s.crossroad
    cr.angle=float(root.get("angle", 0))
    if not root:
        return cr
    cr.segments = []
    for xsg in root.children:
        if xsg.name == "segment":
            sg = crossroads.Segment()
            sg.street = xsg.get("street", "")
            sg.crosswalk = xsg.get("crosswalk", "")
            sg.angle = float(xsg.get("angle", 0))
            sg.lights = xsg.get("lights", "")
            sg.lanes = []
            for xln in xsg.children:
                if xln.name == "lane":
                    ln = crossroads.Lane()
                    ln.type = xln.get("type", "a")
                    ln.light = xln.get("light", "")
                    ln.stop = xln.get("stop", "")
                    ln.width = float(xln.get("width", 3))
                    ln.availa = xln.get("availa", "")
                    ln.direction = xln.get("direction", "i")
                    sg.lanes.append(ln)
            cr.segments.append(sg)
    return cr
