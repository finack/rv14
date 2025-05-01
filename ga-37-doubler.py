import ezdxf

doc = ezdxf.new(dxfversion="R2010")
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


# Add rounded rectangle
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

# Center hole
msp.add_circle((2.75, 1.5), center_hole_diameter / 2)

# Mount holes
mount_points = [
    (2.00, 0.69),
    (3.75, 0.69),
    (2.00, 2.31),
    (3.75, 2.31),
]
for pt in mount_points:
    msp.add_circle(pt, mount_hole_diameter / 2)

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
for pt in rivet_points:
    msp.add_circle(pt, rivet_hole_diameter / 2)

dxf_path = f"ga35_doubler_v{version}.dxf"
doc.saveas(dxf_path)

dxf_path
