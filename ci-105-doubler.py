# Patch to the previous script to add curved corners to the doubler rectangle

import doubler_utils as utils

# Create new DXF document
doc = utils.create_document()
msp = doc.modelspace()
version = "0.3"

# Parameters
width = 5.0
center_hole_diameter = 0.563
# Bottom margin reduced due to interference with rib
bottom_margin = 0.5 + center_hole_diameter / 2
top_margin = 1.5 + center_hole_diameter / 2
height = bottom_margin + top_margin
center_x = width / 2
center_y = bottom_margin
mount_hole_spacing = 1.75
mount_hole_diameter = 0.177
rivet_diameter = 0.128
corner_radius = 0.25

# Draw rounded rectangle
utils.add_rounded_rect(msp, 0, 0, width, height, corner_radius)

# Center antenna hole
utils.add_holes(msp, [(center_x, center_y)], center_hole_diameter)

# Mounting holes
mounting_holes = [
    (center_x - mount_hole_spacing / 2, center_y),
    (center_x + mount_hole_spacing / 2, center_y)
]
utils.add_holes(msp, mounting_holes, mount_hole_diameter)

# Calculate vertical spacing for evenly distributed rivets
y_spacing = (height - 2*0.3) / 3  # Divide available space into 3 parts to get 4 evenly spaced rivets

# Rivet holes with 0.3" edge distance
rivet_points = [
    # Bottom edge
    (0.3, 0.3),
    (1.3, 0.3),
    (3.7, 0.3),
    (4.7, 0.3),
    
    # Top edge
    (0.3, height - 0.3),
    (1.3, height - 0.3),
    (3.7, height - 0.3),
    (4.7, height - 0.3),
    
    # Left edge - 2 additional rivets (corners already counted in top/bottom edges)
    (0.3, 0.3 + y_spacing),        # 1/3 up
    (0.3, 0.3 + 2*y_spacing),      # 2/3 up
    
    # Right edge - 2 additional rivets (corners already counted in top/bottom edges)
    (width - 0.3, 0.3 + y_spacing), # 1/3 up
    (width - 0.3, 0.3 + 2*y_spacing) # 2/3 up
]

utils.add_holes(msp, rivet_points, rivet_diameter)

# Save files
file_name = f"build/ci-105-doubler-v{version}"
utils.save_files(doc, file_name, export_png=True)