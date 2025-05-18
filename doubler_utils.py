"""
Utility functions for aircraft doubler plate designs.
"""

import ezdxf
from ezdxf.addons.drawing import matplotlib
from ezdxf import bbox


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
    Add nutplate rivet holes for each mounting hole.

    Args:
        msp: modelspace object
        mount_hole_centers: list of (x, y) coordinates for mounting holes
        rivet_diameter: diameter of the rivet holes
        spacing: spacing between nutplate rivets and mounting hole center
    """
    for hole_center in mount_hole_centers:
        # Add rivets on each side of the mounting hole (along x-axis)
        msp.add_circle(
            (hole_center[0] - spacing, hole_center[1]),
            rivet_diameter / 2,
        )
        msp.add_circle(
            (hole_center[0] + spacing, hole_center[1]),
            rivet_diameter / 2,
        )


def save_files(doc, filename):
    """
    Save the document as DXF and as PNG with standardized settings.

    Args:
        doc: ezdxf document
        filename: base filename without extension
    """
    # Save DXF file
    doc.saveas(f"{filename}.dxf")

    # Export PNG with standardized settings
    export_png = True

    # Export PNG
    if export_png:
        dpi = 600
        extents = bbox.extents(doc.modelspace())
        width = extents.extmax.x - extents.extmin.x
        height = extents.extmax.y - extents.extmin.y

        scale_factor = 32/29  # Adjusted to correct 29/32" printing to 1"

        width_inches = width * scale_factor
        height_inches = height * scale_factor

        # Print dimensions for debugging (remove this in production)
        print(
            f'Image dimensions for {filename}.png: {width_inches}" x {height_inches}"'
        )

        fig_args = {"bg": "#FFFFFF", "dpi": dpi}
        fig_args["size_inches"] = (width_inches, height_inches)

        # Add a calibration box to verify scale
        msp = doc.modelspace()
        # Add a rectangle that is exactly 1 inch square (to verify scale)
        cal_x = extents.extmin.x + 0.1
        cal_y = extents.extmin.y + 0.1

        square_size = 1.0

        text = msp.add_text("1 INCH SQUARE →", height=0.1)
        text.dxf.insert = (cal_x, cal_y + 0.05)
        msp.add_line(
            (cal_x + 0.25, cal_y), (cal_x + 0.25 + square_size, cal_y)
        )  # bottom
        msp.add_line(
            (cal_x + 0.25, cal_y + square_size),
            (cal_x + 0.25 + square_size, cal_y + square_size),
        )  # top
        msp.add_line((cal_x + 0.25, cal_y), (cal_x + 0.25, cal_y + square_size))  # left
        msp.add_line(
            (cal_x + 0.25 + square_size, cal_y),
            (cal_x + 0.25 + square_size, cal_y + square_size),
        )  # right

        matplotlib.qsave(
            doc.modelspace(),
            f"{filename}.pdf",
            **fig_args,
        )

    return f"{filename}.dxf"
