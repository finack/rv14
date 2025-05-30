"""
Utility functions for aircraft doubler plate designs.
"""

import ezdxf
from ezdxf.addons.drawing import matplotlib
from ezdxf import bbox

# Standard rivet diameters (inches)
RIVET_AN3_DIAMETER = 0.098
RIVET_AN4_DIAMETER = 0.1285


def create_document():
    """Create a new DXF document with R2010 version using inches as units."""
    doc = ezdxf.new(dxfversion="R2010")
    # Set document units to inches
    doc.header["$INSUNITS"] = 1  # 1 = inches
    doc.linetypes.add("DASHED", pattern=[0.5, 0.5, 0.0])
    return doc


def add_rounded_rect(msp, x, y, w, h, r):
    """
    Add a rectangle with rounded corners to the modelspace.

    Args:
        msp: modelspace object
        x, y: coordinates of the bottom-left corner
        w, h: width and height of the rectangle
        r: corner radius
    """
    msp.add_line((x + r, y), (x + w - r, y))
    msp.add_line((x + w, y + r), (x + w, y + h - r))
    msp.add_line((x + w - r, y + h), (x + r, y + h))
    msp.add_line((x, y + h - r), (x, y + r))
    msp.add_arc(center=(x + r, y + r), radius=r, start_angle=180, end_angle=270)
    msp.add_arc(center=(x + w - r, y + r), radius=r, start_angle=270, end_angle=360)
    msp.add_arc(center=(x + w - r, y + h - r), radius=r, start_angle=0, end_angle=90)
    msp.add_arc(center=(x + r, y + h - r), radius=r, start_angle=90, end_angle=180)


def add_bent_edge(msp, x, y, length):
    """
    Add a dashed line representing a bent edge.

    Args:
        msp: modelspace object
        x, y: starting coordinates
        length: length of the bent edge
    """
    bend_line = msp.add_line((x, y), (x + length, y))
    bend_line.dxf.linetype = "DASHED"


def add_holes(msp, centers, diameter):
    """
    Add circles at specified centers with given diameter.

    Args:
        msp: modelspace object
        centers: list of (x, y) coordinates for hole centers
        diameter: hole diameter
    """
    for center in centers:
        msp.add_circle(center, diameter / 2)


def add_nutplate_rivets(msp, mount_hole_centers, rivet_diameter, spacing):
    """
    Add nutplate rivet holes along x-axis for each mounting hole.

    Args:
        msp: modelspace object
        mount_hole_centers: list of (x, y) coordinates for mounting holes
        rivet_diameter: diameter of the rivet holes
        spacing: spacing between nutplate rivets and mounting hole center
    """
    for hole_center in mount_hole_centers:
        msp.add_circle(
            (hole_center[0] - spacing, hole_center[1]),
            rivet_diameter / 2,
        )
        msp.add_circle(
            (hole_center[0] + spacing, hole_center[1]),
            rivet_diameter / 2,
        )


def add_nutplate_mounting_holes(
    msp, mount_points, mount_hole_diameter, rivet_diameter, nutplate_spacing=0.344
):
    """
    Add mounting holes with corresponding nutplate rivet holes.

    Args:
        msp: modelspace object
        mount_points: list of (x, y) coordinates for mounting holes
        mount_hole_diameter: diameter of the mounting holes
        rivet_diameter: diameter of the rivet holes for nutplates
        nutplate_spacing: spacing between nutplate rivets and mounting hole center
    """
    # Add the mounting holes
    add_holes(msp, mount_points, mount_hole_diameter)

    # Add the nutplate rivet holes
    add_nutplate_rivets(msp, mount_points, rivet_diameter, nutplate_spacing)


def save_files(doc, filename):
    """
    Save the document as DXF and as PNG with standardized settings.

    Args:
        doc: ezdxf document
        filename: base filename without extension
    """
    # Save DXF file
    doc.saveas(f"{filename}.dxf")

    dpi = 600
    extents = bbox.extents(doc.modelspace())
    width = extents.extmax.x - extents.extmin.x
    height = extents.extmax.y - extents.extmin.y

    scale_factor = 32 / 29  # Adjusted to correct 29/32" printing to 1"

    width_inches = width * scale_factor
    height_inches = height * scale_factor

    fig_args = {"bg": "#FFFFFF", "dpi": dpi}
    fig_args["size_inches"] = (width_inches, height_inches)

    matplotlib.qsave(
        doc.modelspace(),
        f"{filename}.pdf",
        **fig_args,
    )

    return f"{filename}.dxf"
