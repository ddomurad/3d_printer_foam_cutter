from fcl.options import Options
from fcl.path_planner.path_factory import PathFactory
from fcl.path_planner.tool_path import ToolPath
import fcl.utils.math as fm


class PathPlanner:
    def __init__(self, options: Options):
        self._options = options
        self._path_factory = PathFactory(options)

    def plan_tool_path_from_svg(self, svg_paths):
        paths_sets = []
        for path in svg_paths:
            paths_set = []
            for element in path:
                paths_set.append(
                    self.transform_path(self._path_factory.create_path(element)))
            paths_sets.append(paths_set)

        return paths_sets

    def transform_path(self, path: ToolPath):
        for (i, p) in enumerate(path.tool_positions):

            if self._options.invert_axis[0]:
                p = self._options.working_area[0] - p[0], p[1]
            if self._options.invert_axis[1]:
                p = p[0], self._options.working_area[1] - p[1]
            path.tool_positions[i] = p

        path.start_point = path.tool_positions[0]
        path.end_point = path.tool_positions[-1]
        return path

