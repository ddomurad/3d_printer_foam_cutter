class ToolPath:
    def __init__(self):
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.tool_positions = []

    @staticmethod
    def create_path(tool_positions):
        tp = ToolPath()
        tp.tool_positions = tool_positions
        tp.start_point = tool_positions[0]
        tp.end_point = tool_positions[-1]
        return tp

    def reverse(self):
        self.tool_positions.reverse()
        self.start_point = self.tool_positions[0]
        self.end_point = self.tool_positions[-1]
        return self

    def copy(self):
        tp = ToolPath()
        tp.tool_positions = self.tool_positions.copy()
        tp.start_point = self.start_point
        tp.end_point = self.end_point
        return tp