from staticmap import StaticMap, CircleMarker, Line, Polygon
from semic.utils import URL_TILE_PLAN, URL_TILE_SAT

def get_plan(coord, dist, style='plan', width = None, height = None, poly = False):
    """
    Inputs:
        coord: tuple of gps coordinates (longitude, latitude)
        dist: distance to see around the gps coordinates
        style: style of the static map in (plan, sat)
        width: width of the image
        height: height of the image
    Output:
        static map arround the gps coordinates
    """
    if style == 'plan':
        # zoom : [1; 20]
        url_temp = URL_TILE_PLAN
    elif style == 'sat':
        # zoom : [1; 19]
        # bounds: [[-75, -180], [81, 180]]
        url_temp = URL_TILE_SAT
    
    if width == None:
        width = dist
    if height == None:
        height = dist
    
    m = StaticMap(width, height, url_template=url_temp, tile_size = 256)
    if poly:
        for line in coord:
            l = Line(line, 'red', 2)
            m.add_line(l)
    else:
        if any(isinstance(el, (tuple, list)) for el in coord):
            line = Line(coord, 'red', 2)
            m.add_line(line)
        else:
            marker = CircleMarker(coord, 'red', 5)  # longitude, latitude
            m.add_marker(marker)
    image = m.render()
    return image