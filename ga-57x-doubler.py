import doubler_utils as utils
from doubler_utils import RIVET_AN3_DIAMETER, RIVET_AN4_DIAMETER

# Create new DXF document
doc = utils.create_document()
msp = doc.modelspace()
version = "0.3"

# Plate dimensions
plate_width = 5.5
plate_height = 3.5
corner_radius = 0.25
thickness = 0.063

# Hole specs
center_hole_diameter = 0.625
mount_hole_diameter = 0.203
nutplate_spacing = 0.344

# Draw rounded rectangle
utils.add_rounded_rect(msp, 0, 0, plate_width, plate_height, corner_radius)

# Center holes
center_holes = [(2.08, 1.75), (3.43, 1.75)]
utils.add_holes(msp, center_holes, center_hole_diameter)

# Mount holes and nutplate rivets
mount_points = [
    (1.13, 0.95),
    (4.43, 0.95),
    (1.13, 2.55),
    (4.43, 2.55),
]
utils.add_nutplate_mounting_holes(
    msp, mount_points, mount_hole_diameter, RIVET_AN3_DIAMETER, nutplate_spacing
)

# Rivet holes
rivet_points = [
    (0.30, 0.30),
    (0.30, 1.27),
    (0.30, 2.24),
    (0.30, 3.20),
    (1.74, 0.30),
    (1.74, 3.20),
    (3.76, 0.30),
    (3.75, 3.20),
    (5.20, 0.30),
    (5.20, 1.27),
    (5.20, 2.24),
    (5.20, 3.20),
]
utils.add_holes(msp, rivet_points, RIVET_AN4_DIAMETER)

# Save files
file_name = f"build/ga-57x-doubler-v{version}"
# Expected actual width is 5.5 inches based on the plate dimensions
utils.save_files(doc, file_name)
