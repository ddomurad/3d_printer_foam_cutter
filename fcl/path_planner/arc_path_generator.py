import svgpathtools
from fcl.options import Options
from fcl.path_planner.tool_path import ToolPath
import fcl.utils.math as fm
from math import sin, cos, pi, sqrt, acos, copysign


class ArcBezierPathGenerator:
    def __init__(self, options: Options):
        self.supported_element_type = svgpathtools.path.Arc
        self._options = options

    @staticmethod
    def get_angle(u, v):
        dp = fm.vec_dot(u, v)
        vl = fm.vec_len(u)*fm.vec_len(v)
        sign = copysign(1, u[0]*v[1] - u[1]*v[0])
        return sign*acos(dp/vl)

    def generate_path(self, element):
        x1, y1 = element.start.real, element.start.imag
        rx, ry = (element.radius.real, element.radius.imag)
        th = element.rotation*pi/180 # rad ?

        fa = element.large_arc
        fs = element.sweep
        x2, y2 = (element.end.real, element.end.imag)

        zx = (x1 - x2) / 2
        zy = (y1 - y2) / 2

        x1p = cos(th) * zx + sin(th) * zy
        y1p = -sin(th) * zx + cos(th) * zy

        ue1 = rx ** 2 * ry ** 2 - rx**2 * y1p**2 - ry**2*x1p**2
        ue2 = rx**2*y1p**2 + ry**2*x1p**2
        ue = sqrt(ue1 / ue2)

        if fa == fs:
            ue = -ue

        cxp = ue * rx * y1p / ry
        cyp = -ue * ry * x1p / rx

        sx = (x1 + x2) / 2
        sy = (y1 + y2) / 2

        cx = cos(th) * cxp - sin(th) * cyp + sx
        cy = sin(th) * cxp + cos(th) * cyp + sy

        th1 = ArcBezierPathGenerator.get_angle((1, 0), ((x1p - cxp) / rx, (y1p - cyp) / ry))
        dth = ArcBezierPathGenerator.get_angle(((x1p-cxp)/rx, (y1p-cyp)/ry), ((-x1p-cxp)/rx, (-y1p-cyp)/ry))

        N = self._options.arc_interpolation_steps
        dt = 1/N
        points = []

        for di in range(N+1):
            t = di*dt
            ct = th1 + dth*t

            x = rx*cos(ct)
            y = ry*sin(ct)

            xp = x * cos(th) - y * sin(th)
            yp = x * sin(th) + y * cos(th)

            points.append((xp + cx, yp + cy))

        return ToolPath.create_path(points)
