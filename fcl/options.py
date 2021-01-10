class Options:
    def __init__(self, cfg):
        self.cutting_speed = cfg['cutting_speed']
        self.travel_speed = cfg['travel_speed']

        self.travel_height = cfg['travel_height']
        self.first_cutting_height = cfg['first_cutting_height']
        self.cutting_layer_size = cfg['cutting_layer_size']
        self.cutting_passes = cfg['cutting_passes']
        self.start_gcode = cfg['start_gcode']
        self.end_gcode = cfg['end_gcode']

        self.bezier_interpolation_steps = cfg['bezier_interpolation_steps']
        self.arc_interpolation_steps = cfg['arc_interpolation_steps']
        self.working_area = cfg['working_area']
        self.invert_axis = cfg['invert_axis']
        self.manual_inspection = cfg['manual_inspection']

