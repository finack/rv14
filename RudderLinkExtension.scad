// Extended CS-00015-style rudder cable links, based on:
// https://rv-14a.blogspot.com/2017/10/fuselage-rudder-and-brake-systems.html
// Extended to ten total holes as requested; one more than the blog version.
// Reproduction of a builder's dimensions, not a Van's approved drawing.
// Compare spacing with your kit links and verify suitability with Van's.
// Material: 0.050-inch 4130 steel. Four individual links make one set.
// Holes default to nominal finished #12 diameter, 0.189 inch.
// No waterjet width allowance or kerf compensation is added.
// Use export_rudder_link_dxf.py for an inch-unit, exact-arc ordering DXF.

render_mode = "set"; // [set, single, flat]
quantity = 4;
width_in = 0.5;
thickness_in = 0.050;
hole_count = 10;
first_spacing_in = 0.75;
adjustment_spacing_in = 0.34375; // 11/32; author also suggests checking 0.3445
finished_hole_diameter_in = 0.189;
hole_allowance_in = 0; // Nominal finished holes; 0.015625 leaves 1/64 for drilling
display_gap_in = 0.25;

inch = 25.4;
$fn = 128;
radius_in = width_in / 2;
last_center_in = radius_in + first_spacing_in
                 + (hole_count - 2) * adjustment_spacing_in;
length_in = last_center_in + radius_in;
cut_hole_diameter_in = finished_hole_diameter_in - hole_allowance_in;

function hole_x_in(i) = i == 0 ? radius_in
    : radius_in + first_spacing_in + (i - 1) * adjustment_spacing_in;

assert(render_mode == "set" || render_mode == "single" || render_mode == "flat");
assert(quantity >= 1 && quantity == floor(quantity));
assert(hole_count >= 2 && hole_count == floor(hole_count));
assert(thickness_in > 0 && width_in > finished_hole_diameter_in);
assert(hole_allowance_in >= 0 && cut_hole_diameter_in > 0);
assert(first_spacing_in > finished_hole_diameter_in);
assert(adjustment_spacing_in > finished_hole_diameter_in);
assert(display_gap_in > 0);

// Geometry is in mm, with the lower-left extent at the origin.
module link_2d() {
    scale([inch, inch])
        difference() {
            hull() {
                translate([radius_in, radius_in]) circle(r = radius_in);
                translate([last_center_in, radius_in]) circle(r = radius_in);
            }
            for (i = [0 : hole_count - 1])
                translate([hole_x_in(i), radius_in])
                    circle(d = cut_hole_diameter_in);
        }
}

echo("Link length (in)", length_in);
echo("Cut hole diameter (in)", cut_hole_diameter_in);

if (render_mode == "flat") {
    link_2d();
} else {
    for (i = [0 : (render_mode == "set" ? quantity : 1) - 1])
        translate([0, i * (width_in + display_gap_in) * inch, 0])
            linear_extrude(height = thickness_in * inch) link_2d();
}
