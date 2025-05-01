import ezdxf

doc = ezdxf.new(dxfversion="R2010")
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
nutplate_rivet_hole_diameter = 0.098


def add_rounded_rect(msp, x, y, w, h, r):
    msp.add_line((x + r, y), (x + w - r, y))
    msp.add_line((x + w, y + r), (x + w, y + h - r))
    msp.add_line((x + w - r, y + h), (x + r, y + h))
    msp.add_line((x, y + h - r), (x, y + r))
    msp.add_arc(center=(x + r, y + r), radius=r, start_angle=180, end_angle=270)
    msp.add_arc(center=(x + w - r, y + r), radius=r, start_angle=270, end_angle=360)
    msp.add_arc(center=(x + w - r, y + h - r), radius=r, start_angle=0, end_angle=90)
    msp.add_arc(center=(x + r, y + h - r), radius=r, start_angle=90, end_angle=180)


add_rounded_rect(msp, 0, 0, plate_width, plate_height, corner_radius)

# Center holes
msp.add_circle((2.08, 1.75), center_hole_diameter / 2)
msp.add_circle((3.43, 1.75), center_hole_diameter / 2)

# Mount holes
# (x, y)
mount_points = [
    (1.13, 0.95),
    (4.43, 0.95),
    (1.13, 2.55),
    (4.43, 2.55),
]
for pt in mount_points:
    msp.add_circle(pt, mount_hole_diameter / 2)

nutplate_center_to_rivet_center = 0.344
nutplate_rivet_points = [
    (1.13 - nutplate_center_to_rivet_center, 0.95),
    (1.13 + nutplate_center_to_rivet_center, 0.95),
    (4.43 - nutplate_center_to_rivet_center, 0.95),
    (4.43 + nutplate_center_to_rivet_center, 0.95),
    (1.13 - nutplate_center_to_rivet_center, 2.55),
    (1.13 + nutplate_center_to_rivet_center, 2.55),
    (4.43 - nutplate_center_to_rivet_center, 2.55),
    (4.43 + nutplate_center_to_rivet_center, 2.55),
]
for pt in nutplate_rivet_points:
    msp.add_circle(pt, nutplate_rivet_hole_diameter / 2)

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
for pt in rivet_points:
    msp.add_circle(pt, rivet_hole_diameter / 2)

dxf_path = f"ga57x_doubler_v{version}.dxf"
doc.saveas(dxf_path)

dxf_path
