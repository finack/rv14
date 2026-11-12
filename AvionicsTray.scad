// RV-14 lightweight avionics tray
//
// One-piece 5052-H32 sheet concept with integrated 10.5-inch cross-rails.
// The rail faces remain coplanar with the tray. A shallow downturned lip runs
// from the aft rail edge to a 1-inch flat clearance at the forward rail tip.
// Two additional downturned flanges stiffen the 11-inch long edges between
// the end rails. Mounting holes are intentionally omitted.
//
// Export examples:
//   Formed STL:
//     openscad -o AvionicsTray.stl AvionicsTray.scad
//   SendCutSend upload DXF (inch units, clean entities, and bend lines):
//     python3 export_avionics_tray_dxf.py
//
// Do not upload OpenSCAD's raw DXF directly. OpenSCAD exports unitless mm
// coordinates with a legacy DXF header that some quoting systems misread.
//
// Bend values below match SendCutSend's published 0.080-inch 5052-H32,
// 90-degree specifications as checked September 2026.

$fn = 96;

// ---------- Display ----------

render_mode = "formed"; // [formed, flat, bend_reference]

// ---------- Primary dimensions (inches) ----------

tray_length_in = 13;
tray_width_in = 5.5;
solid_border_in = 1.5;

rail_length_in = 10.5;
rail_depth_in = 1;
forward_flat_clearance_in = 1;
tray_forward_offset_in = 0.5;

sheet_thickness_in = 0.080;
formed_lip_height_in = 0.375;
side_flange_height_in = 0.375;
side_bend_relief_in = 0.375;
flange_corner_radius_in = 0.125;
inside_bend_radius_in = 0.038;
k_factor = 0.48;
bend_angle_deg = 90;
bend_deduction_in = 0.116;
bend_reference_width_in = 0.010;

// Bend lines are placed half the bend deduction inboard from the desired
// formed flange apex dimension.
flat_lip_width_in = formed_lip_height_in - bend_deduction_in / 2;
side_flat_lip_width_in = side_flange_height_in - bend_deduction_in / 2;

// ---------- Lightening-slot pattern ----------

slot_length_in = 1.5;
slot_width_in = 0.5;
outer_row_slots = 5;
middle_row_slots = 4;

// ---------- Unit conversion ----------

inch = 25.4;

tray_length = tray_length_in * inch;
tray_width = tray_width_in * inch;
solid_border = solid_border_in * inch;

rail_length = rail_length_in * inch;
rail_depth = rail_depth_in * inch;
forward_flat_clearance = forward_flat_clearance_in * inch;
tray_forward_offset = tray_forward_offset_in * inch;

sheet_thickness = sheet_thickness_in * inch;
formed_lip_height = formed_lip_height_in * inch;
flat_lip_width = flat_lip_width_in * inch;
side_flange_height = side_flange_height_in * inch;
side_flat_lip_width = side_flat_lip_width_in * inch;
side_bend_relief = side_bend_relief_in * inch;
flange_corner_radius = flange_corner_radius_in * inch;
inside_bend_radius = inside_bend_radius_in * inch;
bend_deduction = bend_deduction_in * inch;
bend_reference_width = bend_reference_width_in * inch;

slot_length = slot_length_in * inch;
slot_width = slot_width_in * inch;

// Maximum Y is the forward edge: the end with the one-inch no-flange pad.
// Moving the tray forward shifts the rail toward negative Y in tray coordinates.
rail_y_min = (tray_width - rail_length) / 2 - tray_forward_offset;
rail_y_max = rail_y_min + rail_length;
lip_y_min = rail_y_min;
lip_y_max = rail_y_max - forward_flat_clearance;
lip_span = lip_y_max - lip_y_min;
side_lip_x_min = rail_depth;
side_lip_x_max = tray_length - rail_depth;
side_lip_span = side_lip_x_max - side_lip_x_min;
side_bend_x_min = side_lip_x_min + side_bend_relief;
side_bend_x_max = side_lip_x_max - side_bend_relief;
side_bend_span = side_bend_x_max - side_bend_x_min;

// ---------- Validation ----------

assert(tray_length > 2 * solid_border,
       "The tray length must exceed twice the solid border.");
assert(tray_width > 2 * solid_border,
       "The tray width must exceed twice the solid border.");
assert(rail_length >= tray_width,
       "The rail must be at least as long as the tray is wide.");
assert(rail_depth <= solid_border,
       "Rail depth must not extend into the lightening-hole field.");
assert(forward_flat_clearance < rail_length,
       "The forward clearance leaves no room for a stiffening lip.");
assert(formed_lip_height_in >= 0.254,
       "SendCutSend requires at least a 0.254-inch flange for this stock.");
assert(side_flange_height_in >= 0.254,
       "SendCutSend requires at least a 0.254-inch side flange for this stock.");
assert(side_bend_relief > side_flat_lip_width,
       "The side relief must extend beyond the long-edge bend line.");
assert(side_bend_span > 0,
       "The side bend reliefs leave no long-edge flange between them.");
assert(2 * flange_corner_radius < flat_lip_width,
       "The corner radius is too large for the end-rail flange blank.");
assert(2 * flange_corner_radius < side_flat_lip_width,
       "The corner radius is too large for the long-edge flange blank.");
assert(3 * slot_width <= tray_width - 2 * solid_border,
       "The three lightening-slot rows do not fit inside the solid border.");
assert(slot_length < tray_length - 2 * solid_border,
       "The lightening slots do not fit inside the solid border.");

// ---------- 2D geometry ----------

module rounded_rectangle_2d(size, radius) {
    offset(r = radius)
        offset(delta = -radius)
            square(size);
}

module rail_top_profiles_2d() {
    // Integrated end rails occupy the one-inch solid end borders and extend
    // equally beyond both long sides of the tray.
    translate([0, rail_y_min])
        square([rail_depth, rail_length]);

    translate([tray_length - rail_depth, rail_y_min])
        square([rail_depth, rail_length]);
}

module formed_top_outline_2d() {
    union() {
        square([tray_length, tray_width]);
        rail_top_profiles_2d();
    }
}

module flat_lip_profiles_2d() {
    // Developed lip strips. Their width is deliberately independent of the
    // displayed formed height so a measured bend allowance can be applied.
    translate([-flat_lip_width, lip_y_min])
        rounded_rectangle_2d(
            [flat_lip_width, lip_span],
            flange_corner_radius
        );

    translate([tray_length, lip_y_min])
        rounded_rectangle_2d(
            [flat_lip_width, lip_span],
            flange_corner_radius
        );

    // Long-edge flange strips stop at the inside edges of the end rails so
    // their bend lines do not intersect the cross-rail bend lines.
    translate([side_bend_x_min, -side_flat_lip_width])
        rounded_rectangle_2d(
            [side_bend_span, side_flat_lip_width],
            flange_corner_radius
        );

    translate([side_bend_x_min, tray_width])
        rounded_rectangle_2d(
            [side_bend_span, side_flat_lip_width],
            flange_corner_radius
        );
}

module flat_outline_2d() {
    union() {
        formed_top_outline_2d();
        flat_lip_profiles_2d();
    }
}

module racetrack_slot_2d() {
    end_center_offset = (slot_length - slot_width) / 2;

    hull() {
        translate([-end_center_offset, 0])
            circle(d = slot_width);
        translate([end_center_offset, 0])
            circle(d = slot_width);
    }
}

module slot_row(row_y, slot_count, stagger = false) {
    x_min = solid_border + slot_length / 2;
    x_max = tray_length - solid_border - slot_length / 2;
    outer_pitch = (x_max - x_min) / (outer_row_slots - 1);

    if (stagger) {
        staggered_x_min = x_min + outer_pitch / 2;
        staggered_x_max = x_max - outer_pitch / 2;

        for (column = [0 : slot_count - 1])
            translate([
                staggered_x_min +
                    column * (staggered_x_max - staggered_x_min) /
                    (slot_count - 1),
                row_y
            ])
                racetrack_slot_2d();
    } else {
        for (column = [0 : slot_count - 1])
            translate([
                x_min + column * (x_max - x_min) / (slot_count - 1),
                row_y
            ])
                racetrack_slot_2d();
    }
}

module lightening_holes_2d() {
    row_y_min = solid_border + slot_width / 2;
    row_y_max = tray_width - solid_border - slot_width / 2;
    row_y_middle = tray_width / 2;

    slot_row(row_y_min, outer_row_slots);
    slot_row(row_y_middle, middle_row_slots, true);
    slot_row(row_y_max, outer_row_slots);
}

module side_bend_reliefs_2d() {
    // Four square reliefs separate the long-edge flanges from the end rails.
    // Each relief crosses the bend line slightly, preventing the bend from
    // terminating in uncut material.
    for (x = [side_lip_x_min, side_lip_x_max - side_bend_relief]) {
        translate([x, -side_flat_lip_width])
            square([side_bend_relief, side_bend_relief]);

        translate([
            x,
            tray_width + side_flat_lip_width - side_bend_relief
        ])
            square([side_bend_relief, side_bend_relief]);
    }
}

module cut_profile_2d(use_flat_outline = false) {
    difference() {
        if (use_flat_outline)
            flat_outline_2d();
        else
            formed_top_outline_2d();

        lightening_holes_2d();
        side_bend_reliefs_2d();
    }
}

module bend_reference_2d() {
    // Preview/print aid only. Do not upload this mode as a cutting DXF: the
    // red rectangles are reference marks, not cut geometry.
    color("lightgray")
        cut_profile_2d(true);

    color("red")
        for (x = [0, tray_length])
            translate([
                x - bend_reference_width / 2,
                lip_y_min
            ])
                square([
                    bend_reference_width,
                    lip_span
                ]);

    color("red")
        for (y = [0, tray_width])
            translate([
                side_bend_x_min,
                y - bend_reference_width / 2
            ])
                square([
                    side_bend_span,
                    bend_reference_width
                ]);
}

// ---------- 3D formed concept ----------

module formed_lips_3d() {
    // The two end-rail flanges bend upward from the tray plane.
    multmatrix([
        [0, 0, 1, 0],
        [1, 0, 0, lip_y_min],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])
        linear_extrude(height = sheet_thickness)
            rounded_rectangle_2d(
                [lip_span, formed_lip_height],
                flange_corner_radius
            );

    // Right/rear cross-rail outer edge.
    multmatrix([
        [0, 0, 1, tray_length - sheet_thickness],
        [1, 0, 0, lip_y_min],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])
        linear_extrude(height = sheet_thickness)
            rounded_rectangle_2d(
                [lip_span, formed_lip_height],
                flange_corner_radius
            );
}

module formed_side_flanges_3d() {
    side_lip_z_min = -side_flange_height + sheet_thickness;

    // The two long-edge flanges bend downward from the tray plane.
    translate([side_bend_x_min, 0, side_lip_z_min])
        rotate([90, 0, 0])
            linear_extrude(height = sheet_thickness)
                rounded_rectangle_2d(
                    [side_bend_span, side_flange_height],
                    flange_corner_radius
                );

    translate([
        side_bend_x_min,
        tray_width,
        side_lip_z_min + side_flange_height
    ])
        rotate([-90, 0, 0])
            linear_extrude(height = sheet_thickness)
                rounded_rectangle_2d(
                    [side_bend_span, side_flange_height],
                    flange_corner_radius
                );
}

module formed_tray() {
    union() {
        linear_extrude(height = sheet_thickness)
            cut_profile_2d(false);

        formed_lips_3d();
        formed_side_flanges_3d();
    }
}

// ---------- Output ----------

if (render_mode == "flat") {
    cut_profile_2d(true);
} else if (render_mode == "bend_reference") {
    bend_reference_2d();
} else {
    formed_tray();
}

echo(str("Tray: ", tray_length_in, " x ", tray_width_in, " inches"));
echo(str("Rail length: ", rail_length_in, " inches"));
echo(str("Forward flat clearance: ", forward_flat_clearance_in, " inch"));
echo(str("Tray offset toward forward rail tip: ", tray_forward_offset_in, " inch"));
echo(str("Sheet thickness: ", sheet_thickness_in, " inch"));
echo(str("Nominal inside bend radius: ", inside_bend_radius_in, " inch"));
echo(str("K factor: ", k_factor));
echo(str("Bend deduction: ", bend_deduction_in, " inch"));
echo(str("Formed lip height: ", formed_lip_height_in, " inch"));
echo(str("Long-edge flange height: ", side_flange_height_in, " inch"));
echo(str("Long-edge bend relief: ", side_bend_relief_in, " inch square"));
echo(str("Exposed flange corner radius: ", flange_corner_radius_in, " inch"));
echo(str("Long-edge bend length: ", side_bend_span / inch, " inches"));
echo("Bend directions: end-rail flanges UP; long-edge flanges DOWN.");
echo("Mounting holes intentionally omitted.");
