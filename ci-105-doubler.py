# Design notes
# - Space between the conn hole and rib is 0.6 (with prob interference)
# - Using AN4 rivets for strength

import doubler_utils as utils

doc = utils.create_document()
msp = doc.modelspace()
version = "0.3"

# Parameters
# Antenna is 4.0 x 0.92
width = 4.0 + 1
height = 0.92 + 0.5  # Can't go bigger since rib is in the way
conn_diameter = 0.563
conn_x_center = width / 2
conn_y_center = height / 2
mount_hole_spacing = 1.75
mount_hole_diameter = 0.177
rivet_an3_diameter = 0.098
rivet_an4_diameter = 0.1285
edge_distance = 0.25
corner_radius = 0.25

# Draw rounded rectangle
utils.add_rounded_rect(msp, 0, 0, width, height, corner_radius)

# Connector antenna hole
utils.add_holes(msp, [(conn_x_center, conn_y_center)], conn_diameter)

# Mounting holes
mounting_holes = [
    (conn_x_center - mount_hole_spacing / 2, conn_y_center),
    (conn_x_center + mount_hole_spacing / 2, conn_y_center),
]
utils.add_holes(msp, mounting_holes, mount_hole_diameter)

rivet_points = [
    (edge_distance, edge_distance),
    (edge_distance, height / 2),
    (edge_distance, height - edge_distance),
    (width - edge_distance, edge_distance),
    (width - edge_distance, height / 2),
    (width - edge_distance, height - edge_distance),
]

utils.add_holes(msp, rivet_points, rivet_an4_diameter)

file_name = f"build/ci-105-doubler-v{version}"
# Expected actual width should be about 4.25 inches based on the plate dimensions
utils.save_files(doc, file_name)
