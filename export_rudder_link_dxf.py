#!/usr/bin/env python3
"""Render the SCAD flat profile, then export one exact-arc inch DXF.

Order quantity 4 in 0.050-inch 4130 steel. OpenSCAD is required; on macOS
the agent may need approval to run it outside its sandbox.
"""

import argparse
import math
import subprocess
import tempfile
from pathlib import Path

import ezdxf
from ezdxf import appsettings

from export_avionics_tray_dxf import find_openscad, bounding_box, polygon_area


def export(source: Path, output: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="rudder-link-") as temporary:
        raw_path = Path(temporary) / "flat.dxf"
        subprocess.run(
            [str(find_openscad()), "-o", str(raw_path), "-D",
             'render_mode="flat"', str(source.resolve())], check=True,
        )
        raw = ezdxf.readfile(raw_path)

    contours = []
    for entity in raw.modelspace():
        if entity.dxftype() != "LWPOLYLINE" or not entity.closed:
            raise ValueError("Expected closed OpenSCAD polylines.")
        contours.append([(x / 25.4, y / 25.4)
                         for x, y in entity.get_points("xy")])
    if len(contours) < 3:
        raise ValueError("Expected an outline and at least two holes.")
    outer = max(contours, key=polygon_area)
    x0, y0, x1, y1 = bounding_box(outer)
    radius = (y1 - y0) / 2
    left, right, cy = x0 + radius, x1 - radius, (y0 + y1) / 2
    if radius <= 0 or right <= left:
        raise ValueError("Invalid capsule dimensions.")
    # Check every rendered outline vertex against the analytic capsule.
    for x, y in outer:
        nearest_x = min(max(x, left), right)
        if abs(math.hypot(x - nearest_x, y - cy) - radius) > 0.0001:
            raise ValueError("Outline is not a capsule; update this exporter.")

    doc = ezdxf.new("R2013")
    doc.units = 1
    doc.header["$MEASUREMENT"] = 0
    doc.layers.add("CUT")
    msp = doc.modelspace()
    # CCW: bottom edge, right semicircle, top edge, left semicircle.
    msp.add_lwpolyline(
        [(left, y0, 0), (right, y0, 1),
         (right, y1, 0), (left, y1, 1)],
        format="xyb", close=True, dxfattribs={"layer": "CUT"},
    )
    for points in contours:
        if points is outer:
            continue
        hx0, hy0, hx1, hy1 = bounding_box(points)
        hx, hy = (hx0 + hx1) / 2, (hy0 + hy1) / 2
        hr = (hx1 - hx0) / 2
        if (hr <= 0 or abs((hy1 - hy0) / 2 - hr) > 0.0001
                or abs(hy - cy) > 0.0001
                or hx - hr <= x0 or hx + hr >= x1
                or hr >= radius
                or any(abs(math.hypot(x - hx, y - hy) - hr) > 0.0001
                       for x, y in points)):
            raise ValueError("Expected circular centerline holes inside the link.")
        msp.add_circle((hx, hy), hr, dxfattribs={"layer": "CUT"})
    appsettings.update_extents(doc)
    audit = doc.audit()
    if audit.errors or audit.fixes:
        raise ValueError("DXF failed audit.")
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(output)
    print(f"Wrote {output}: {x1-x0:.6f} x {y1-y0:.6f} inches, "
          f"{len(contours)-1} circular holes. Order quantity 4.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).with_name("RudderLinkExtension.scad"))
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("build")
                        / "RudderLinkExtension-sendcutsend.dxf")
    args = parser.parse_args()
    export(args.source, args.output)
