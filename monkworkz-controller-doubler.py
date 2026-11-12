# Design notes
# - Doubler for Monkworkz engine controller, mounted on firewall
# - Controller has 4 mounting holes: 4.255" horizontal x 2.314" vertical spacing
# - Controller mounts with four 6-32 screws into MS21059-06 nutplates
# - Nutplates attach with -3 rivets, 0.688" center-to-center spacing
# - Doubler attaches to firewall with four -3 rivets, arranged in the same
#   aspect ratio as the mounting hole pattern but scaled to 40% so
#   they clear the nutplate rivet holes

import doubler_utils as utils
from doubler_utils import RIVET_AN3_DIAMETER, RIVET_AN4_DIAMETER

doc = utils.create_document()
msp = doc.modelspace()
version = "0.4"

# Mounting hole specifications (Monkworkz controller)
mount_hole_diameter = 0.146  # clearance hole for a #6 screw
mount_hole_spacing_x = 4.255  # horizontal, center to center
mount_hole_spacing_y = 2.314  # vertical, center to center
nutplate_rivet_spacing = 0.344  # center to each MS21059-06 attachment rivet

# Plate parameters
edge_distance = 0.35  # margin from features to plate edge
corner_radius = 0.25
width = mount_hole_spacing_x + 2 * (nutplate_rivet_spacing + edge_distance)
height = mount_hole_spacing_y + 2 * edge_distance + mount_hole_diameter
center_x = width / 2
center_y = height / 2

# Mounting hole positions (corners of the rectangle defined by the spacing)
mounting_holes = [
    (center_x - mount_hole_spacing_x / 2, center_y - mount_hole_spacing_y / 2),
    (center_x + mount_hole_spacing_x / 2, center_y - mount_hole_spacing_y / 2),
    (center_x - mount_hole_spacing_x / 2, center_y + mount_hole_spacing_y / 2),
    (center_x + mount_hole_spacing_x / 2, center_y + mount_hole_spacing_y / 2),
]

# Draw rounded rectangle for plate outline
utils.add_rounded_rect(msp, 0, 0, width, height, corner_radius)

# Mounting holes with nutplate rivet holes
utils.add_nutplate_mounting_holes(
    msp,
    mounting_holes,
    mount_hole_diameter,
    RIVET_AN3_DIAMETER,
    nutplate_rivet_spacing,
)

# Firewall attach rivets: same aspect ratio as the mounting hole pattern,
# scaled down 40% so they clear the nutplate rivet holes
firewall_rivet_scale = 0.40
firewall_rivet_spacing_x = mount_hole_spacing_x * firewall_rivet_scale
firewall_rivet_spacing_y = mount_hole_spacing_y * firewall_rivet_scale
firewall_rivets = [
    (
        center_x - firewall_rivet_spacing_x / 2,
        center_y - firewall_rivet_spacing_y / 2,
    ),
    (
        center_x + firewall_rivet_spacing_x / 2,
        center_y - firewall_rivet_spacing_y / 2,
    ),
    (
        center_x - firewall_rivet_spacing_x / 2,
        center_y + firewall_rivet_spacing_y / 2,
    ),
    (
        center_x + firewall_rivet_spacing_x / 2,
        center_y + firewall_rivet_spacing_y / 2,
    ),
]
utils.add_holes(msp, firewall_rivets, RIVET_AN3_DIAMETER)

# Save files
file_name = f"build/monkworkz-controller-doubler-v{version}"
utils.save_files(doc, file_name)
