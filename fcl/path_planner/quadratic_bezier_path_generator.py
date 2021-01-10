import svgpathtools
from fcl.options import Options
from fcl.path_planner.tool_path import ToolPath
import fcl.utils.math as fm


class QuadraticBezierPathGenerator:
    def __init__(self, options: Options):
        self.supported_element_type = svgpathtools.path.QuadraticBezier
        self._options = options

    def generate_path(self, element):
        p0 = (element.start.real, element.start.imag)
        p1 = (element.control.real, element.control.imag)
        p2 = (element.end.real, element.end.imag)

        n = self._options.bezier_interpolation_steps
        dt = 1/n
        points = []

        for ti in range(n+1):
            t = ti*dt
            rt = 1-t

            b = fm.vec_add(
                fm.vec_mul(p0, rt**2),
                fm.vec_mul(p1, 2*rt*t),
                fm.vec_mul(p2, t**2))

            points.append(b)
        return ToolPath.create_path(points)
