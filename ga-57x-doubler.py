import doubler_utils as utils

# Create new DXF document
doc = utils.create_document()
msp = doc.modelspace()
version = "0.2"

# Plate dimensions
plate_width = 5.5
plate_height = 3.5
corner_radius = 0.25
thickness = 0.063

# Hole specs
center_hole_diameter = 0.625
mount_hole_diameter = 0.203
rivet_hole_diameter = 0.128
rivet_an3_diameter = 0.128

# Draw rounded rectangle
utils.add_rounded_rect(msp, 0, 0, plate_width, plate_height, corner_radius)

# Center holes
center_holes = [
    (2.08, 1.75),
    (3.43, 1.75)
]
utils.add_holes(msp, center_holes, center_hole_diameter)

# Mount holes
mount_points = [
    (1.13, 0.95),
    (4.43, 0.95),
    (1.13, 2.55),
    (4.43, 2.55),
]
utils.add_holes(msp, mount_points, mount_hole_diameter)

# Nutplate rivet holes
nutplate_center_to_rivet_center = 0.344
nutplate_rivet_points = []

for pt in mount_points:
    nutplate_rivet_points.extend([
        (pt[0] - nutplate_center_to_rivet_center, pt[1]),
        (pt[0] + nutplate_center_to_rivet_center, pt[1])
    ])

utils.add_holes(msp, nutplate_rivet_points, rivet_an3_diameter)

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
utils.add_holes(msp, rivet_points, rivet_hole_diameter)

# Save files
file_name = f"build/ga-57x-doubler-v{version}"
# Expected actual width is 5.5 inches based on the plate dimensions
utils.save_files(doc, file_name)