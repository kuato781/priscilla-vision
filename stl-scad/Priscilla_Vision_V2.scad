/*
Priscilla Vision — double-ball adapter, V2 (PETG FIT PROTOTYPE)
Dimensions in millimeters. Based on the user's measured 15.75 mm kit ball,
20.75 mm Voyager ball, 85/30 mm nominal spans, and approximately 90° elbow.

NOT LOAD-RATED. Do not use on-road until tested/verified; final ASA to be
professionally printed. All arm lengths below refer to ball CENTER to elbow
CENTER, not straight neck lengths; edit as needed after mockup.
*/
$fn = 36;

// MEASURED BALL DIAMETERS
kit_ball_d = 15.75;
voyager_ball_d = 20.75;

// V1 INTERPRETATION OF SKETCH; easily adjustable
long_span = 85;             // elbow center to kit ball center, via final bent neck
short_span = 30;            // elbow center to Voyager ball center
elbow_angle_deg = 90;       // included angle between main and short arm directions
long_tilt_from_vertical = 12; // long arm leans left relative to vertical
kit_tip_kink_deg = 30;     // final neck turns left relative to main long arm
kit_tip_length = 10;       // length of angled end portion

// NECKS, SELECTED FOR V1, NOT MEASURED
long_neck_d = 8.0;
short_neck_d = 9.0;
elbow_reinforcement_d = 13.0;

// Coordinate system: long shaft rises (+Y) and leans left (-X);
// Voyager-side short shaft extends left (mostly -X).
function vadd(a,b) = [a[0]+b[0],a[1]+b[1],a[2]+b[2]];
function vmul(a,s) = [a[0]*s,a[1]*s,a[2]*s];
function vlen(a) = sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2]);
function uangle(deg) = [cos(deg),sin(deg),0];

elbow = [0,0,0];
long_dir_angle = 90 + long_tilt_from_vertical;
short_dir_angle = long_dir_angle + elbow_angle_deg;
kit_tip_dir_angle = long_dir_angle + kit_tip_kink_deg;

// Nominal 85 mm polyline from elbow to kit ball center.
kit_bend = vadd(elbow,vmul(uangle(long_dir_angle),long_span-kit_tip_length));
kit_ball = vadd(kit_bend,vmul(uangle(kit_tip_dir_angle),kit_tip_length));
voyager_ball = vadd(elbow,vmul(uangle(short_dir_angle),short_span));

module bead(p,r) { translate(p) sphere(r=r); }
module rounded_segment(a,b,r1,r2) {
    hull() { bead(a,r1); bead(b,r2); }
}

union() {
    // Rounded reinforced elbow blends into both shafts.
    rounded_segment(elbow,kit_bend,elbow_reinforcement_d/2,long_neck_d/2);
    rounded_segment(kit_bend,kit_ball,long_neck_d/2,long_neck_d/2);
    rounded_segment(elbow,voyager_ball,elbow_reinforcement_d/2,short_neck_d/2);
    bead(kit_ball,kit_ball_d/2);
    bead(voyager_ball,voyager_ball_d/2);
}
