import argparse
import json
from svgpathtools import svg2paths
from fcl import PathPlanner, Options, GcodeGenerator


parser = argparse.ArgumentParser(description='Generate foam cutter gcode from svg file.')
parser.add_argument('-i', type=str, help='svg input file', required=True)
parser.add_argument('-o', type=str, help='generated gcode file', required=True)
parser.add_argument('-c', type=str, help='configuration file', required=True)

args = parser.parse_args()
input_file, output_file, config_file = args.i, args.o, args.c

print(f"Generating gcode with arguments: input_file: '{input_file}', output_file: '{output_file}', config_file: '{config_file}'")

json_config = json.load(open(config_file, 'r'))
print("Configuration used: ", json_config)

options = Options(json_config)
planner = PathPlanner(options)
gcode_generator = GcodeGenerator(options)

paths, attributes = svg2paths(input_file)
paths.reverse()
tool_path = planner.plan_tool_path_from_svg(paths)

gcode = gcode_generator.generate_gcode(tool_path)
with open(output_file, 'w') as out_file:
    out_file.write(gcode)

new_line = '\n'
print(f"Gcode written into: '{output_file}', length: {len(gcode)} chars, lines: { gcode.count(new_line)}")
