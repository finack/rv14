// Drill Guide Block
// Dimensions: 31.8mm x 50.8mm x 25mm

// ========== Parameters ==========

width = 31.8;    // X dimension
height = 50.8;   // Z dimension (tall)
// Thickness depends on gap between elevator horns
thickness = 25;  // Y dimension (depth)

// Hole parameters
// #12 drill bit = 0.189" = 4.8mm
hole_diameter = 4.8;
hole_from_bottom = 12.7;  // Z position from bottom
hole_from_side = 15.9;    // X position from left side

// ========== Main Assembly ==========

module drill_guide_block() {
    difference() {
        // Main block
        cube([width, thickness, height]);

        // #12 hole through the thickness (Y axis)
        translate([hole_from_side, -0.01, hole_from_bottom])
            rotate([-90, 0, 0])
                cylinder(h = thickness + 0.02, d = hole_diameter, $fn = 32);
    }
}

// ========== Render ==========

drill_guide_block();
