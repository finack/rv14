import doubler_utils as utils

# Create new DXF document
doc = utils.create_document()
msp = doc.modelspace()
version = "0.2"

# Plate dimensions
plate_width = 5.0
plate_height = 3.0
corner_radius = 0.25
thickness = 0.063

# Hole specs
center_hole_diameter = 0.625
mount_hole_diameter = 0.188
rivet_hole_diameter = 0.128

# Draw rounded rectangle
utils.add_rounded_rect(msp, 0, 0, plate_width, plate_height, corner_radius)

# Center hole
utils.add_holes(msp, [(2.75, 1.5)], center_hole_diameter)

# Mount holes
mount_points = [
    (2.00, 0.69),
    (3.75, 0.69),
    (2.00, 2.31),
    (3.75, 2.31),
]
utils.add_holes(msp, mount_points, mount_hole_diameter)

# Rivet holes
rivet_points = [
    (0.30, 0.30),
    (0.30, 1.10),
    (0.30, 1.90),
    (0.30, 2.70),
    (1.18, 0.30),
    (1.18, 2.70),
    (3.82, 0.30),
    (3.82, 2.70),
    (4.70, 0.30),
    (4.70, 1.10),
    (4.70, 1.90),
    (4.70, 2.70),
]
utils.add_holes(msp, rivet_points, rivet_hole_diameter)

# Save files
file_name = f"build/ga-37-doubler-v{version}"
utils.save_files(doc, file_name, export_png=True)