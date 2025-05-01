# Patch to the previous script to add curved corners to the doubler rectangle

import ezdxf
from ezdxf.math import ConstructionArc

doc = ezdxf.new(dxfversion="R2010")
msp = doc.modelspace()
version = "0.2"

# Parameters
width = 6.0
height = 3.0
center_x = width / 2
center_y = height / 2
center_hole_diameter = 0.563
mount_hole_spacing = 1.75
mount_hole_diameter = 0.177
rivet_diameter = 0.128
rivet_margin = 0.5  # inches from edge
rivet_spacing = 1.0
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

# Top and bottom rivet lines
x_vals = [
    rivet_margin + i * rivet_spacing
    for i in range(int((width - 2 * rivet_margin) // rivet_spacing) + 1)
]
for x in x_vals:
    msp.add_circle((x, rivet_margin), rivet_diameter / 2)
    msp.add_circle((x, height - rivet_margin), rivet_diameter / 2)

# Left and right rivet lines
y_vals = [
    rivet_margin + i * rivet_spacing
    for i in range(1, int((height - 2 * rivet_margin) // rivet_spacing) + 1)
]
for y in y_vals:
    msp.add_circle((rivet_margin, y), rivet_diameter / 2)
    msp.add_circle((width - rivet_margin, y), rivet_diameter / 2)

# Save file
dxf_file = f"ci105_doubler_v{version}.dxf"
doc.saveas(dxf_file)

dxf_file
