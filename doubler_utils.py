"""
Utility functions for aircraft doubler plate designs.
"""
import ezdxf
from ezdxf.addons.drawing import matplotlib

def create_document():
    """Create a new DXF document with R2010 version."""
    doc = ezdxf.new(dxfversion="R2010")
    # Add dashed linetype
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

def save_files(doc, filename, export_png=True, dpi=300):
    """
    Save the document as DXF and optionally as PNG.
    
    Args:
        doc: ezdxf document
        filename: base filename without extension
        export_png: whether to export PNG file
        dpi: resolution for PNG output
    """
    # Save DXF file
    doc.saveas(f"{filename}.dxf")
    
    # Export PNG if requested
    if export_png:
        matplotlib.qsave(doc.modelspace(), f"{filename}.png", dpi=dpi, bg="#FFFFFF")
    
    return f"{filename}.dxf"