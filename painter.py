from crossroads import Crossroad  # , Segment, Lane


def cr_paint(cr: Crossroad) -> str:
    """
    Создает svg
    :param cr:
    :return: svg
    """
    cr.recalc()
    svg = f'<svg viewBox="{cr.style.viewBox}" xmlns="http://www.w3.org/2000/svg">\n'  # viewBox="0 0 6 4"
    svg += f'<g id="crossroad" transform="rotate({cr.angle} 0 0)">\n'
    # Создаю заголовки слоев
    layers = {"asphalt": "", "marks": "", "rr": "", "lights": "", "availa": "", "names": ""}
    for key, val in layers.items():
        layers[key] += f'<g id="l_{key}">\n'

    # асфальтирую центр перекрестка
    layers["asphalt"] += f'<polygon points="'
    for p in cr.central_area:
        layers["asphalt"] += f'{p.x},{p.y} '
    layers["asphalt"] += f'" fill="{cr.style.asphalt_color}"/>\n'

    for sg in cr.segments:
        y = -sg.width / 2
        x = max(sg.left_intersection, sg.right_intersection)
        x2 = x + cr.style.segments_length

        for key, val in layers.items():
            layers[key] += f'<g transform="rotate({sg.angle} 0 0)">\n'

        layers["asphalt"] += f'<polygon points="' \
                             f'{sg.left_intersection},{y} {x2},{y} {x2},{-y} {sg.right_intersection},{-y}" ' \
                             f'fill="{cr.style.asphalt_color}"/>\n'
        layers["names"] += f'<text x="{x + cr.style.segments_length / 2}" y="0" fill="black" ' \
                           f'font-size="{1}">{sg.street} </text>\n'

        layers["lights"] += f'<g transform="translate({x + 4},{y - 1})">\n'
        if sg.lights.find("m") > -1:
            layers["lights"] += '<circle cx="3" cy="0" r="0.5" fill="green" />' \
                                '<circle cx="2" cy="0" r="0.5" fill="yellow" />' \
                                '<circle cx="1" cy="0" r="0.5" fill="red" />'
        layers["lights"] += '</g>\n'
        layers["marks"] += f'<line x1="{sg.left_intersection}" x2="{x2}" y1="{y}" y2="{y}" ' \
                           f'style="{cr.style.line_style}"/>\n '
        if sg.crosswalk:
            layers["marks"] += f'<line x1="{x + cr.style.crosswalk_margin}" x2="{x + cr.style.crosswalk_margin}" ' \
                               f'y1="{y}" y2="{-y}" ' \
                               f'style="{cr.style.crosswalk_style}"/>\n '

        previous_direction = ""
        for ln in sg.lanes:

            if ln.type == "d":  # разделительная полоса
                y += ln.width / 2
                layers["rr"] += f'<line x1="{x + ln.width / 2}" x2="{x2 - ln.width / 2}" y1="{y}" y2="{y}" ' \
                                f'style="{cr.style.lane_median_strip} stroke-width: {ln.width}"/>\n'
                y += ln.width / 2
                previous_direction = ""
            elif ln.type == "t":  # рельсы
                y += ln.width / 2
                # шпалы
                layers["rr"] += f'<line x1="{x}" x2="{x2}" y1="{y}" y2="{y}" style="{cr.style.rails_sleeper_style} ' \
                                f'stroke-width: {ln.width * cr.style.rails_sleeper_width}"/>\n'
                yg = ln.width * cr.style.rails_gauge / 2
                layers[
                    "rr"] += f'<line x1="{x}" x2="{x2}" y1="{y - yg}" y2="{y - yg}" style="{cr.style.rails_style}"/>\n'
                layers[
                    "rr"] += f'<line x1="{x}" x2="{x2}" y1="{y + yg}" y2="{y + yg}" style="{cr.style.rails_style}"/>\n'
                y += ln.width / 2
                previous_direction = ""
            else:
                if (previous_direction == "o" and ln.direction == "o") or \
                        (previous_direction == "i" and ln.direction == "i"):
                    "прерывистая линия"
                    layers["marks"] += f'<line x1="{x}" x2="{x2}" y1="{y}" y2="{y}" ' \
                                       f'style="{cr.style.line_style} {cr.style.dash_line_style}"/>\n'
                elif (previous_direction == "r" or ln.direction == "r") or \
                        (previous_direction == "i" and ln.direction == "o") or \
                        (previous_direction == "o" and ln.direction == "i"):
                    "двойная сплошная"
                    yg = cr.style.double_line_distance / 2
                    layers["marks"] += f'<line x1="{x}" x2="{x2}" y1="{y - yg}" y2="{y - yg}" ' \
                                       f'style="{cr.style.line_style}"/>\n'
                    layers["marks"] += f'<line x1="{x}" x2="{x2}" y1="{y + yg}" y2="{y + yg}" ' \
                                       f'style="{cr.style.line_style}"/>\n'

                y += ln.width / 2
                #  Стрелки разрешенных направлений
                if ln.direction == "r" or ln.direction == "i":
                    layers["availa"] += f'<g transform="translate({x},{y}) scale(0.16)">'
                    if ln.availa.find("f") > -1:
                        layers["availa"] += '<polygon points="0,0 6,3 6,1 20,1 20,-1 6,-1 6,-3" ' \
                                            'fill="white"/>\n'
                    if ln.availa.find("r") > -1:
                        layers["availa"] += '<polygon points="10,7 13,4 11,4 12,1 20,1 20,-1 11,-1 9,4 7,4" ' \
                                            'fill="white"/>\n'
                    if ln.availa.find("l") > -1:
                        layers["availa"] += '<polygon points="10,-7 13,-4 11,-4 12,-1 20,-1 20,1 11,1 9,-4 7,-4" ' \
                                            'fill="white"/>\n'
                    layers["availa"] += f'</g>\n'
                # svg += f'<line x1="{x}" x2="{x2}" y1="{y}" y2="{y}" style="{cr.style.lane_auto} stroke-width: {ln.width}"/>\n'
                y += ln.width / 2

                previous_direction = ln.direction
        layers["marks"] += f'<line x1="{sg.right_intersection}" x2="{x2}" y1="{y}" y2="{y}" ' \
                           f'style="{cr.style.line_style}"/>\n'
        for key, val in layers.items():
            layers[key] += '</g>\n'
    for key, val in layers.items():
        layers[key] += '</g>\n'
    svg += layers["asphalt"] + layers["marks"] + layers["rr"] + layers["lights"] + layers["availa"] + layers["names"]
    svg += '</g>\n</svg>\n'

    return svg
