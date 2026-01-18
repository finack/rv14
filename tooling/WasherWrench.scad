// Washer Wrench for AN960 Aviation Washers
// Designed for #6, #8, and #10 washers
// Print with PLA on Bambu H2S

// ========== Parameters ==========

// Overall dimensions
total_length = 150;      // 6 inches in mm
end_width = 25;          // Width at the forked ends
middle_width = 15;       // Width at the narrowest point (center)
thickness = 2;

// AN960 Washer dimensions (in mm)
// Format: [ID, OD]
washer_6 = [3.78, 9.53];   // #6: ID 0.149", OD 0.375"
washer_8 = [4.47, 11.13];  // #8: ID 0.176", OD 0.438"
washer_10 = [5.16, 12.70]; // #10: ID 0.203", OD 0.500"

// Fork slot parameters
slot_clearance = 0.5;     // Extra clearance for slot width
// Fork depth is calculated as 1/2 washer OD for each slot

// Relief slit parameters
slit_width = 2.5;         // Width of the relief slits
slit_inset = 0;           // Distance from fork end to slit start
slit_gap = 40;            // Gap between slits at center (for center hole)

// Center hole
center_hole_dia = 6;

// ========== Modules ==========

// Creates the main body outline as a 2D shape
module body_outline() {
    hull() {
        // Left end
        translate([-total_length/2 + end_width/2, 0])
            circle(r = end_width/2, $fn=60);

        // Center - narrower
        circle(r = middle_width/2, $fn=60);

        // Right end
        translate([total_length/2 - end_width/2, 0])
            circle(r = end_width/2, $fn=60);
    }
}

// Fork slot that opens at the end - creates the gap between tines
// slot_width: width of the opening (must be > washer OD)
module open_fork_slot(slot_width, depth) {
    // Slot extends from edge into body
    hull() {
        // Opening extends past edge
        translate([-10, -slot_width/2])
            square([1, slot_width]);
        // Rounded inner end
        translate([depth, 0])
            circle(r = slot_width/2, $fn=40);
    }
}

// Relief slit - runs from near fork toward center
module relief_slit(length, width) {
    hull() {
        circle(r = width/2, $fn=30);
        translate([length, 0])
            circle(r = width/2, $fn=30);
    }
}

// ========== Main Assembly ==========

module washer_wrench_2d() {
    // Calculate slot widths for each washer size
    slot_width_8 = washer_8[1] + slot_clearance;   // For #6/#8 end (use #8 size)
    slot_width_10 = washer_10[1] + slot_clearance; // For #10 end

    // Fork depth = 1/2 washer OD
    fork_depth_8 = washer_8[1] / 2;
    fork_depth_10 = washer_10[1] / 2;

    // Calculate slit lengths (from near fork to near center)
    slit_length_left = total_length/2 - slit_inset - fork_depth_8 - slit_gap/2;
    slit_length_right = total_length/2 - slit_inset - fork_depth_10 - slit_gap/2;

    difference() {
        // Main body
        body_outline();

        // Left fork slot (#6/#8 - use larger #8 slot, works for both)
        translate([-total_length/2, 0])
            open_fork_slot(slot_width_8, fork_depth_8);

        // Right fork slot (#10)
        translate([total_length/2, 0])
            mirror([1, 0])
                open_fork_slot(slot_width_10, fork_depth_10);

        // Left relief slit (runs from near left fork toward center)
        translate([-total_length/2 + slit_inset + fork_depth_8, 0])
            relief_slit(slit_length_left, slit_width);

        // Right relief slit (runs from near right fork toward center)
        translate([slit_gap/2, 0])
            relief_slit(slit_length_right, slit_width);

        // Center hole
        circle(d = center_hole_dia, $fn=40);
    }
}

// 3D extrusion
module washer_wrench() {
    linear_extrude(height = thickness)
        washer_wrench_2d();
}

// ========== Render ==========

washer_wrench();

// Uncomment to see 2D profile only:
// washer_wrench_2d();
