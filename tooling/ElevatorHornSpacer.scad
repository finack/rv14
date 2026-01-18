// Elevator Horn Spacer
// Dimensions: 12.5mm x 5.8mm x 7.5mm

// ========== Parameters ==========

width = 12.5;   // X dimension
depth = 5.8;    // Y dimension
height = 7.5;   // Z dimension

// Text parameters
text_line1 = "HORN";
text_line2 = "SPACER";
text_size = 2;          // Font size in mm
text_depth = 0.5;       // How deep to emboss
text_font = "Liberation Sans:style=Bold";
line_spacing = 0.5;     // Gap between lines

// Color parameters
body_color = "SteelBlue";
text_color = "White";

// ========== Modules ==========

module text_shape() {
    // 2D text shape - two lines centered
    line_height = text_size + line_spacing;

    // Line 1 (HORN) - upper
    translate([0, line_height/2])
        text(text_line1, size = text_size, font = text_font,
             halign = "center", valign = "center");

    // Line 2 (SPACER) - lower
    translate([0, -line_height/2])
        text(text_line2, size = text_size, font = text_font,
             halign = "center", valign = "center");
}

module embossed_text() {
    // Position text centered on the front face (Y=0)
    // Rotate to stand upright on the XZ plane
    translate([width/2, -0.01, height/2])
        rotate([90, 0, 0])
            linear_extrude(height = text_depth + 0.01)
                text_shape();
}

module text_inlay() {
    // Inlay piece that fits into the embossed area
    // Slightly thinner than emboss depth for fit
    inlay_thickness = text_depth - 0.1;
    translate([width/2, inlay_thickness - 0.01, height/2])
        rotate([90, 0, 0])
            linear_extrude(height = inlay_thickness)
                text_shape();
}

// ========== Main Assembly ==========

module elevator_horn_spacer_body() {
    difference() {
        cube([width, depth, height]);
        embossed_text();
    }
}

module elevator_horn_spacer() {
    color(body_color) elevator_horn_spacer_body();
    color(text_color) text_inlay();
}

// ========== Render ==========

// Full assembly with colors (for preview)
elevator_horn_spacer();

// Export these separately for multi-color printing:
//elevator_horn_spacer_body();
//text_inlay();
