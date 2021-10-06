import math


def manhatten_dist(start, end):
    # manhatten distance
    return start[0]-end[0] + start[1]-end[1]

def get_length(start, end):
    # actual pythagorian distance
    return math.hypot(end[0] - start[0],
                      end[1] - start[1])

def points_are_counterclockwise(a, b, c):
    return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])

def do_lines_intersect(a, b, c, d):
    # Return true if line segments AB and CD intersect
    ccw = points_are_counterclockwise
    return ccw(a,c,d) != ccw(b,c,d) and ccw(a,b,c) != ccw(a,b,d)

def get_intersecting_lines(ray_start, ray_end, lines):
    return [l for l in lines
            if do_lines_intersect(ray_start, ray_end, *l)]

def blocked_ray_end(ray_start, ray_end, block_start, block_end):
    # Intersection point of line segments

    def coef(p1, p2):
        a = (p1[1] - p2[1])
        b = (p2[0] - p1[0])
        c = (p1[0]*p2[1] - p2[0]*p1[1])
        return a, b, -c

    L1, L2 = coef(ray_start, ray_end), coef(block_start, block_end)
    d  = L1[0] * L2[1] - L1[1] * L2[0]
    dx = L1[2] * L2[1] - L1[1] * L2[2]
    dy = L1[0] * L2[2] - L1[2] * L2[0]
    if d != 0:
        x = dx / d
        y = dy / d
        return int(x), int(y)
    else:
        return ray_end

def get_intersections(ray_start, ray_end, lines, check_intersection = True):
    if check_intersection:
        lines = get_intersecting_lines(ray_start, ray_end, lines)
    
    return [(ray_start, blocked_ray_end(ray_start, ray_end, l_start, l_end))
             for l_start, l_end in lines]

def closest_ray_end(ray_start, ray_end, lines, check_intersection = True):
    line_pairs = get_intersections(ray_start, ray_end, lines, check_intersection)

    if line_pairs == []:
        return ray_end

    dist_dict = {get_length(*l):l for l in line_pairs}
    shortest_dist = sorted(dist_dict)[0]
    
    shortest_line = dist_dict[shortest_dist]
    return shortest_line[1]

def get_closest_blocking_wall(ray_start, ray_end, lines):
    lines = get_intersecting_lines(ray_start, ray_end, lines)

    # No blocking wall at all
    if lines == []:
        return (None, (ray_start, ray_end))

    # Get the intersection rays for each line 
    line_ray_pairs = [(l, (ray_start, blocked_ray_end(ray_start, ray_end, *l)))
                      for l in lines]

    dist_dict = {get_length(*ray):(l, ray) for l, ray in line_ray_pairs}
    shortest_dist = sorted(dist_dict)[0]
    
    shortest_line_ray_pair = dist_dict[shortest_dist]
    return shortest_line_ray_pair

def get_line_from_angle(ray_start, angle, length):
    x = ray_start[0] + length * math.cos(angle)
    y = ray_start[1] + length * math.sin(angle)
    return x, y 

def get_angle_from_line(ray_start, ray_end):
    dx = ray_end[0] - ray_start[0];
    dy = ray_end[1] - ray_start[1];
    return math.atan2(dy, dx)

def ray_end_plus_angle(ray_start, ray_end, angle, length=None):
    if length is None:
        length = get_length(ray_start, ray_end)
    a = get_angle_from_line(ray_start, ray_end)
    return get_line_from_angle(ray_start, a+angle, length)

def circle_up(points, center=(0, 0)):
    # Takes a list of points and 'sorts' them into a convex shape sequence
    points.sort(key=lambda p: get_angle_from_line(center, p))
    return points

def anlge_between_lines(a, b, c):
    a1 = get_angle_from_line(a, b)
    a2 = get_angle_from_line(b, c)
    return a1 - a2

def pos_to_pixels(r, c, cell_size):
    cs = cell_size
    x, y = c * cs, r * cs
    return (x, y)
