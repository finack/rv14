# Design notes
# - GHA-15 mounting cutout and unit outline

import doubler_utils as utils
from doubler_utils import RIVET_AN3_DIAMETER, RIVET_AN4_DIAMETER

doc = utils.create_document()
msp = doc.modelspace()
version = "0.1"

# Plate dimensions (matching the unit outline)
plate_width = 5.0 + (24.0 / 32.0)
plate_height = 6.0 + (11.0 / 32.0)  # 6 11/32"
corner_radius = 1.0

# Center cutout for unit mounting
center_cutout_diameter = 1.50
center_x = plate_width / 2
center_y = plate_height / 2

# Mounting hole specifications
mount_hole_diameter = 0.210  # Nominal diameter (tolerance ±0.003)

# Mounting hole positions (from diagram)
# Holes positioned from centerline:
# Horizontal: 1.375" from center (2.750" apart)
# Vertical: 1.450" from center (2.9" apart)
horizontal_offset_from_center = 1.375
vertical_offset_from_center = 1.450

mount_hole_right_x = center_x + horizontal_offset_from_center
mount_hole_left_x = center_x - horizontal_offset_from_center
mount_hole_top_y = center_y + vertical_offset_from_center
mount_hole_bottom_y = center_y - vertical_offset_from_center

# Draw rounded rectangle for plate outline
utils.add_rounded_rect(msp, 0, 0, plate_width, plate_height, corner_radius)

# Center cutout hole for unit mounting
utils.add_holes(msp, [(center_x, center_y)], center_cutout_diameter)

# Mounting holes (screws only, no nutplate rivets)
mounting_holes = [
    (mount_hole_left_x, mount_hole_bottom_y),
    (mount_hole_right_x, mount_hole_bottom_y),
    (mount_hole_left_x, mount_hole_top_y),
    (mount_hole_right_x, mount_hole_top_y),
]

# Add mounting holes
utils.add_holes(msp, mounting_holes, mount_hole_diameter)

# Save files
file_name = f"build/gha-15-doubler-v{version}"
utils.save_files(doc, file_name)
