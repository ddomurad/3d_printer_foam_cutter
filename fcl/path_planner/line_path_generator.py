import svgpathtools
from fcl.options import Options
from fcl.path_planner.tool_path import ToolPath


class LinePathGenerator:
    def __init__(self, options: Options):
        self.supported_element_type = svgpathtools.path.Line
        self._options = options

    @staticmethod
    def generate_path(element):
        return ToolPath.create_path([(element.start.real, element.start.imag), (element.end.real, element.end.imag)])
