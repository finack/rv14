// R4 Radius Gauge Template
// Isoceles triangle with 45° apex angle.
// Two straight sides; base is a convex arc with R = 4" = 101.6mm curving outward.
// Thickness: 4mm
//
// Usage: press the convex base arc into the inside of a bend
// to verify a 4-inch (101.6mm) radius. Arc should seat flush with no gap.

// ========== Parameters ==========

R_arc      = 101.6;  // Arc radius: 4 inches in mm
leg        = 127.0;  // Length of each straight side: 5 inches
apex_angle =  45.0;  // Apex angle in degrees
r_corner   =   5.0;  // Corner roundover radius
thickness  =   4.0;  // Part thickness: 4mm

// ========== Derived Dimensions ==========

half_angle = apex_angle / 2;

// Chord length across the base (distance between the two base corners)
chord = 2 * leg * sin(half_angle);

// Height from apex down to the base chord
tri_height = leg * cos(half_angle);

// Vertex positions: apex at top, base corners at bottom, centered on X axis
V_apex  = [         0,           0 ];
V_left  = [ -chord / 2, -tri_height ];
V_right = [  chord / 2, -tri_height ];

// Distance from base chord to arc center (arc center sits inside the triangle,
// above the base chord, so the arc curves outward/downward).
d_arc = sqrt(R_arc * R_arc - (chord / 2) * (chord / 2));

// Arc center inside the triangle, d_arc above the base chord
arc_center = [ 0, -tri_height + d_arc ];

// ========== 2D Profile ==========

module gauge_2d() {
    // Round all convex corners (including the arc-to-straight junctions at the
    // base corners) using erosion-then-dilation.
    offset(r = r_corner, $fn = 64)
    offset(r = -r_corner)
    union() {
        // Solid triangle
        polygon([ V_apex, V_left, V_right ]);
        // Add the circular segment below the base chord to form the outward arc
        intersection() {
            translate(arc_center) circle(R_arc, $fn = 256);
            // Half-plane below the base chord: top edge at y = -tri_height,
            // extending downward by R_arc (more than enough for the arc sag)
            translate([ -R_arc, -tri_height - R_arc ])
                square([ 2 * R_arc, R_arc ]);
        }
    }
}

// ========== Render ==========

linear_extrude(height = thickness)
    gauge_2d();
