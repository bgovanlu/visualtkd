// Posable 3D mannequin for pose guides (three.js).
// Frame: +Y up, +Z = the way the figure faces, +X = the figure's LEFT. Units: metres (adult ≈ 1.75 m).
// A pose spec {stance, lead, arms:{L,R}} is turned into joint positions by build(); every number it uses
// can be overridden per pose (data/pose-overrides.json) from the editor in mannequin.html.
import * as THREE from "three";

export const BODY = {thigh:.44, shin:.43, upper:.30, fore:.27, hipHalf:.09, shoulderHalf:.19, spine:.50, ankleY:.075, footLen:.25};
const SW = .40;            // shoulder width: ap kubi width = SW + 2 in, length from 1½ SW (Brian, #10)
const IN = .0254;

// ---------- stances (lead foot = L; s flips everything for a right lead) ----------
// feet: ankle [x, z], yaw in degrees (0 = toes along +Z, + = toward +X), mode: flat | ball
// pelvis: [x, y, z] (y = height of the hip line), hipYaw/chestYaw/lean/sideLean/headYaw in degrees
// knee: pole direction for each knee (world), defaults to where the toes point
export const STANCES = {
  ready: s => ({feet:{lead:{at:[.15*s,0],yaw:0}, rear:{at:[-.15*s,0],yaw:0}}, pelvis:[0,.93,0]}),
  close: s => ({feet:{lead:{at:[.055*s,0],yaw:0}, rear:{at:[-.055*s,0],yaw:0}}, pelvis:[0,.94,0]}),
  // ap seogi: one natural step, legs straight, rear foot turned out a little
  walk:  s => ({feet:{lead:{at:[.07*s,.30],yaw:0}, rear:{at:[-.07*s,-.30],yaw:-20*s}}, pelvis:[0,"max",.02], lean:2}),
  // ap kubi: width = shoulder width + 2 in (feet centre to centre); front heel to rear toes = 1½ SW;
  // front shin vertical, rear leg locked straight, rear foot out 30°, hips square
  front: s => ({feet:{lead:{at:[(SW+2*IN)/2*s,.43],yaw:0}, rear:{at:[-(SW+2*IN)/2*s,-.43],yaw:-30*s}}, pelvis:"apkubi", lean:3}),
  // dwit kubi: L shape; rear foot turned 90° out; the front heel sits 1.5 in back from the rear heel line,
  // on the side away from the rear toes (#11); ~70% weight on the rear leg, rear knee out over its toes;
  // hips and chest turned toward the rear-foot side, head looks over the front foot
  back:  s => ({feet:{lead:{at:[(.06+1.5*IN)*s,.51],yaw:0}, rear:{at:[0,0],yaw:-90*s}},
                pelvis:[.02*s,.80,.13], hipYaw:-70*s, chestYaw:-75*s, headYaw:0,
                knee:{rear:[-1*s,.15,.35], lead:[0,.2,1]}}),
  // beom seogi: very short; front heel ~2 in behind the rear toes; rear foot flat, out 30°, carries the weight;
  // front foot on its ball, heel raised
  tiger: s => ({feet:{lead:{at:[.07*s,.20],yaw:0,mode:"ball"}, rear:{at:[-.06*s,0],yaw:-30*s}},
                pelvis:[-.02*s,.82,.02], hipYaw:-35*s, chestYaw:-30*s, headYaw:0,
                knee:{lead:[-.15*s,.1,1], rear:[-.3*s,0,1]}}),
  // juchum seogi: feet two shoulder widths apart, toes turned in ~15°, knees pushed out over the toes
  horse: s => ({feet:{lead:{at:[.40,0],yaw:-15}, rear:{at:[-.40,0],yaw:15}}, pelvis:[0,.74,-.02],
                knee:{lead:[.6,0,1], rear:[-.6,0,1]}}),
  // kkoa seogi: lead foot flat; rear foot crossed behind it, on the ball, just outside the lead heel
  cross: s => ({feet:{lead:{at:[0,.06],yaw:0}, rear:{at:[.12*s,-.12],yaw:10*s,mode:"ball"}}, pelvis:[.05*s,.82,-.03],
                knee:{lead:[-.1*s,0,1], rear:[-.1*s,0,1]}}),
  // hakdari seogi (lead = the standing leg): standing knee bent forward over the toes like ap kubi;
  // lifted knee forward, its foot sole-down beside the standing knee, inner edge touching (#14)
  crane: s => ({feet:{lead:{at:[.05*s,0],yaw:0}, rear:{lift:"crane"}}, pelvis:[.03*s,.84,-.10],
                knee:{lead:[0,0,1], rear:[0,.5,1]}}),
  // kicks (lead = the kicking leg)
  kick:  s => ({feet:{lead:{kick:[.08*s,1.12,.62], toe:[0,.85,.5], sole:[0,.5,-.86]}, rear:{at:[-.09*s,0],yaw:-20*s}},
                pelvis:[-.05*s,.93,-.02], lean:-8, knee:{lead:[0,1,.3]}}),
  // yeop chagi toward +Z: body side-on, torso leaning away in line with the leg; foot blade and heel lead,
  // sole flat to the target, toes back; supporting heel points at the target (#15)
  skick: s => ({feet:{lead:{kick:[0,1.02,.82], toe:[-1*s,.08,0], sole:[0,.12,1]}, rear:{at:[-.02*s,-.05],yaw:180}},
                pelvis:[0,.90,-.06], hipYaw:-90*s, chestYaw:-90*s, sideLean:-32*s, headYaw:0,
                knee:{lead:[-1*s,.3,0], rear:[0,.2,-1]}}),
  // dollyeo chagi at impact: instep strikes, hips turned over, supporting heel to the target (#15)
  rkick: s => ({feet:{lead:{kick:[.04*s,1.38,.70], toe:[-1*s,.05,0], sole:[0,.2,-1]}, rear:{at:[-.03*s,-.05],yaw:180}},
                pelvis:[0,.92,-.08], hipYaw:-110*s, chestYaw:-75*s, sideLean:-20*s, headYaw:0,
                knee:{lead:[-1*s,.4,.2], rear:[0,.2,-1]}}),
  knee:  s => ({feet:{lead:{kick:[.08*s,.50,.20], toe:[0,-.6,.8], sole:[0,-.8,-.6]}, rear:{at:[-.09*s,0],yaw:-15*s}},
                pelvis:[-.04*s,.93,0], lean:4, knee:{lead:[0,.6,1]}})
};

// ---------- arms: hand target relative to that shoulder, in the chest frame ----------
// x = outward on that arm's side, y = up, z = forward; pole = where the elbow points; hand: fist | open
const A = (t, pole, hand="fist") => ({t, pole, hand});
const DOWN = [.35,-1,-.15], BACKP = [.15,-.3,-1], OUT = [1,-.3,0];
export const ARMS = {
  chamber: A([-.05,-.47,-.06], BACKP),            // fists palm-up on the belt at the sides, 2 in back (#9)
  junbi:   A([-.11,-.44,.17], DOWN),
  guard:   A([-.10,-.12,.30], DOWN),
  punch:   A([-.19,-.12,.56], DOWN),
  hpunch:  A([-.19,.02,.55], DOWN),
  low:     A([.06,-.58,.26], [.3,-.2,1]),
  inside:  A([-.13,.02,.30], [.4,-1,0]),
  outer:   A([.05,.03,.30], [.2,-1,-.1]),
  high:    A([-.16,.34,.16], [1,.2,.2]),
  backfist:A([-.08,.10,.46], DOWN),
  hammer:  A([-.05,-.12,.50], DOWN),
  elbow:   A([-.32,-.06,.12], [0,-.1,1]),
  houter:  A([.10,.27,.24], [.4,-1,0]),
  spread:  A([.16,-.52,.16], DOWN),
  xlow:    A([-.25,-.52,.36], DOWN),
  wedge:   A([.10,.06,.26], [.4,-1,0]),
  uppercut:A([-.15,.05,.36], [.2,-1,.2]),
  cover:   A([-.20,-.22,.25], DOWN),
  sidepunch:A([.62,-.02,.02], [0,-1,0]),
  assist:  A([-.20,-.16,.25], DOWN),
  hingepunch:A([-.46,-.09,.20], [0,-.2,1]),
  hingetop:A([-.30,-.36,.05], BACKP),
  hammerout:A([.56,.0,.15], [0,-1,0]),
  sideelbow:A([-.10,-.06,.10], OUT),
  shoulder:A([-.36,.0,.08], DOWN),
  hammerlow:A([-.17,-.46,.20], DOWN),
  crosspunch:A([-.52,-.06,.16], DOWN),
  // open hands
  ksout:   A([.05,.03,.32], [.2,-1,-.1], "open"),
  ksblock: A([.04,.02,.36], [.2,-1,-.1], "open"),
  ksguard: A([-.18,-.21,.23], DOWN, "open"),
  spear:   A([-.17,-.10,.58], DOWN, "open"),
  press:   A([-.26,-.26,.30], DOWN, "open"),
  neck:    A([-.20,.05,.50], DOWN, "open"),
  khigh:   A([-.16,.34,.16], [1,.2,.2], "open"),
  twist:   A([-.05,.10,.40], DOWN, "open"),
  palm:    A([-.13,.02,.30], [.4,-1,0], "open"),
  kslow:   A([.06,-.58,.26], [.3,-.2,1], "open"),
  ksside:  A([.36,.0,.10], [0,-1,-.2], "open"),
  eltarget:A([-.25,-.05,.30], DOWN, "open"),
  grab:    A([-.10,.0,.45], DOWN, "open"),
  tongmil: A([-.17,-.06,.35], OUT, "open"),
  ksstrike:A([.15,.0,.50], DOWN, "open"),
  arc:     A([-.18,.0,.50], DOWN, "open"),
  kneebreak:A([-.10,-.50,.40], DOWN, "open"),
  hold:    A([.0,-.36,.15], BACKP, "open"),
  target:  A([.50,-.05,.10], [0,-1,0], "open"),
  lspear:  A([-.15,-.50,.46], DOWN, "open"),
  pressdown:A([-.15,-.35,.30], DOWN, "open"),
  elbowpush:A([-.30,-.06,.15], DOWN, "open"),
  palmlow: A([-.17,-.46,.20], DOWN, "open"),
  palmjaw: A([-.18,.05,.50], DOWN, "open"),
  ksin:    A([-.13,.02,.30], [.4,-1,0], "open"),
  kspread: A([.16,-.52,.16], DOWN, "open"),
  tgrab:   A([-.12,-.10,.45], DOWN, "open")
};

// ---------- helpers ----------
const V = (x=0,y=0,z=0) => new THREE.Vector3(x,y,z);
const rad = d => d*Math.PI/180;
function frame(yaw=0, lean=0, side=0){            // returns {fwd, up, left}
  const t=rad(yaw); let fwd=V(Math.sin(t),0,Math.cos(t)), left=V(Math.cos(t),0,-Math.sin(t)), up=V(0,1,0);
  const p=rad(lean); const up1=up.clone().multiplyScalar(Math.cos(p)).add(fwd.clone().multiplyScalar(Math.sin(p)));
  const f1=fwd.clone().multiplyScalar(Math.cos(p)).sub(up.clone().multiplyScalar(Math.sin(p)));
  const q=rad(side); const up2=up1.clone().multiplyScalar(Math.cos(q)).add(left.clone().multiplyScalar(Math.sin(q)));
  const l2=left.clone().multiplyScalar(Math.cos(q)).sub(up1.clone().multiplyScalar(Math.sin(q)));
  return {fwd:f1, up:up2, left:l2};
}
function ik(a, t, l1, l2, pole){                  // two-bone IK: returns [joint, end]
  const d0=t.clone().sub(a), d=THREE.MathUtils.clamp(d0.length(), Math.abs(l1-l2)+1e-3, l1+l2-1e-3);
  const n=d0.normalize(), end=a.clone().add(n.clone().multiplyScalar(d));
  const x=(l1*l1-l2*l2+d*d)/(2*d), h=Math.sqrt(Math.max(l1*l1-x*x,0));
  let p=pole.clone().sub(n.clone().multiplyScalar(pole.dot(n)));
  if(p.lengthSq()<1e-6) p=V(0,1,0).cross(n); p.normalize();
  return [a.clone().add(n.multiplyScalar(x)).add(p.multiplyScalar(h)), end];
}
const toeDir = yaw => V(Math.sin(rad(yaw)),0,Math.cos(rad(yaw)));
const merge = (a,b) => { if(!b) return a; for(const k in b){ if(b[k]&&typeof b[k]==="object"&&!Array.isArray(b[k])&&a[k]&&typeof a[k]==="object"&&!Array.isArray(a[k])) merge(a[k],b[k]); else a[k]=b[k]; } return a; };

// ---------- build the pose ----------
// spec: {stance, lead, arms:{L,R}}; ovr: per-pose overrides (same shape as a stance object + arms)
export function build(spec, ovr){
  const lead = spec.lead || "L", s = lead==="L"?1:-1, rear = lead==="L"?"R":"L";
  const P = merge(STANCES[spec.stance](s), JSON.parse(JSON.stringify((ovr&&ovr.stance)||{})));
  const B = BODY, J = {feet:{}, knees:{}, ankles:{}, hips:{}};
  const hipF = frame(P.hipYaw||0, 0, 0);
  // feet first
  const foot = {};
  for(const [role, side] of [["lead",lead],["rear",rear]]){
    const f = P.feet[role];
    if(f.at){
      const ball = f.mode==="ball", td = toeDir(f.yaw||0);
      const ankle = V(f.at[0], ball?.13:B.ankleY, f.at[1]);
      const toe = ball ? td.clone().multiplyScalar(Math.cos(rad(28))).add(V(0,-Math.sin(rad(28)),0)) : td;
      foot[side] = {ankle, toe:toe.normalize(), sole:V(0,-1,0).add(toe.clone().multiplyScalar(ball?.45:0)).normalize(), ball};
    }else if(f.kick){
      foot[side] = {ankle:V(...f.kick), toe:V(...f.toe).normalize(), sole:V(...f.sole).normalize(), kick:true};
    }
  }
  // pelvis
  let pel;
  if(P.pelvis==="apkubi"){                          // rear leg straight, front shin vertical
    const fa = foot[lead].ankle, ra = foot[rear].ankle, Lmax = B.thigh+B.shin-.004;
    const kneeF = fa.clone().add(V(0,B.shin,0));
    let z = (fa.z+ra.z)/2, y=.85;
    for(let i=0;i<60;i++){
      const hx = 0; // pelvis centred between the feet sideways
      const hipR = V(hx - B.hipHalf*s, 0, z), hipL = V(hx + B.hipHalf*s, 0, z);
      // height from the straight rear leg
      const dxr = hipR.x-ra.x, dzr = z-ra.z; y = ra.y + Math.sqrt(Math.max(Lmax*Lmax-dxr*dxr-dzr*dzr, .01));
      // move z until the front thigh length fits the vertical-shin knee
      const dxf = hipL.x-kneeF.x, dyf = y-kneeF.y, need = Math.sqrt(Math.max(B.thigh*B.thigh-dxf*dxf-dyf*dyf,0));
      z += ((kneeF.z - need) - z)*.5;
    }
    pel = V(0, y, z);
  }else{
    const p = P.pelvis; let y = p[1];
    if(y==="max"){ // as tall as the farther foot allows (straight legs)
      y = 9; for(const sd of ["L","R"]){ const f=foot[sd]; if(!f||f.kick) continue;
        const hip = V(p[0]+(sd==="L"?B.hipHalf:-B.hipHalf), 0, p[2]), dx=hip.x-f.ankle.x, dz=hip.z-f.ankle.z, L=B.thigh+B.shin-.006;
        y = Math.min(y, f.ankle.y+Math.sqrt(Math.max(L*L-dx*dx-dz*dz,.01))); }
    }
    pel = V(p[0], y, p[2]);
  }
  J.pelvis = pel;
  for(const sd of ["L","R"]) J.hips[sd] = pel.clone().add(hipF.left.clone().multiplyScalar(sd==="L"?B.hipHalf:-B.hipHalf)).add(V(0,-.02,0));
  // crane: lifted foot beside the standing knee, sole down
  if(P.feet.rear.lift==="crane"){
    const st = foot[lead], hipS = J.hips[lead];
    const [kneeS] = ik(hipS, st.ankle, B.thigh, B.shin, V(...(P.knee&&P.knee.lead||[0,0,1])));
    foot[rear] = {ankle: kneeS.clone().add(V(-s*.085, .02, .06)), toe:V(0,-.15,1).normalize(), sole:V(0,-1,-.1).normalize()};
  }
  // legs
  for(const [role, sd] of [["lead",lead],["rear",rear]]){
    const f = foot[sd], pole = V(...((P.knee&&P.knee[role]) || [f.toe.x, .25, f.toe.z]));
    const [knee, ankle] = ik(J.hips[sd], f.ankle, B.thigh, B.shin, pole);
    J.knees[sd]=knee; J.ankles[sd]=ankle; J.feet[sd]=f;
  }
  // torso and head
  const ch = frame(P.chestYaw ?? P.hipYaw ?? 0, P.lean||0, P.sideLean||0);
  J.chest = ch; J.hipFrame = hipF;
  J.shoulderC = pel.clone().add(ch.up.clone().multiplyScalar(B.spine));
  J.shoulders = {L: J.shoulderC.clone().add(ch.left.clone().multiplyScalar(B.shoulderHalf)),
                 R: J.shoulderC.clone().add(ch.left.clone().multiplyScalar(-B.shoulderHalf))};
  J.neck = J.shoulderC.clone().add(ch.up.clone().multiplyScalar(.05));
  J.head = J.neck.clone().add(ch.up.clone().multiplyScalar(.15));
  J.headFwd = frame(P.headYaw ?? 0).fwd;
  // arms
  J.elbows={}; J.wrists={}; J.hands={};
  for(const sd of ["L","R"]){
    const key = (spec.arms&&spec.arms[sd]) || "chamber";
    const a = merge(JSON.parse(JSON.stringify(ARMS[key] || ARMS.chamber)), ovr&&ovr.arms&&ovr.arms[sd]);
    const o = sd==="L"?1:-1, sh = J.shoulders[sd];
    const W = v => ch.left.clone().multiplyScalar(o*v[0]).add(ch.up.clone().multiplyScalar(v[1])).add(ch.fwd.clone().multiplyScalar(v[2]));
    const [el, wr] = ik(sh, sh.clone().add(W(a.t)), B.upper, B.fore, W(a.pole));
    J.elbows[sd]=el; J.wrists[sd]=wr; J.hands[sd]={kind:a.hand, dir:wr.clone().sub(el).normalize(), key};
  }
  return J;
}

// ---------- meshes ----------
const COL = {L:0x8fa9d4, R:0xe2ad84, body:0xc9ccd2, belt:0x22252b, floor:0xf3f4f6};
function capsule(a, b, r, color){
  const d=b.clone().sub(a), len=d.length(), g=new THREE.CapsuleGeometry(r, Math.max(len,1e-3), 6, 14);
  const m=new THREE.Mesh(g, new THREE.MeshLambertMaterial({color}));
  m.position.copy(a.clone().add(b).multiplyScalar(.5));
  m.quaternion.setFromUnitVectors(V(0,1,0), d.normalize()); return m;
}
function boxAt(center, x, y, z, size, color){       // box with axes x,y,z (unit vectors) and size [sx,sy,sz]
  const m=new THREE.Mesh(new THREE.BoxGeometry(...size), new THREE.MeshLambertMaterial({color}));
  const M=new THREE.Matrix4().makeBasis(x.clone().normalize(), y.clone().normalize(), z.clone().normalize());
  m.quaternion.setFromRotationMatrix(M); m.position.copy(center); return m;
}
function ellipsoid(center, axes, radii, color){
  const m=new THREE.Mesh(new THREE.SphereGeometry(1, 24, 18), new THREE.MeshLambertMaterial({color}));
  m.scale.set(...radii); const M=new THREE.Matrix4().makeBasis(...axes); m.quaternion.setFromRotationMatrix(M);
  m.position.copy(center); return m;
}
export function meshes(J){
  const g=new THREE.Group(), B=BODY;
  // torso: pelvis block, chest, belt
  const hf=J.hipFrame, ch=J.chest;
  g.add(ellipsoid(J.pelvis.clone().add(V(0,.01,0)), [hf.left, V(0,1,0), hf.fwd], [.15,.11,.10], COL.body));
  const chestC = J.pelvis.clone().add(ch.up.clone().multiplyScalar(.31));
  g.add(ellipsoid(chestC, [ch.left, ch.up, ch.fwd], [.165,.22,.10], COL.body));
  const beltC = J.pelvis.clone().add(ch.up.clone().multiplyScalar(.11));
  g.add(ellipsoid(beltC, [ch.left, ch.up, ch.fwd], [.15,.028,.10], COL.belt));
  g.add(capsule(J.shoulders.L, J.shoulders.R, .055, COL.body));
  // head with a nose so the facing reads in every view
  g.add(capsule(J.neck, J.neck.clone().add(ch.up.clone().multiplyScalar(.07)), .045, COL.body));
  g.add(ellipsoid(J.head, [V(1,0,0),V(0,1,0),V(0,0,1)], [.10,.125,.11], COL.body));
  const nose=new THREE.Mesh(new THREE.ConeGeometry(.03,.07,12), new THREE.MeshLambertMaterial({color:0x6b7280}));
  nose.position.copy(J.head.clone().add(J.headFwd.clone().multiplyScalar(.11)));
  nose.quaternion.setFromUnitVectors(V(0,1,0), J.headFwd); g.add(nose);
  for(const sd of ["L","R"]){
    const c=COL[sd];
    g.add(capsule(J.hips[sd], J.knees[sd], .068, c));
    g.add(capsule(J.knees[sd], J.ankles[sd], .052, c));
    const f=J.feet[sd], side=f.sole.clone().cross(f.toe).normalize();   // right-handed basis (toe, side, sole)
    const fc=J.ankles[sd].clone().add(f.toe.clone().multiplyScalar(.07)).add(f.sole.clone().multiplyScalar(.045));
    g.add(boxAt(fc, f.toe, side, f.sole, [B.footLen,.10,.06], c));
    g.add(boxAt(fc.clone().add(f.toe.clone().multiplyScalar(B.footLen*.42)).add(f.sole.clone().multiplyScalar(.012)), f.toe, side, f.sole, [.035,.10,.03], 0x4b5563)); // toe cap: shows which way the foot points
    g.add(capsule(J.shoulders[sd], J.elbows[sd], .048, c));
    g.add(capsule(J.elbows[sd], J.wrists[sd], .04, c));
    const h=J.hands[sd], d=h.dir, up=Math.abs(d.y)>.9?V(1,0,0):V(0,1,0), sx=d.clone().cross(up).normalize(), sy=d.clone().cross(sx).normalize();
    if(h.kind==="open") g.add(boxAt(J.wrists[sd].clone().add(d.clone().multiplyScalar(.09)), d, sx, sy, [.18,.08,.025], c));
    else g.add(boxAt(J.wrists[sd].clone().add(d.clone().multiplyScalar(.05)), d, sx, sy, [.10,.085,.085], c));
  }
  return g;
}

// ---------- scene + cameras ----------
export function makeScene(canvas, w, h){
  const r=new THREE.WebGLRenderer({canvas, antialias:true, preserveDrawingBuffer:true}); r.setSize(w,h,false); r.setClearColor(0xffffff);
  const scene=new THREE.Scene();
  scene.add(new THREE.HemisphereLight(0xffffff, 0x9aa3b2, 1.6));
  const dl=new THREE.DirectionalLight(0xffffff, 1.4); dl.position.set(1.5,3,2.5); scene.add(dl);
  const dl2=new THREE.DirectionalLight(0xffffff, .5); dl2.position.set(-2,2,-2); scene.add(dl2);
  // floor with a 10 cm grid
  const floor=new THREE.Mesh(new THREE.PlaneGeometry(6,6), new THREE.MeshLambertMaterial({color:COL.floor}));
  floor.rotation.x=-Math.PI/2; scene.add(floor);
  const grid=new THREE.GridHelper(6, 60, 0xd5d9e0, 0xe4e7ec); grid.position.y=.001; scene.add(grid);
  return {renderer:r, scene};
}
// view: front (camera where the figure faces), back, side + face R (figure faces right of the picture) or L
export function camera(view, face, box, aspect){
  const c=box.getCenter(V()), size=box.getSize(V());
  const across = (view==="side") ? size.z : size.x;            // horizontal extent seen by this camera
  const hgt=Math.max(2.15, size.y+.3, (across+.35)/aspect), wid=hgt*aspect;
  const cam=new THREE.OrthographicCamera(-wid/2, wid/2, hgt/2, -hgt/2, .1, 50);
  const tgt=V(c.x, hgt/2-.12, c.z), d=10, el=Math.tan(8*Math.PI/180);   // 8° above eye level so the feet read
  if(view==="top"){ const w=Math.max(size.x,size.z)+.5, h=w/aspect>w?w:w; const top=new THREE.OrthographicCamera(-w/2*aspect/aspect,w/2,w/2/aspect*aspect,-w/2,.1,50);
    top.left=-w/2; top.right=w/2; top.top=w/2/aspect; top.bottom=-w/2/aspect; top.updateProjectionMatrix();
    top.position.set(c.x,8,c.z); top.up.set(0,0,1); top.lookAt(c.x,0,c.z); return top; }
  const dir = view==="front"?V(0,0,1): view==="back"?V(0,0,-1): face==="R"?V(-1,0,0):V(1,0,0);
  cam.position.copy(tgt.clone().add(dir.multiplyScalar(d)).add(V(0,d*el,0)));
  cam.lookAt(tgt); return cam;
}
