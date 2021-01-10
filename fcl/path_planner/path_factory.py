import sys
from fcl.options import Options
from fcl.path_planner.line_path_generator import LinePathGenerator
from fcl.path_planner.quadratic_bezier_path_generator import QuadraticBezierPathGenerator
from fcl.path_planner.cubic_bezier_path_generator import CubicBezierPathGenerator
from fcl.path_planner.arc_path_generator import ArcBezierPathGenerator


class PathFactory:
    def __init__(self, options: Options):
        self._options = options
        self._factories = {}

        self._register_factory(LinePathGenerator(options))
        self._register_factory(QuadraticBezierPathGenerator(options))
        self._register_factory(CubicBezierPathGenerator(options))
        self._register_factory(ArcBezierPathGenerator(options))

    def _register_factory(self, factory):
        self._factories[factory.supported_element_type] = factory

    def create_path(self, svg_element):
        if type(svg_element) in self._factories:
            return self._factories[type(svg_element)].generate_path(svg_element)
        else:
            print(f"{type(svg_element)} not supported",  file=sys.stderr)
            exit(1)
