from fcl.options import Options
from fcl.path_planner.tool_path import ToolPath
import fcl.utils.math as fm


class GcodeGenerator:
    def __init__(self, options: Options):
        self._options = options
        self._gcode = ""

    def generate_gcode(self, paths_groups: [[ToolPath]]):
        self._gcode = self._options.start_gcode
        self._gcode += "\n"

        self._startup_commands()
        self._pick_up_tool()

        for cp in range(self._options.cutting_passes):

            self._generate_gecode_for_one_pass(paths_groups,
                                               self._options.first_cutting_height -
                                               cp*self._options.cutting_layer_size)

        self._gcode += "\n"
        self._gcode += self._options.end_gcode
        return self._gcode

    def _generate_gecode_for_one_pass(self, paths_groups: [[ToolPath]], depth):

        for paths in paths_groups:
            start_pos = paths[0].start_point

            self._pick_up_tool()
            self._travel_to(start_pos)
            self._insert_tool(depth)

            for (pi, path) in enumerate(paths):
                if pi > 0 and not fm.vec_cmp(path.start_point, paths[pi-1].end_point, 2):
                    self._pick_up_tool()
                    self._travel_to(path.start_point)
                    self._insert_tool(depth)

                for pos in path.tool_positions:
                    self._cut_to(pos)
            self._pick_up_tool()

    def _startup_commands(self):
        self._gcode += "G21; set mm\n"
        self._gcode += "G90; set absolute coordinates\n"
        self._gcode += f"G0 F{self._options.travel_speed:.2f}; set traveling speed\n"
        self._gcode += f"G1 F{self._options.cutting_speed:.2f}; set cutting  speed\n"

    def _insert_tool(self, depth):
        self._gcode += f"G1 Z{depth:.2f}; insert tool\n"

    def _pick_up_tool(self):
        self._gcode += f"G0 Z{self._options.travel_height:.2f}; pick up tool\n"

    def _travel_to(self, pos):
        self._gcode += f"G0 X{pos[0]:.2f} Y{pos[1]:.2f}; travel to\n"

    def _cut_to(self, pos):
        self._gcode += f"G1 X{pos[0]:.2f} Y{pos[1]:.2f}; cut to\n"

