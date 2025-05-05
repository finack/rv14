# Patch to the previous script to add curved corners to the doubler rectangle

import ezdxf
from ezdxf.math import ConstructionArc

doc = ezdxf.new(dxfversion="R2010")
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


def add_rounded_rect(msp, x, y, w, h, r):
    msp.add_line((x + r, y), (x + w - r, y))
    msp.add_line((x + w, y + r), (x + w, y + h - r))
    msp.add_line((x + w - r, y + h), (x + r, y + h))
    msp.add_line((x, y + h - r), (x, y + r))
    msp.add_arc(center=(x + r, y + r), radius=r, start_angle=180, end_angle=270)
    msp.add_arc(center=(x + w - r, y + r), radius=r, start_angle=270, end_angle=360)
    msp.add_arc(center=(x + w - r, y + h - r), radius=r, start_angle=0, end_angle=90)
    msp.add_arc(center=(x + r, y + h - r), radius=r, start_angle=90, end_angle=180)


# Draw rounded rectangle
add_rounded_rect(msp, 0, 0, width, height, corner_radius)

# Center antenna hole
msp.add_circle((center_x, center_y), center_hole_diameter / 2)

# Mounting holes
msp.add_circle((center_x - mount_hole_spacing / 2, center_y), mount_hole_diameter / 2)
msp.add_circle((center_x + mount_hole_spacing / 2, center_y), mount_hole_diameter / 2)

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

for pt in rivet_points:
    msp.add_circle(pt, rivet_diameter / 2)

# Save file
dxf_file = f"ci105_doubler_v{version}.dxf"
doc.saveas(dxf_file)

dxf_file
