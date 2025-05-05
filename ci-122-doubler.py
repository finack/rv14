# Design notes
# - Existing doubler is 3 x 2
# - Available space is on 2" fore of center, 3" aft of center
# Attaches with four #8-32, flat head 100 degree stainless steel
# into MS21059-08 nutplates
# - Comant Instructions A12206 Rev: A used for dimensions of antenna

import doubler_utils as utils

# Create new DXF document
doc = utils.create_document()
msp = doc.modelspace()
version = "0.1"

# Plate parameters
width = 4.30
height = 3
conn_hole_diameter = 0.625
conn_x_center = 1.9
conn_y_center = height / 2
mount_hole_spacing_x = 1.75
mount_hole_left_of_center = 1.0
mount_hole_spacing_y = 1.625
mount_hole_y_offset = 0.812
mount_hole_diameter = 0.177
rivet_an4_diameter = 0.1285
rivet_an3_diameter = 0.098
nutplate_rivet_spacing = 0.281
corner_radius = 0.25
bend_height = 0.255

# Draw rounded rectangle
utils.add_rounded_rect(msp, 0, 0, width, height, corner_radius)

# Add bent edges along the x-axis at top and bottom
utils.add_bent_edge(msp, 0, bend_height, width)
utils.add_bent_edge(msp, 0, height - bend_height, width)

# Center antenna hole
utils.add_holes(msp, [(conn_x_center, conn_y_center)], conn_hole_diameter)

# Mounting holes and nutplate rivet holes
mounting_holes = [
    (conn_x_center - mount_hole_left_of_center, conn_y_center + mount_hole_y_offset),
    (
        conn_x_center - mount_hole_left_of_center + mount_hole_spacing_x,
        conn_y_center + mount_hole_y_offset,
    ),
    (conn_x_center - mount_hole_left_of_center, conn_y_center - mount_hole_y_offset),
    (
        conn_x_center - mount_hole_left_of_center + mount_hole_spacing_x,
        conn_y_center - mount_hole_y_offset,
    ),
]

# Add mounting holes
utils.add_holes(msp, mounting_holes, mount_hole_diameter)

# Add nutplate rivet holes
utils.add_nutplate_rivets(msp, mounting_holes, rivet_an3_diameter, nutplate_rivet_spacing)

# Add reinforcement rivets
rivet_points = [
    (0.3, conn_y_center - mount_hole_y_offset),
    (0.3, height / 2),
    (0.3, conn_y_center + mount_hole_y_offset),
    (width - 0.3, conn_y_center - mount_hole_y_offset),
    (width - 0.3, height / 2),
    (width - 0.3, conn_y_center + mount_hole_y_offset),
]

utils.add_holes(msp, rivet_points, rivet_an3_diameter)

# Save files
file_name = f"build/ci-122-doubler-v{version}"
utils.save_files(doc, file_name, export_png=True)