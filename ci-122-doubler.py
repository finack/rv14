# Design notes
# - Existing doubler is 3 x 2
# - Available space is on 2" fore of center, 3" aft of center
# Attaches with four #8-32, flat head 100 degree stainless steel
# into MS21059-08 nutplates
# - Comant Instructions A12206 Rev: A used for dimensions of antenna

import ezdxf
from ezdxf.math import ConstructionArc
from ezdxf.addons.drawing import matplotlib

doc = ezdxf.new(dxfversion="R2010")
doc.linetypes.add("DASHED", pattern=[0.5, 0.5, 0.0])
msp = doc.modelspace()
version = "0.1"

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


def add_rounded_rect(msp, x, y, w, h, r):
    msp.add_line((x + r, y), (x + w - r, y))
    msp.add_line((x + w, y + r), (x + w, y + h - r))
    msp.add_line((x + w - r, y + h), (x + r, y + h))
    msp.add_line((x, y + h - r), (x, y + r))
    msp.add_arc(center=(x + r, y + r), radius=r, start_angle=180, end_angle=270)
    msp.add_arc(center=(x + w - r, y + r), radius=r, start_angle=270, end_angle=360)
    msp.add_arc(center=(x + w - r, y + h - r), radius=r, start_angle=0, end_angle=90)
    msp.add_arc(center=(x + r, y + h - r), radius=r, start_angle=90, end_angle=180)


def add_bent_edge(msp, x, y, length):
    bend_line = msp.add_line((x, y), (x + length, y))
    bend_line.dxf.linetype = "DASHED"


# Draw rounded rectangle
add_rounded_rect(msp, 0, 0, width, height, corner_radius)

# Add bent edges along the x-axis at top and bottom
add_bent_edge(msp, 0, bend_height, width)
add_bent_edge(msp, 0, height - bend_height, width)

# Center antenna hole
msp.add_circle((conn_x_center, conn_y_center), conn_hole_diameter / 2)

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

for hole_center in mounting_holes:
    # Add mounting hole
    msp.add_circle(hole_center, mount_hole_diameter / 2)

    # Add nutplate rivet holes on each side of the mounting hole (along x-axis)
    msp.add_circle(
        (hole_center[0] - nutplate_rivet_spacing, hole_center[1]),
        rivet_an3_diameter / 2,
    )
    msp.add_circle(
        (hole_center[0] + nutplate_rivet_spacing, hole_center[1]),
        rivet_an3_diameter / 2,
    )

y_spacing = (height * 0.3) / 3

rivet_points = [
    (0.3, conn_y_center - mount_hole_y_offset),
    (0.3, height / 2),
    (0.3, conn_y_center + mount_hole_y_offset),
    (width - 0.3, conn_y_center - mount_hole_y_offset),
    (width - 0.3, height / 2),
    (width - 0.3, conn_y_center + mount_hole_y_offset),
]

for pt in rivet_points:
    msp.add_circle(pt, rivet_an3_diameter / 2)

file_name = f"build/ci-122-doubler-v{version}"
doc.saveas(f"{file_name}.dxf")

# Use inverse color scheme for PNG output (black lines on white background)
matplotlib.qsave(doc.modelspace(), f"{file_name}.png", dpi=300, bg="#FFFFFF")
