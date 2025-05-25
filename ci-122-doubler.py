# Design notes
# - Existing doubler is 3 x 2
# - Available space is on 2" fore of center, 3" aft of center
# Attaches with four #8-32, flat head 100 degree stainless steel
# into MS21059-08 nutplates
# - Comant Instructions A12206 Rev: A used for dimensions of antenna

import doubler_utils as utils
from doubler_utils import RIVET_AN3_DIAMETER, RIVET_AN4_DIAMETER

# Create new DXF document
doc = utils.create_document()
msp = doc.modelspace()
version = "0.1"

# Plate parameters
width = 4.30
height = 2.75
conn_hole_diameter = 0.575
conn_x_center = 1.9
conn_y_center = height / 2
mount_hole_spacing_x = 1.75
mount_hole_left_of_center = 1.0
mount_hole_spacing_y = 1.625
mount_hole_y_offset = 0.812
mount_hole_diameter = 0.177
nutplate_rivet_spacing = 0.281
corner_radius = 0.25

# Draw rounded rectangle
utils.add_rounded_rect(msp, 0, 0, width, height, corner_radius)

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
utils.add_nutplate_rivets(
    msp, mounting_holes, RIVET_AN3_DIAMETER, nutplate_rivet_spacing
)

# Add reinforcement rivets
rivet_points = [
    (0.3, conn_y_center - mount_hole_y_offset),
    (0.3, height / 2),
    (0.3, conn_y_center + mount_hole_y_offset),
    (width - 0.3, conn_y_center - mount_hole_y_offset),
    (width - 0.3, height / 2),
    (width - 0.3, conn_y_center + mount_hole_y_offset),
]

utils.add_holes(msp, rivet_points, RIVET_AN4_DIAMETER)

# Save files
file_name = f"build/ci-122-doubler-v{version}"
# Expected actual width should be about 4.3 inches based on the plate dimensions
utils.save_files(doc, file_name)
