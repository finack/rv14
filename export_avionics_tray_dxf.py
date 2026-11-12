#!/usr/bin/env python3
"""Export a SendCutSend-friendly 5052-H32 inch DXF from AvionicsTray.scad.

OpenSCAD models in millimetres and its DXF exporter can emit a legacy-version
header with newer LWPOLYLINE entities and no explicit drawing units. This
script renders the OpenSCAD flat pattern, converts it to inches, replaces the
polygonal racetrack slots with exact line-and-arc polylines, and writes a
consistent AutoCAD 2013 DXF with explicit inch units.
"""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import ezdxf
from ezdxf import appsettings


MM_PER_INCH = 25.4
EXPECTED_SLOT_COUNT = 14
EXPECTED_HEIGHT_IN = 10.5
EXPECTED_SLOT_LENGTH_IN = 1.5
EXPECTED_SLOT_WIDTH_IN = 0.5
TRAY_LENGTH_IN = 13.0
TRAY_WIDTH_IN = 5.5
RAIL_LENGTH_IN = 10.5
FORWARD_FLAT_CLEARANCE_IN = 1.0
TRAY_FORWARD_OFFSET_IN = 0.5
FORMED_LIP_HEIGHT_IN = 0.375
BEND_DEDUCTION_IN = 0.116
FLAT_LIP_WIDTH_IN = FORMED_LIP_HEIGHT_IN - BEND_DEDUCTION_IN / 2
SIDE_FLANGE_HEIGHT_IN = 0.375
SIDE_FLAT_LIP_WIDTH_IN = SIDE_FLANGE_HEIGHT_IN - BEND_DEDUCTION_IN / 2
SIDE_BEND_RELIEF_IN = 0.375
EXPECTED_WIDTH_IN = TRAY_LENGTH_IN + 2 * FLAT_LIP_WIDTH_IN
DIMENSION_TOLERANCE_IN = 0.002


def find_openscad() -> Path:
    """Find the OpenSCAD command-line executable."""
    command = shutil.which("openscad")
    if command:
        return Path(command)

    macos_app_binary = Path("/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD")
    if macos_app_binary.is_file():
        return macos_app_binary

    raise FileNotFoundError(
        "OpenSCAD was not found in PATH or /Applications/OpenSCAD.app."
    )


def render_flat_pattern(source: Path, destination: Path) -> None:
    """Render the flat 2D cut profile using OpenSCAD."""
    command = [
        str(find_openscad()),
        "-o",
        str(destination),
        "-D",
        'render_mode="flat"',
        str(source),
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        # Some universal macOS OpenSCAD/Qt builds fail their native ARM CPU
        # feature check but run normally through the bundled x86_64 slice.
        if sys.platform != "darwin" or platform.machine() != "arm64":
            raise
        subprocess.run(["arch", "-x86_64", *command], check=True)


def polyline_points(entity: ezdxf.entities.LWPolyline) -> list[tuple[float, float]]:
    """Return an LWPOLYLINE's XY points as ordinary floats."""
    return [(float(x), float(y)) for x, y in entity.get_points("xy")]


def bounding_box(points: list[tuple[float, float]]) -> tuple[float, float, float, float]:
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return min(xs), min(ys), max(xs), max(ys)


def polygon_area(points: list[tuple[float, float]]) -> float:
    """Return the absolute shoelace area for a closed polygon."""
    return abs(
        sum(
            x1 * y2 - x2 * y1
            for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1])
        )
        / 2
    )


def validate_racetrack_polygon(
    points: list[tuple[float, float]],
) -> tuple[float, float]:
    """Validate an OpenSCAD slot contour and return its centre in inches."""
    min_x_mm, min_y_mm, max_x_mm, max_y_mm = bounding_box(points)
    length_in = (max_x_mm - min_x_mm) / MM_PER_INCH
    width_in = (max_y_mm - min_y_mm) / MM_PER_INCH

    if abs(length_in - EXPECTED_SLOT_LENGTH_IN) > DIMENSION_TOLERANCE_IN:
        raise ValueError(f"Unexpected racetrack length: {length_in:.6f} inches.")
    if abs(width_in - EXPECTED_SLOT_WIDTH_IN) > DIMENSION_TOLERANCE_IN:
        raise ValueError(f"Unexpected racetrack width: {width_in:.6f} inches.")

    return (
        (min_x_mm + max_x_mm) / (2 * MM_PER_INCH),
        (min_y_mm + max_y_mm) / (2 * MM_PER_INCH),
    )


def write_clean_dxf(raw_dxf: Path, output: Path) -> None:
    """Convert an OpenSCAD DXF to a clean, explicit inch-unit DXF."""
    raw_document = ezdxf.readfile(raw_dxf)
    entities = list(raw_document.modelspace())

    if not entities or any(entity.dxftype() != "LWPOLYLINE" for entity in entities):
        raise ValueError("Expected only LWPOLYLINE entities from OpenSCAD.")
    if any(not entity.closed for entity in entities):
        raise ValueError("OpenSCAD produced an open contour.")

    contours = [(entity, polyline_points(entity)) for entity in entities]
    outer_entity, outer_points_mm = max(contours, key=lambda item: polygon_area(item[1]))
    del outer_entity

    slot_contours = [points for _, points in contours if points is not outer_points_mm]
    if len(slot_contours) != EXPECTED_SLOT_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_SLOT_COUNT} lightening slots, "
            f"found {len(slot_contours)}."
        )

    outer_points_in = [
        (x / MM_PER_INCH, y / MM_PER_INCH) for x, y in outer_points_mm
    ]
    min_x, min_y, max_x, max_y = bounding_box(outer_points_in)
    width = max_x - min_x
    height = max_y - min_y

    if abs(width - EXPECTED_WIDTH_IN) > DIMENSION_TOLERANCE_IN:
        raise ValueError(f"Unexpected flat-pattern width: {width:.6f} inches.")
    if abs(height - EXPECTED_HEIGHT_IN) > DIMENSION_TOLERANCE_IN:
        raise ValueError(f"Unexpected flat-pattern height: {height:.6f} inches.")

    clean_document = ezdxf.new("R2013", setup=False)
    clean_document.header["$INSUNITS"] = 1  # Inches
    clean_document.header["$MEASUREMENT"] = 0  # English
    clean_document.layers.add("CUT", color=7)
    clean_document.linetypes.add(
        "DASHED",
        pattern=[0.2, 0.1, -0.1],
        description="Bend reference line",
    )
    clean_document.layers.add("BEND", color=1, linetype="DASHED")
    modelspace = clean_document.modelspace()

    modelspace.add_lwpolyline(
        outer_points_in,
        close=True,
        dxfattribs={"layer": "CUT"},
    )

    slot_centres = [
        validate_racetrack_polygon(points_mm) for points_mm in slot_contours
    ]
    row_counts: list[int] = []
    for _, center_y_in in sorted(slot_centres, key=lambda point: point[1]):
        if not row_counts:
            row_counts.append(1)
            previous_y = center_y_in
        elif abs(center_y_in - previous_y) <= DIMENSION_TOLERANCE_IN:
            row_counts[-1] += 1
        else:
            row_counts.append(1)
            previous_y = center_y_in
    if row_counts != [5, 4, 5]:
        raise ValueError(f"Unexpected racetrack row counts: {row_counts}.")

    slot_radius = EXPECTED_SLOT_WIDTH_IN / 2
    end_center_offset = (EXPECTED_SLOT_LENGTH_IN - EXPECTED_SLOT_WIDTH_IN) / 2
    for center_x_in, center_y_in in slot_centres:
        if not (
            min_x + EXPECTED_SLOT_LENGTH_IN / 2 < center_x_in
            < max_x - EXPECTED_SLOT_LENGTH_IN / 2
            and min_y + slot_radius < center_y_in < max_y - slot_radius
        ):
            raise ValueError("A lightening slot is not contained by the part extents.")

        # Bulge 1.0 is a counter-clockwise 180-degree arc. The resulting
        # four-vertex closed polyline contains two straight sides and two
        # exact semicircular ends.
        modelspace.add_lwpolyline(
            [
                (center_x_in - end_center_offset, center_y_in - slot_radius, 0.0),
                (center_x_in + end_center_offset, center_y_in - slot_radius, 1.0),
                (center_x_in + end_center_offset, center_y_in + slot_radius, 0.0),
                (center_x_in - end_center_offset, center_y_in + slot_radius, 1.0),
            ],
            format="xyb",
            close=True,
            dxfattribs={"layer": "CUT"},
        )

    rail_y_min = (
        (TRAY_WIDTH_IN - RAIL_LENGTH_IN) / 2 - TRAY_FORWARD_OFFSET_IN
    )
    # The end-rail bend begins at the aft free edge and stops one inch before
    # the forward rail tip. There are no cut relief notches in this flange.
    bend_y_min = rail_y_min
    bend_y_max = rail_y_min + RAIL_LENGTH_IN - FORWARD_FLAT_CLEARANCE_IN
    for bend_x in (0.0, TRAY_LENGTH_IN):
        modelspace.add_line(
            (bend_x, bend_y_min),
            (bend_x, bend_y_max),
            dxfattribs={"layer": "BEND", "linetype": "DASHED", "color": 1},
        )

    side_bend_x_min = 1.0 + SIDE_BEND_RELIEF_IN
    side_bend_x_max = TRAY_LENGTH_IN - 1.0 - SIDE_BEND_RELIEF_IN
    for bend_y in (0.0, TRAY_WIDTH_IN):
        modelspace.add_line(
            (side_bend_x_min, bend_y),
            (side_bend_x_max, bend_y),
            dxfattribs={"layer": "BEND", "linetype": "DASHED", "color": 1},
        )

    # ezdxf rewrites HEADER extents from the modelspace layout during save.
    # Populate the layout values and calculate header extents after all
    # entities exist so importers do not see the unset +/-1e20 sentinels.
    modelspace.dxf.extmin = (min_x, min_y, 0)
    modelspace.dxf.extmax = (max_x, max_y, 0)
    modelspace.dxf.limmin = (min_x, min_y)
    modelspace.dxf.limmax = (max_x, max_y)
    appsettings.update_extents(clean_document)

    output.parent.mkdir(parents=True, exist_ok=True)
    clean_document.saveas(output)

    print(f"Wrote {output}")
    print(f"Units: inches; extents: {width:.3f} x {height:.3f}")
    print(
        "Entities: 1 closed outer LWPOLYLINE, 14 closed racetrack "
        "LWPOLYLINE slots, 4 LINE bend marks"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).with_name("AvionicsTray.scad"),
        help="OpenSCAD source file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("build")
        / "AvionicsTray-sendcutsend.dxf",
        help="Destination DXF path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.source.resolve()
    output = args.output.resolve()

    with tempfile.TemporaryDirectory(prefix="avionics-tray-") as temporary_directory:
        raw_dxf = Path(temporary_directory) / "AvionicsTray-openscad.dxf"
        render_flat_pattern(source, raw_dxf)
        write_clean_dxf(raw_dxf, output)


if __name__ == "__main__":
    main()
