from fcl.options import Options
from fcl.path_planner.tool_path import ToolPath
import fcl.utils.math as fm


class GcodeGenerator:
    def __init__(self, options: Options):
        self._options = options
        self._gcode = ""
        self._current_pos = (-1, -1)

    def generate_gcode(self, paths_groups: [[ToolPath]]):
        self._gcode = self._options.start_gcode
        self._gcode += "\n"

        self._startup_commands()
        self._pick_up_tool(True)

        for paths in paths_groups:
            self._generate_passes_for_one_group(paths)

        self._gcode += "\n"
        self._gcode += self._options.end_gcode
        return self._gcode

    def _generate_passes_for_one_group(self, paths: [ToolPath]):
        start_pos = paths[0].start_point
        self._travel_to(start_pos)

        for cp in range(self._options.cutting_passes):
            depth = self._options.first_cutting_height - cp*self._options.cutting_layer_size

            self._insert_tool(depth)

            for (pi, path) in enumerate(paths):
                if pi > 0 and not fm.vec_cmp(path.start_point, paths[pi-1].end_point, 2):
                    self._pick_up_tool()
                    self._travel_to(path.start_point)
                    self._insert_tool(depth)

                for pos in path.tool_positions:
                    self._cut_to(pos)

        if self._options.manual_inspection:
            self._manual_inspection()
        self._pick_up_tool()

    def _startup_commands(self):
        self._gcode += "G21; set mm\n"
        self._gcode += "G90; set absolute coordinates\n"

    def _insert_tool(self, depth):
        self._gcode += f"G1 F{self._options.travel_speed:.2f}; set cutting  speed\n"
        self._gcode += f"G1 Z{depth:.2f}; insert tool\n"
        self._gcode += f"G1 F{self._options.cutting_speed:.2f}; set cutting  speed\n"
        self._is_cutting = True

    def _pick_up_tool(self, force=False):
        self._gcode += f"G0 F{self._options.travel_speed:.2f}; set traveling speed\n"
        self._gcode += f"G0 Z{self._options.travel_height:.2f}; pick up tool\n"
        self._is_cutting = False

    def _travel_to(self, pos):
        if self._current_pos != pos:
            self._gcode += f"G0 X{pos[0]:.2f} Y{pos[1]:.2f}; travel to\n"
            self._current_pos = pos

    def _cut_to(self, pos):
        if self._current_pos != pos:
            self._gcode += f"G1 X{pos[0]:.2f} Y{pos[1]:.2f}; cut to\n"
            self._current_pos = pos

    def _manual_inspection(self):
        self._gcode += "M0 Inspect and press the button; manual inspection\n"
