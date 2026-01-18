// Float Arm Wire Bending Tool
// For IE-F385B fuel sender float arm
// Wire: 0.090" (~2.29mm) stainless steel
// Single block with channels on different faces, bends at edges

// ========== Parameters ==========

// Wire specifications
wire_diameter = 2.29;  // 0.090 inches in mm
channel_clearance = 0.3;  // Extra clearance for wire
channel_width = wire_diameter + channel_clearance;
channel_depth = wire_diameter + 0.5;  // Deep enough to hold wire

// Bend dimensions from drawing
bend1_length = 19.5;     // Total length of tip section (first bend)
bend2_length = 95.3;     // Distance from first to second bend
bend3_length = 90.0;     // Length of diagonal section
bend3_offset = 15.1;     // Offset over the diagonal section
bend3_angle = atan(bend3_offset / bend3_length);  // ~9.53 degrees

// Block dimensions - sized to accommodate both channels
block_length = bend2_length + 10;  // Long enough for 95.3mm channel + grip
block_width = 25;                   // Width for comfortable grip
block_height = bend1_length + 10;   // Tall enough for 19.5mm channel + grip

// Reference mark dimensions
mark_depth = 0.8;
mark_width = 1;

// ========== Modules ==========

// Wire channel - U-shaped groove
module wire_channel(length) {
    translate([0, -channel_width/2, 0])
        cube([length, channel_width, channel_depth + 0.1]);
}

// Reference mark across channel
module ref_mark() {
    translate([0, -channel_width - 2, 0])
        cube([mark_width, channel_width + 4, mark_depth]);
}

// ========== Main Tool ==========

module float_arm_bend_tool() {
    difference() {
        // Main block
        cube([block_length, block_width, block_height]);

        // === Station 1: 19.5mm tip bend ===
        // Channel on TOP face, runs to the LEFT edge (X=0)
        // Position wire with 19.5mm extending past the edge, bend over edge
        translate([-0.1, block_width/2, block_height - channel_depth])
            wire_channel(bend1_length + 10);

        // Reference mark at 19.5mm from left edge
        translate([bend1_length - mark_width/2, block_width/2 - channel_width/2 - 2,
                   block_height - mark_depth])
            cube([mark_width, channel_width + 4, mark_depth + 0.1]);

        // === Relief channel for Station 1 bent wire when using Station 2 ===
        // On FRONT face (Y=0), at start of Station 2 channel, running down (-Z)
        // Accepts the already-bent tip from Station 1 when making the Station 2 bend
        translate([block_length - bend2_length - 5 - channel_width/2, -0.1, -0.1])
            cube([channel_width, channel_depth + 0.2, block_height/2 + channel_width/2 + 0.2]);

        // === Station 2: 95.3mm second bend ===
        // Channel on FRONT face (Y=0), runs to the RIGHT edge (X=block_length)
        // Position wire with reference at left, 95.3mm to right edge for bending
        translate([block_length - bend2_length - 5, -0.1, block_height/2])
            rotate([-90, 0, 0])
                wire_channel(bend2_length + 5 + 0.1);

        // Reference mark at start of 95.3mm measurement
        translate([block_length - bend2_length - mark_width/2, -0.1,
                   block_height/2 - channel_width/2 - 2])
            cube([mark_width, mark_depth + 0.1, channel_width + 4]);

        // === Station 3: Diagonal bend (15.1mm offset over 90mm) ===
        // On BACK face (Y=block_width)

        // Straight reference channel from edge to bend start point
        // This gives a reference to bend against
        bend3_start = 10;  // Where the diagonal bend begins
        bend3_z = 5;       // Z height at bend start (bottom of channel)
        translate([-0.1, block_width - channel_depth, bend3_z])
            cube([bend3_start + channel_width, channel_depth + 0.2, channel_width]);

        // Diagonal channel using hull - starts where reference channel ends
        hull() {
            // Start of diagonal at bend point (aligned with reference channel)
            translate([bend3_start, block_width - channel_depth, bend3_z])
                cube([channel_width, channel_depth + 0.2, channel_width]);
            // End of diagonal (offset by 15.1mm in Z over 90mm)
            translate([bend3_start + bend3_length, block_width - channel_depth, bend3_z + bend3_offset])
                cube([channel_width, channel_depth + 0.2, channel_width]);
        }
    }
}

// ========== Render ==========

float_arm_bend_tool();
