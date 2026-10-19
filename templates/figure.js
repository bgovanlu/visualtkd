/* Figure renderer, footprints and stance chips, shared by the form pages and the library.
   Inlined by tools/build_form.py and tools/build_site.py; needs LIB (names and links from data/techniques.json). */
const BELTS={white:"#f4f4f2",yellow:"#f2c230",green:"#2f8f4e",blue:"#2456c8",red:"#c8102e",black:"#17181c"};
let belt="black";

// labels from data/techniques.json: [romanised, Hangul, English]
const T=Object.fromEntries(Object.entries(LIB.t).map(([k,v])=>[k,v.slice(0,3)]));
const STANCE=Object.fromEntries(Object.entries(LIB.s).map(([k,v])=>[k,v.slice(0,3)]));
// library links: /library/<family>/#<slug>
const techHref=k=>LIB.t[k][3],stanceHref=k=>LIB.s[k][3];
const DIRN={na:"na",ga:"ga",na4:"na",na5:"na",ga4:"ga",ga5:"ga",gada2:"ga-da",nada2:"na-da",gara2:"ga-ra",nara2:"na-ra",da1:"da¹",da2:"da²",da3:"da³",ra1:"ra¹",ra2:"ra²",ra3:"ra³",gada:"ga-da",nada:"na-da",gara:"ga-ra",nara:"na-ra"};

let gid=0;
/* ---------- vector helpers ---------- */
const f=n=>(+n).toFixed(2);
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],sub=(a,b)=>[a[0]-b[0],a[1]-b[1]],mul=(a,k)=>[a[0]*k,a[1]*k];
const norm=a=>{const l=Math.hypot(a[0],a[1])||1;return[a[0]/l,a[1]/l]};
const lerp=(a,b,t)=>[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t];
const dist=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
function ik(a,b,l1,l2,pref){
  let dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy);const mx=l1+l2-.6;
  if(d>mx){b=[a[0]+dx/d*mx,a[1]+dy/d*mx];dx=b[0]-a[0];dy=b[1]-a[1];d=mx}
  d=Math.max(d,1e-3);
  const ang=Math.acos(Math.max(-1,Math.min(1,(l1*l1+d*d-l2*l2)/(2*l1*d)))),base=Math.atan2(dy,dx);
  const c1=[a[0]+Math.cos(base+ang)*l1,a[1]+Math.sin(base+ang)*l1],c2=[a[0]+Math.cos(base-ang)*l1,a[1]+Math.sin(base-ang)*l1];
  const mid=lerp(a,b,.5),s=p=>(p[0]-mid[0])*pref[0]+(p[1]-mid[1])*pref[1];
  return[s(c1)>=s(c2)?c1:c2,b];
}
const area=P=>P.reduce((s,p,i)=>{const q=P[(i+1)%P.length];return s+p[0]*q[1]-q[0]*p[1]},0);
const orient=P=>area(P)<0?P.slice().reverse():P;
function spline(Q,tension=1){
  const P=orient(Q),n=P.length,k=6/tension;let d=`M${f(P[0][0])} ${f(P[0][1])}`;
  for(let i=0;i<n;i++){const p0=P[(i-1+n)%n],p1=P[i],p2=P[(i+1)%n],p3=P[(i+2)%n];
    d+=`C${f(p1[0]+(p2[0]-p0[0])/k)} ${f(p1[1]+(p2[1]-p0[1])/k)} ${f(p2[0]-(p3[0]-p1[0])/k)} ${f(p2[1]-(p3[1]-p1[1])/k)} ${f(p2[0])} ${f(p2[1])}`}
  return d+"Z";
}
function openCurve(P){ // smooth open stroke
  let d=`M${f(P[0][0])} ${f(P[0][1])}`;const n=P.length;
  for(let i=0;i<n-1;i++){const p0=P[Math.max(i-1,0)],p1=P[i],p2=P[i+1],p3=P[Math.min(i+2,n-1)];
    d+=`C${f(p1[0]+(p2[0]-p0[0])/6)} ${f(p1[1]+(p2[1]-p0[1])/6)} ${f(p2[0]-(p3[0]-p1[0])/6)} ${f(p2[1]-(p3[1]-p1[1])/6)} ${f(p2[0])} ${f(p2[1])}`}
  return d;
}
function xf(P,o,ang=0,sx=1,sy=1){const c=Math.cos(ang),s=Math.sin(ang);return P.map(([x,y])=>[o[0]+x*sx*c-y*sy*s,o[1]+x*sx*s+y*sy*c])}
const ellPts=(c,rx,ry,ang=0)=>{const P=[];for(let i=0;i<14;i++){const t=i/14*Math.PI*2;P.push([Math.cos(t)*rx,Math.sin(t)*ry])}return xf(P,c,ang)};
const ln=(a,b)=>`M${f(a[0])} ${f(a[1])}L${f(b[0])} ${f(b[1])}`;

/* ---------- limb contour ----------
   One closed outline around shoulder→elbow→wrist (or hip→knee→ankle),
   offset by a width profile so cloth tapers and flares like a dobok. */
const TS=[0,.14,.28,.42,.5,.58,.72,.86,1];
function contour(ch,W,capTop){
  const[a,j,b]=ch,d1=norm(sub(j,a)),d2=norm(sub(b,j)),dm=norm(add(d1,d2));
  const Lp=[],Rp=[],mid=[];
  TS.forEach((t,i)=>{
    let p,d;
    if(t<.5){p=lerp(a,j,t/.5);d=d1}else if(t>.5){p=lerp(j,b,(t-.5)/.5);d=d2}else{p=j;d=dm}
    const n=[-d[1],d[0]],w=W[i];Lp.push(add(p,mul(n,w)));Rp.push(add(p,mul(n,-w)));mid.push({p,n,w,d});
  });
  const pts=[...Lp,...Rp.reverse()];
  if(capTop)pts.push(add(a,mul(d1,-W[0]*.75)));
  return{pts,mid,d1,d2};
}

/* ---------- skeleton ---------- */
const FOOT_SIDE=[[-3.4,-1.6],[1.6,-1.8],[5,.8],[9.4,3],[12.8,4.4],[14,5.9],[11,6.5],[6,6.1],[2.6,5.7],[-1.8,6.4],[-5,6],[-5.9,2.8]];
const FOOT_FRONT=[[-3.9,-1.4],[3.9,-1.4],[5.1,3.4],[5.6,6],[2,6.9],[-2,6.9],[-5.6,6],[-5.1,3.4]];
const FOOT_HEEL=[[-3.7,-1],[3.7,-1],[4.4,3.8],[3.2,6.5],[-3.2,6.5],[-4.4,3.8]];
const FIST=[[-.4,-3.8],[3,-4.6],[7.6,-4.5],[9.8,-2.8],[10.3,.4],[9.4,3.6],[6,4.8],[1.6,4.3],[-.4,3.6]];
const HAND_FLAT=[[-.4,-3],[3,-3.4],[9,-3.2],[13.2,-2],[14,0],[13.2,2],[9,3.1],[3,3.3],[-.4,2.8]];
// open-hand techniques draw a flat hand instead of a fist
const OPEN=new Set(["palmup","kstwinhigh","ksout","ksblock","ksguard","spear","press","neck","khigh","eltarget","twist","palm","grab","ksside","kslow",
  "tongmil","gyeopson","ksstrike","arc","kneebreak","hold","target","lspear","pressdown","elbowpush","palmlow","palmjaw","ksin","kspread","tgrab",
  "passist","rockhi","rocklo","rwedge","lift","kxlow","htarget",
  "ksdown","kswedge","heaven","kxcheck","wing","khopen","twistm","swingo","ohouter","pushlo","pushhi","grabtw"]);
// seen from the front, these come straight at the viewer: drawn foreshortened (fist face or hand edge), never across the face
const TOWARD={bfside:k=>[12,-7],hpunch:k=>[3,9],twinv:k=>[12,-2],upset:k=>[7,18],punch:k=>[1.5,20],neck:k=>[-3,5],arc:k=>[-1,5],palmjaw:k=>[-1,9],tgrab:k=>[-2,16],chet:k=>[7,20]};
const KNIFE_FACE=[[-6.8,-2.4],[6.8,-2.4],[7.6,0],[6.8,2.4],[-6.8,2.4],[-7.6,0]];
const FIST_FACE=[[-5.4,-4.3],[5.4,-4.3],[6.3,0],[5.6,4.5],[-5.6,4.5],[-6.3,0]];
const mk=far=>({far,legs:[],arms:[],feet:[],fists:[],torso:null,head:null,neck:null});

function skel(m,pr){
  if(m.stance==="ogeum")m={...m,stance:"crane",ogeum:true};
  if(m.stance==="oneleg")m={...m,stance:"crane"};   // ITF waebal sogi (one-leg stance): drawn as the crane stance
  if(m.stance==="sasun")m={...m,stance:"horse"};   // ITF sasun sogi (diagonal stance): drawn as the sitting stance   // ogeum seogi: drawn as crane stance, lifted foot behind the knee
  if(m.stance==="fixed")m={...m,stance:"back"};   // ITF gojung sogi (fixed stance): drawn with L-stance geometry
  if(m.stance==="vertical")m={...m,stance:"back"};   // ITF soojik sogi (vertical stance): a short, upright L shape
  if(m.stance==="lowst")m={...m,stance:"front"};  // ITF nachuo sogi (low stance): drawn as the walking stance
  const HANDS={};let side;   // where each hand ends up (for the same-stance motion arcs and count badges)
  const k=(pr.thigh+pr.shin)/65,tk=pr.torso/55,ak=(pr.upper+pr.fore)/47,sw=pr.shW/18.5,hw=pr.hipW/9;
  function addArm(L,sh,h,pref,pf,flat){
    if(pf){L.arms.push({ch:[sh,lerp(sh,h,.5),h],front:true});L.fists.push({c:h,front:true,flat});HANDS[side]=h;return}
    const[e,w]=ik(sh,h,pr.upper,pr.fore,pref);L.arms.push({ch:[sh,e,w]});L.fists.push({w,d:norm(sub(w,e)),flat});HANDS[side]=w;
  }
  if(m.view==="side"){
    const near=m.face==="R"?"R":"L",st=m.stance;
    const hipY={walk:0,front:14,kick:-2,back:8,skick:-4,rkick:-4,knee:-2,tiger:10,horse:12,cross:6,close:-1,ready:-1,crane:0,nieun:6,gyeot:8}[st]*k,lean={gyeot:2,walk:2,front:5,kick:-8,back:-3,nieun:-2,skick:-13,rkick:-12,knee:-4,tiger:-1,horse:0,cross:3,close:0,ready:0,crane:0}[st]*tk;
    const H=[0,hipY],S=[lean,hipY-pr.torso],u=norm(sub(S,H)),r=[-u[1],u[0]],Lt=pr.torso;
    const P=(x,y)=>add(add(H,mul(r,x)),mul(u,y));
    const Lay={farArm:mk(1),farLeg:mk(1),nearLeg:mk(0),head:mk(0),torso:mk(0),nearArm:mk(0)};
    Lay.farArm.part=Lay.nearArm.part="arm";Lay.farLeg.part=Lay.nearLeg.part="leg";
    const shN=P(0,Lt-5.5*tk),SH={near:shN,far:add(shN,[-3,-1.2])},hN=P(0,1),HP={near:hN,far:add(hN,[-3,0])};
    ["L","R"].forEach(s=>{side=s;
      const dp=s===near?"near":"far",lead=s===m.lead;
      let t,pref=[1,-.25];
      if(st==="walk")t=lead?[24,56]:[-22,56];
      else if(st==="front")t=lead?[38,56]:[-44,56];
      else if(st==="back")t=lead?[22,56]:[-17,56];                    // dwit kubi: weight on the bent rear leg
      else if(st==="skick"){t=lead?[60,-6]:[-6,56];if(lead)pref=[.3,-1];} // yeop chagi: leg level, body leaning away
      else if(st==="rkick"){t=lead?[54,-30]:[-6,56];if(lead)pref=[.6,-1];} // dollyeo chagi: kick at face height
      else if(st==="knee"){t=lead?[18,22]:[-4,56];if(lead)pref=[1,-1];}    // mureup chigi: knee driven up
      else if(st==="tiger")t=lead?[12,56]:[-14,56];                      // beom seogi: short, weight on the bent rear leg
      else if(st==="nieun")t=lead?[15,56]:[-11,56];                      // nieunja seogi: feet at right angles, about one foot apart
      else if(st==="horse"){t=dp==="near"?[19,56]:[11,56];pref=[1,-.1]}             // juchum seogi in profile: legs side by side, knees forward
      else if(st==="crane"){t=lead?[1,56]:m.ogeum?[-8,30]:[4,25];if(!lead)pref=m.ogeum?[-1,.4]:[1,-.35]}  // hakdari seogi: lifted foot against the standing knee (ogeum: behind it)
      else if(st==="cross")t=lead?[8,56]:[-6,56];                        // kkoa seogi: rear foot tucked behind
      else if(st==="gyeot")t=lead?[10,56]:[-4,56];                       // gyeotdari seogi: rear knee bent in behind the front knee
      else if(st==="close"||st==="ready")t=lead?[3,56]:[-1,56];
      else{t=lead?[58,-16]:[-5,56];if(lead)pref=[.4,-1];}
      t=mul(t,k);
      const hp=HP[dp],[kn,an]=ik(hp,t,pr.thigh,pr.shin,pref),Lg=dp==="near"?Lay.nearLeg:Lay.farLeg;
      Lg.legs.push({ch:[hp,kn,an]});
      const kicking=["kick","skick","rkick","knee"].includes(st),kick=kicking&&lead;
      const fs=lead||kicking?1:st==="back"||st==="nieun"?.6:st==="crane"?.9:.82;   // back-stance rear foot is turned out 90°, so it reads short
      Lg.feet.push({pts:xf(FOOT_SIDE,an,kick?({skick:-.15,rkick:-.4,knee:.9}[st]??-1.25):(st==="tiger"&&lead?-.35:st==="crane"&&!lead?1.15:0),fs*pr.foot,pr.foot)});
      const act=(m.arms&&m.arms[s])||"chamber",sh=SH[dp];let h,p=[0,1];
      if(act==="chamber"){h=[-4,hipY-11*tk];p=[-1,.1]}
      else if(act==="punch")h=add(sh,mul([46,6],ak));
      else if(act==="hpunch"||act==="twinv")h=add(sh,mul([45,-9],ak));
      else if(act==="upset")h=add(sh,mul([40,10],ak));                 // ITF upset punch: fist palm-up at solar-plexus height
      else if(act==="uhigh")h=add(sh,mul([34,-12],ak));                // ITF U-shape block, upper arm: forearm level at head height
      else if(act==="ulow")h=add(sh,mul([34,14],ak));                  // … lower arm at middle height
      else if(act==="palmup"){h=add(sh,mul([26,-4],ak));p=[1,.2]}      // ITF upward palm block: palm rising in front of the chest
      else if(act==="bfback"){h=add(sh,mul([-16,-14],ak));p=[-1,-.2]}  // ITF back fist side back strike: fist driven back past the shoulder at head height
      else if(act==="low")h=[26*ak,hipY-2];
      else if(act==="inside")h=add(sh,mul([22,-1],ak));
      else if(act==="high"||act==="khigh"){h=add(sh,mul([17,-30],ak));p=[1,-.15]}
      else if(act==="outer")h=add(sh,mul([19,-7],ak));
      else if(act==="sideblk")h=add(sh,mul([27,-2],ak));
      else if(act==="xshoulder")h=add(sh,mul([14,4],ak));   // fist drawn back in front of the other shoulder   // ITF side block: forearm upright out in front of the shoulder, clear of the face
      else if(act==="twinhigh"||act==="kstwinhigh"){h=add(sh,mul([5,-36],ak));p=[1,-.15]}   // ITF twin forearm (or knife-hand) block, rear arm: guarding above the forehead
      else if(act==="ksout")h=add(sh,mul([22,-5],ak));
      else if(act==="ksblock")h=add(sh,mul([25,-3],ak));
      else if(act==="ksguard")h=add(sh,mul([13,15],ak));
      else if(act==="spear")h=add(sh,mul([48,4],ak));
      else if(act==="press")h=add(sh,mul([24,20],ak));
      else if(act==="neck")h=add(sh,mul([40,-4],ak));
      else if(act==="backfist"||act==="bfside")h=add(sh,mul([36,-12],ak));
      else if(act==="hammer")h=add(sh,mul([38,10],ak));
      else if(act==="elbow"){h=add(sh,mul([10,2],ak));p=[1,.3]}
      else if(act==="eltarget")h=add(sh,mul([24,2],ak));
      else if(act==="houter"){h=add(sh,mul([14,-26],ak));p=[1,.5]}
      else if(act==="twist")h=add(sh,mul([24,-14],ak));
      else if(act==="spread")h=[8,hipY+10];
      else if(act==="palm")h=add(sh,mul([22,-1],ak));
      else if(act==="xlow")h=[24*ak,hipY+2];
      else if(act==="wedge")h=add(sh,mul([18,-8],ak));
      else if(act==="uppercut")h=add(sh,mul([26,-6],ak));
      else if(act==="grab")h=add(sh,mul([30,-4],ak));
      else if(act==="cover")h=add(sh,mul([16,14],ak));
      else if(act==="sidepunch")h=add(sh,mul([46,4],ak));
      else if(act==="ksside")h=add(sh,mul([24,-2],ak));
      else if(act==="kslow")h=[26*ak,hipY-2];
      else if(act==="assist")h=add(sh,mul([14,14],ak));
      else if(act==="tongmil")h=add(sh,mul([24,-8],ak));
      else if(act==="ksstrike")h=add(sh,mul([40,-6],ak));
      else if(act==="ksdown")h=add(sh,mul([38,8],ak));
      else if(act==="kswedge")h=add(sh,mul([18,-8],ak));   // ITF knife-hand wedging block: the open-hand wedge block
      else if(act==="heaven"){h=add(sh,mul([16,-30],ak));p=[1,-.2]}   // ITF heaven hand: open hands raised to a triangle in front of the forehead
      else if(act==="kxcheck")h=add(sh,mul([30,2],ak));               // ITF X-knife-hand checking block: both hands crossed at the wrists in front of the chest                // ITF knife-hand downward strike: edge brought down to chest height in front
      else if(act==="arc")h=add(sh,mul([44,-8],ak));
      else if(act==="kneebreak")h=[30*ak,hipY+4];
      else if(act==="hold"){h=[5,hipY-17*tk];p=[-1,.2]}
      else if(act==="target")h=add(sh,mul([36,2],ak));
      else if(act==="crosspunch")h=add(sh,mul([44,4],ak));
      else if(act==="lspear")h=[36*ak,hipY-1];
      else if(act==="shoulder"){h=add(sh,mul([8,5],ak));p=[1,.7]}
      else if(act==="pressdown")h=add(sh,mul([24,26],ak));
      else if(act==="sideelbow"){h=add(sh,mul([2,10],ak));p=[-1,.2]}
      else if(act==="elbowpush")h=add(sh,mul([14,8],ak));
      else if(act==="hammerlow"||act==="palmlow")h=add(sh,mul([20,30],ak));
      else if(act==="palmjaw")h=add(sh,mul([42,-10],ak));
      else if(act==="ksin")h=add(sh,mul([22,-1],ak));
      else if(act==="hingepunch")h=add(sh,mul([26,4],ak));
      else if(act==="hingetop")h=add(sh,mul([10,16],ak));
      else if(act==="hammerout")h=add(sh,mul([44,-2],ak));
      else if(act==="kspread")h=[22*ak,hipY+2];
      else if(act==="tgrab")h=add(sh,mul([36,4],ak));
      else if(act==="gyeopson"){h=[7*ak,hipY-4];p=[1,.3]}                   // overlapped hands in front of the lower belly
      else if(act==="upelbow"){h=add(sh,mul([5,-9],ak));p=[1,-.15]}         // palkup ollyeo chigi: elbow driven up and forward, fist by the ear
      else if(act==="sidebf")h=add(sh,mul([36,-12],ak));
      else if(act==="crossbf")h=add(sh,mul([30,-10],ak));
      else if(act==="bull"){h=add(sh,mul([6,-30],ak));p=[1,.4]}             // hwangso makki: fists above the forehead
      else if(act==="passist"){h=add(sh,mul([16,0],ak));p=[1,.4]}           // open palm bracing the blocking wrist
      else if(act==="rockhi"){h=add(sh,mul([30,-24],ak));p=[1,.3]}          // bawi milgi: upper hand at head height
      else if(act==="rocklo"){h=add(sh,mul([32,-6],ak));p=[1,.3]}           // bawi milgi: lower hand in front of the face
      else if(act==="rwedge")h=add(sh,mul([18,-8],ak));
      else if(act==="lift"){h=add(sh,mul([26,0],ak));p=[1,.5]}             // geodeo olligi: forearm lifting in front, hand open
      else if(act==="chet")h=add(sh,mul([46,8],ak));                       // chetdari jireugi: both fists forward
      else if(act==="kxlow")h=[24*ak,hipY+2];
      else if(act==="htarget")h=add(sh,mul([34,-6],ak));                  // mejumeok pyojeok an chigi: open target hand at face height
      else if(act==="hammerin")h=add(sh,mul([38,-4],ak));                  // hammer fist swung in to the target
      else if(act==="lowside")h=[22*ak,hipY-4];
      else if(act==="wing")h=add(sh,mul([6,-2],ak));                       // nalgae pyeogi: palms pushed out to the sides
      else if(act==="khopen"){h=add(sh,mul([10,-26],ak));p=[1,.4]}         // sonnal eolgul hecho makki: open hands above the head
      else if(act==="twistm")h=add(sh,mul([26,-2],ak));                    // sonnal biteureo makki at chest height
      else if(act==="wesc"){h=add(sh,mul([14,10],ak));p=[1,.4]}           // bakkat teureo ppaegi: wrist twisted free, drawn back
      else if(act==="swing"||act==="swingo"){h=add(sh,mul([14,-26],ak));p=[1,.5]}   // hwidulleo makki: arm circling up and out
      else if(act==="ohouter"){h=add(sh,mul([14,-26],ak));p=[1,.5]}
      else if(act==="pushlo"){h=add(sh,mul([32,24],ak));p=[1,.3]}          // taesan milgi: lower hand at belt height
      else if(act==="pushhi"){h=add(sh,mul([34,-8],ak));p=[1,.3]}          // taesan milgi: upper hand at lip height
      else if(act==="bamup")h=add(sh,mul([26,-6],ak));
      else if(act==="hammerin2")h=add(sh,mul([30,4],ak));                 // du mejumeok an chigi: both hammer fists in at chest height
      else if(act==="xhigh"){h=add(sh,mul([20,-28],ak));p=[1,-.1]}       // eotgeoreo eolgul makki: wrists crossed above the forehead
      else if(act==="grabtw"){h=add(sh,mul([30,-2],ak));p=[1,.3]}         // hands turned over, taking hold in front of the chest
      else h=dp==="near"?add(sh,mul([24,14],ak)):add(sh,mul([17,7],ak));
      addArm(dp==="near"?Lay.nearArm:Lay.farArm,sh,h,p,false,OPEN.has(act));
    });
    const ang=Math.atan2(u[0],-u[1]),hs=pr.head,Hc=P(2.2,Lt+10.6*hs+3);
    Lay.head.head={c:Hc,s:hs,ang,view:"side"};
    Lay.head.neck={pts:[P(-3.2,Lt-3),P(5.2,Lt-3),add(Hc,xf([[5.2,7.5*hs]],[0,0],ang)[0]),add(Hc,xf([[-2.8,7.2*hs]],[0,0],ang)[0])]};
    const ww=pr.waist;
    Lay.torso.torso={
      pts:[P(-4.8,Lt+1.8),P(-10.2,Lt-5),P(-11*ww,Lt-23*tk),P(-9.6*ww,9),P(-13,-11),P(0,-13),P(12.8,-11),P(10*ww,11),P(12.6,Lt-20*tk),P(10.6,Lt-6),P(4.6,Lt+1.2)],
      collar:openCurve([P(3.8,Lt+.6),P(7.6,Lt-6),P(10.4,Lt-15*tk)]),
      lapel:"",
      under:openCurve([P(-13,-10.5),P(0,-12),P(12.8,-10.5)]),
      gather:"",
      band:[P(-10.4*ww,7),P(10.6*ww,7),P(10.6*ww,2.4),P(-10.4*ww,2.4)],
      tails:[[P(9.6*ww,4.6),P(13.6,-13)],[P(9.2*ww,4.6),P(8.2,-14.2)]],knot:null,
      shadeA:P(-12,Lt/2),shadeB:P(12,Lt/2)
    };
    return{k,hands:HANDS,mirror:m.face==="L",layers:["farArm","farLeg","nearLeg","head","torso","nearArm"].map(q=>Lay[q])};
  }
  const back=m.view==="back",sx=s=>(s==="L"?1:-1)*(back?-1:1),st=m.stance;
  const hipY=(st==="front"||st==="back"||st==="tiger"||st==="nieun")?6*k:st==="horse"?10*k:st==="cross"||st==="gyeot"?4*k:st==="crane"?-1*k:-3*k,T=hipY-pr.torso;
  const Lay={arms:mk(0),farLeg:mk(1),nearLeg:mk(0),head:mk(0),torso:mk(0),kick:mk(1)};
  Lay.arms.part="arm";Lay.farLeg.part=Lay.nearLeg.part=Lay.kick.part="leg";
  ["L","R"].forEach(s=>{side=s;
    const x=sx(s),hp=[x*pr.hipW*.95,hipY];let an,kn,nearer=true,sc=1;
    if(st==="ready"){an=[x*11*hw,58*k];kn=add(lerp(hp,an,.5),[x*.6,0])}
    else if(st==="close"){an=[x*4.5*hw,58*k];kn=add(lerp(hp,an,.5),[x*.3,0])}
    else if(st==="horse"){an=[x*24*hw,60*k];kn=add(lerp(hp,an,.5),[x*6,0])}  // juchum seogi: wide, knees pushed out
    else if(st==="tiger"){ // beom seogi: front foot light and close, rear knee bent
      const lead=s===m.lead;nearer=back?!lead:lead;
      if(lead){an=[x*6*hw,(back?55:60)*k];kn=add(lerp(hp,an,.5),[x*2,0]);sc=back?.9:1}
      else{an=[x*10*hw,(back?60:55)*k];kn=add(lerp(hp,an,.5),[x*4,0]);sc=back?1:.9}
    }else if(st==="cross"||st==="gyeot"){ // kkoa seogi after a jump (gyeotdari seogi drawn the same way): rear foot crossed behind the front one
      const lead=s===m.lead;nearer=back?!lead:lead;
      if(lead){an=[x*5*hw,(back?55:60)*k];kn=lerp(hp,an,.5);sc=back?.9:1}
      else{an=[x*-1*hw,(back?60:54)*k];kn=add(lerp(hp,an,.5),[x*2,0]);sc=back?1:.86}
    }
    else if(st==="crane"){ // hakdari seogi: lifted knee turned out, foot resting against the standing knee
      const lead=s===m.lead;nearer=back?lead:!lead;
      if(lead){an=[x*4*hw,58*k];kn=add(lerp(hp,an,.5),[x*.6,0])}
      else{kn=[x*17*hw,hipY+21];an=[x*-2.5*hw,hipY+31];sc=.9}
    }
    else if(st==="walk"){ // ap seogi seen from front/back: both legs straight, lead foot nearer the viewer from the front
      const lead=s===m.lead;nearer=back?!lead:lead;
      if(nearer){an=[x*10.5*hw,62*k];sc=1.06}else{an=[x*9.5*hw,54*k];sc=.9}
      kn=add(lerp(hp,an,.5),[x*.4,0]);
    }else if(st==="back"||st==="nieun"){ // dwit kubi (and the shorter nieunja seogi) from front/back: front leg light and near the centre line, rear knee bent outward
      const lead=s===m.lead;nearer=back?!lead:lead;
      if(lead){an=[x*7*hw,(back?54:61)*k];kn=add(lerp(hp,an,.5),[x*1,0]);sc=back?.9:1.04}
      else{an=[x*12*hw,(back?61:54)*k];kn=add(lerp(hp,an,.5),[x*5,0]);sc=back?1.04:.9}
    }else if(st==="kick"){ // front kick seen from behind: kicking leg raised away from the viewer, foot just clear of the body
      const kicker=s===m.lead;nearer=back?!kicker:kicker;
      if(kicker){kn=back?[x*9*hw,hipY-4]:[x*11*hw,hipY+12];an=back?[x*8*hw,hipY-24]:[x*10*hw,hipY+4];sc=back?.78:1.25}
      else{an=[x*10.5*hw,58*k];kn=add(lerp(hp,an,.5),[x*.4,0])}
    }
    else{
      const lead=s===m.lead;nearer=back?!lead:lead;
      if(nearer){an=[x*14*hw,63*k];kn=lead?[x*13.5*hw,hipY+pr.thigh*.7]:add(lerp(hp,an,.5),[x*.4,0]);sc=1.1}
      else{an=[x*12.5*hw,52*k];kn=lead?[x*12.5*hw,hipY+pr.thigh*.62]:add(lerp(hp,an,.5),[x*.4,0]);sc=.86}
    }
    // seen from behind, the kicking leg is raised in front of the body: draw it over the torso in the far-side tone
    const Lg=(st==="kick"&&back&&s===m.lead)?Lay.kick:(nearer?Lay.nearLeg:Lay.farLeg);
    Lg.legs.push({ch:[hp,kn,an],front:true});
    if(st==="crane"&&s!==m.lead)Lg.feet.push({pts:xf(FOOT_SIDE,an,Math.PI/2,.8*pr.foot,-.8*x*pr.foot)});
    else Lg.feet.push({pts:xf(back?FOOT_HEEL:FOOT_FRONT,add(an,[x*.8,0]),0,sc*x*pr.foot,sc*pr.foot)});
    const act=(m.arms&&m.arms[s])||"chamber",sh=[x*pr.shW,T+8*tk];
    if((act==="punch"||act==="spear")&&back)addArm(Lay.arms,sh,[x*-3,T+20*tk],[x,.2],false,OPEN.has(act));
    else if(act==="chet"&&back)addArm(Lay.arms,sh,[x*7,T+20*tk],[x,.2]);
    else if(act==="lspear"&&!back)addArm(Lay.arms,sh,[x*-2,hipY+1],null,true,true);
    else if(TOWARD[act]&&!back){   // strikes toward the viewer: fist face or knife-hand edge, foreshortened
      const q=TOWARD[act]();addArm(Lay.arms,sh,[x*q[0],T+q[1]*tk],null,true,OPEN.has(act));
    }else{
      let h,p=[x,.15];
      if(act==="chamber")h=[x*(pr.hipW+7),hipY-9*tk];
      else if(act==="low")h=[x*(pr.hipW+15),hipY+4*k];
      else if(act==="inside"){h=[x*-3,T+9*tk];p=[x*.5,1]}      // forearm upright, fist at the centre line
      else if(act==="high"){h=[x*-4,T-24*tk];p=[x,-.4]}        // forearm across, above the forehead
      else if(act==="khigh"){h=[x*-4,T-24*tk];p=[x,-.4]}
      else if(act==="outer"){h=[x*(pr.shW+4),T+6*tk];p=[x*.4,1]}
      else if(act==="sideblk"){h=[x*(pr.shW+4),T+6*tk];p=[x*.4,1]}
      else if(act==="uhigh"){h=[x*(pr.shW+6),T-10*tk];p=[x*.4,1]}
      else if(act==="ulow"){h=[x*(pr.shW+6),T+18*tk];p=[x*.4,1]}
      else if(act==="palmup"){h=[x*-2,T+12*tk];p=[x*.5,1]}
      else if(act==="bfback"){h=[x*(pr.shW+4),T-16*tk];p=[x,.2]}
      else if(act==="xshoulder"){h=[x*-15,T+8*tk];p=[x*.6,.6]}
      else if(act==="twinhigh"||act==="kstwinhigh"){h=[x*-4,T-24*tk];p=[x,-.4]}
      else if(act==="ksout"||act==="ksblock"){h=[x*(pr.shW+2),T+4*tk];p=[x*.4,1]}
      else if(act==="ksguard"){h=[x*-2,T+22*tk];p=[x,.3]}
      else if(act==="neck"){h=[x*-7,T-2*tk];p=[x,.6]}          // knife hand ends at neck height, palm up
      else if(act==="backfist"||act==="bfside"){h=[x*3,T-14*tk];p=[x,.2]}
      else if(act==="hammer")h=[x*(pr.shW+30),T+16*tk];
      else if(act==="elbow"){h=[x*-6,T+4*tk];p=[x,.2]}
      else if(act==="eltarget"||act==="grab"){h=[x*-8,T+6*tk];p=[x,.4]}
      else if(act==="houter"){h=[x*(pr.shW+4),T-14*tk];p=[x*.4,1]}
      else if(act==="twist"){h=[x*-2,T-4*tk];p=[x*.5,1]}
      else if(act==="spread"){h=[x*(pr.shW+12),hipY+12*k];p=[x,.2]}
      else if(act==="palm"){h=[x*-3,T+9*tk];p=[x*.5,1]}
      else if(act==="xlow"){h=[x*-3,hipY+4*k];p=[x,.4]}
      else if(act==="wedge"){h=[x*(pr.shW+6),T+2*tk];p=[x*.4,1]}
      else if(act==="uppercut"){h=[x*-2,T-2*tk];p=[x*.3,1]}
      else if(act==="cover"){h=[x*2,T+18*tk];p=[x,.3]}
      else if(act==="sidepunch")h=[x*(pr.shW+46),T+10*tk];
      else if(act==="ksside"){h=[x*(pr.shW+28),T+6*tk];p=[x*.3,1]}
      else if(act==="kslow"){h=[x*(pr.shW+12),hipY+6*k];p=[x,.2]}
      else if(act==="assist"){h=[x*-2,T+20*tk];p=[x,.3]}
      else if(act==="guard")h=[x*8,T+28*tk];
      else if(act==="tongmil"){h=[x*-1.5,T+15*tk];p=[x,.15]}   // hands meet below the chin, elbows out
      else if(act==="ksstrike"){h=[x*(pr.shW+30),T+2*tk];p=[x*.3,1]}
      else if(act==="ksdown"){h=[x*(pr.shW+6),T+14*tk];p=[x*.4,1]}
      else if(act==="kswedge"){h=[x*(pr.shW+6),T+2*tk];p=[x*.4,1]}
      else if(act==="heaven"){h=[x*-2,T-26*tk];p=[x,-.3]}
      else if(act==="kxcheck"){h=[x*-4,T+10*tk];p=[x,.4]}
      else if(act==="arc"||act==="palmjaw"){h=[x*-3,T+5*tk];p=[x,.3]}
      else if(act==="tgrab"){h=[x*-3,T+14*tk];p=[x,.3]}
      else if(act==="lspear"){h=[x*-3,hipY-1];p=[x,.2]}
      else if(act==="kneebreak"){h=[x*-2,hipY+12*k];p=[x,.2]}
      else if(act==="hold"){h=[x*(pr.hipW+8),hipY-16*tk];p=[x,.2]}
      else if(act==="target"){h=[x*(pr.shW+30),T+8*tk];p=[x*.2,1]}
      else if(act==="crosspunch"){h=[x*-(pr.shW+14),T+8*tk];p=[x*.2,1]}
      else if(act==="shoulder"){h=[x*-(pr.shW-5),T+5*tk];p=[x,.6]}
      else if(act==="pressdown"){h=[x*-2,T+30*tk];p=[x,.3]}
      else if(act==="sideelbow"){h=[x*(pr.shW+3),T+11*tk];p=[x,.05]}   // arm folded, elbow driven out to the side
      else if(act==="elbowpush"){h=[x*-(pr.shW+1),T+12*tk];p=[x,.3]}
      else if(act==="hammerlow"){h=[x*-1,hipY-5*k];p=[x,.2]}
      else if(act==="palmlow"){h=[x*-1,hipY-8*k];p=[x,.2]}
      else if(act==="ksin"){h=[x*-3,T+9*tk];p=[x*.5,1]}
      else if(act==="hingepunch"){h=[x*-(pr.shW+4),T+11*tk];p=[x*.3,1]}
      else if(act==="hingetop"){h=[x*-(pr.hipW+6),hipY-18*tk];p=[x,.3]}
      else if(act==="hammerout"){h=[x*(pr.shW+40),T+6*tk];p=[x*.2,1]}
      else if(act==="kspread"){h=[x*(pr.shW+12),hipY+12*k];p=[x,.2]}
      else if(act==="gyeopson"){h=[x*-1.5,hipY+3];p=[x,.2]}       // gyeopson junbi: open hands overlapped in front of the lower belly
      else if(act==="upelbow"){h=[x*-6,T+4*tk];p=[x,.2]}
      else if(act==="sidebf"){h=[x*(pr.shW+26),T-6*tk];p=[x,-.3]}   // back-fist out to the side at head height
      else if(act==="crossbf"){h=[x*-(pr.shW+6),T-6*tk];p=[x,.3]}   // back-fist across the body to the other side
      else if(act==="bull"){h=[x*11,T-19*tk];p=[x,.5]}                // hwangso makki: fists above the forehead, elbows out
      else if(act==="passist"){h=[x*-(pr.shW-2),T+8*tk];p=[x,.4]}   // open palm at the other arm's wrist
      else if(act==="rockhi"){h=[x*5,T-20*tk];p=[x,.2]}
      else if(act==="rocklo"){h=[x*-2,T+2*tk];p=[x,.4]}
      else if(act==="rwedge"){h=[x*(pr.shW+6),T+2*tk];p=[x*.4,1]}
      else if(act==="lift"){h=[x*-1,T+14*tk];p=[x,.6]}
      else if(act==="kxlow"){h=[x*-3,hipY+4*k];p=[x,.4]}
      else if(act==="htarget"){h=[x*(pr.shW+26),T+3*tk];p=[x*.2,1]}  // target hand out to the side, kept below the face
      else if(act==="hammerin"){h=[x*-(pr.shW+17),T+4*tk];p=[x*.2,1]}
      else if(act==="lowside"){h=[x*(pr.shW+24),hipY-2*k];p=[x,.1]}   // naeryeo yeop makki: forearm swept down and out to the side
      else if(act==="wing"){h=[x*(pr.shW+22),T+2*tk];p=[x*.2,1]}        // nalgae pyeogi: palms pushed out to the sides at shoulder height
      else if(act==="khopen"){h=[x*(pr.shW+9),T-15*tk];p=[x*.4,1]}      // knife hands spread above the shoulders
      else if(act==="twistm"){h=[x*-2,T+5*tk];p=[x*.5,1]}
      else if(act==="wesc"){h=[x*(pr.shW+4),T+16*tk];p=[x,.3]}
      else if(act==="swing"||act==="swingo"||act==="ohouter"){h=[x*(pr.shW+4),T-14*tk];p=[x*.4,1]}
      else if(act==="pushlo"){h=[x*-1,hipY-7*k];p=[x,.3]}
      else if(act==="pushhi"){h=[x*-3,T+7*tk];p=[x,.3]}            // drawn at the chest so it never crosses the face
      else if(act==="bamup"){h=[x*-3,T+7*tk];p=[x*.3,1]}           // double knuckle uppercut, kept below the face
      else if(act==="hammerin2"){h=[x*(pr.shW-3),T+11*tk];p=[x*.3,1]}  // fists level with the edges of the body
      else if(act==="xhigh"){h=[x*-3,T-23*tk];p=[x,-.3]}            // wrists crossed above the forehead
      else if(act==="grabtw"){h=[x*-2,T+8*tk];p=[x,.3]}
      else h=[x*6.5,hipY-12*tk];                                 // junbi
      addArm(Lay.arms,sh,h,p,false,OPEN.has(act));
    }
  });
  const hs=pr.head,Hc=[0,T-10.4*hs-2.6];
  Lay.head.head={c:Hc,s:hs,ang:0,view:back?"back":"front"};
  Lay.head.neck={pts:[[-4.3*hs,Hc[1]+6*hs],[4.3*hs,Hc[1]+6*hs],[5.4,T+2],[-5.4,T+2]]};
  const ww=pr.waist;
  Lay.torso.torso={
    pts:[[-5.6,T-.6],[-13*sw,T+1.6],[-19.6*sw,T+4.8],[-21*sw,T+9],[-18.6*sw,T+24*tk],[-14.6*hw*ww,hipY-8],[-16.8*hw,hipY+12],[0,hipY+13.4],[16.8*hw,hipY+12],[14.6*hw*ww,hipY-8],[18.6*sw,T+24*tk],[21*sw,T+9],[19.6*sw,T+4.8],[13*sw,T+1.6],[5.6,T-.6]],
    collar:back?openCurve([[-6.5,T+.4],[0,T+3.2],[6.5,T+.4]]):openCurve([[-6,T-.2],[-2,T+9*tk],[1.4,T+20*tk]])+openCurve([[6,T-.2],[2.4,T+8*tk],[-1.4,T+15*tk]]),
    lapel:back?openCurve([[0,T+5],[0,hipY-8]]):openCurve([[1.4,T+20*tk],[3.6,T+34*tk],[5.6*hw,hipY-8]]),
    under:back?"":ln([5.6*hw,hipY-1],[6.2*hw,hipY+12.8]),
    gather:openCurve([[-8*hw,hipY-.2],[-9*hw,hipY+5]])+openCurve([[8*hw,hipY-.2],[9*hw,hipY+5]]),
    band:[[-15*hw*ww,hipY-6.8],[15*hw*ww,hipY-6.8],[15.1*hw*ww,hipY-2],[-15.1*hw*ww,hipY-2]],
    tails:back?[]:[[[0,hipY-3],[-4.6,hipY+14]],[[0,hipY-3],[4.6,hipY+14]]],
    knot:back?null:[[-3.6,hipY-8.6],[3.6,hipY-8.6],[3.6,hipY+.2],[-3.6,hipY+.2]],
    shadeA:[-20,T+20],shadeB:[20,T+20]
  };
  return{k,hands:HANDS,mirror:false,layers:back?[Lay.arms,Lay.farLeg,Lay.nearLeg,Lay.head,Lay.torso,Lay.kick]:[Lay.farLeg,Lay.nearLeg,Lay.head,Lay.torso,Lay.arms,Lay.kick]};
}

/* ---------- head shapes (local units, x forward / y down) ---------- */
const HEAD_SIDE=[[-8.6,-1],[-7.6,-7.6],[-3,-11],[3,-10.8],[7.2,-7.4],[8.1,-3.4],[8.9,-1.2],[9.6,.4],[8.4,1.5],[8.6,3.4],[8.1,5.1],[7.4,7.3],[4.8,9.3],[.6,9],[-4.6,6.4],[-7.6,3.6]];
const HEAD_FRONT=[[0,-11],[5.8,-9.6],[8,-4.4],[7.9,1],[6.6,6],[3.6,9.2],[0,10.2],[-3.6,9.2],[-6.6,6],[-7.9,1],[-8,-4.4],[-5.8,-9.6]];
const HAIR={
  short:{side:[[6.6,-7.6],[2.5,-11.5],[-3.8,-11.4],[-8.8,-6],[-9.2,0],[-8,4.2],[-6.2,4.6],[-5.4,.2],[-3.4,-3.6],[.6,-5.8],[5,-6]],
         front:[[-8.3,-3],[-7,-9.2],[0,-11.8],[7,-9.2],[8.3,-3],[7.4,-3.6],[5.2,-7.2],[0,-7.8],[-5.2,-7.2],[-7.4,-3.6]]},
  part:{side:[[7.4,-6.6],[3,-11.8],[-3.8,-11.9],[-9,-6.2],[-9.4,.6],[-8,4.8],[-6,5],[-5.4,0],[-3,-3.8],[1.6,-5.2],[6.4,-4.4]],
         front:[[-8.5,-2.4],[-7.3,-9.5],[-1,-12.1],[7.2,-9.8],[8.5,-2.6],[7.4,-3.8],[4.6,-7],[-2.4,-7.4],[-4.6,-5.6],[-7.5,-3.4]]},
  crop:{side:[[6,-8.2],[2.4,-11.2],[-3.6,-11.1],[-8.4,-6],[-8.8,-.6],[-7.6,2.8],[-6.2,3],[-5.4,-.8],[-3,-4.4],[.6,-6.6],[4.6,-6.9]],
         front:[[-8.1,-4],[-6.8,-9.1],[0,-11.4],[6.8,-9.1],[8.1,-4],[7.2,-4.6],[5,-7.8],[0,-8.4],[-5,-7.8],[-7.2,-4.6]]},
  bun:{side:[[7,-7],[2.6,-11.7],[-4,-11.5],[-8.9,-6],[-9.3,0],[-8,4.4],[-6,4.6],[-5.3,0],[-3.2,-4],[1.4,-6],[6,-5.6]],
         front:[[-8.4,-2.4],[-7.1,-9.4],[0,-11.9],[7.1,-9.4],[8.4,-2.4],[7.5,-3.2],[6,-6.8],[0,-8.4],[-6,-6.8],[-7.5,-3.2]],
         bun:{side:[-8.6,-8.4,4.6],front:[0,-12.6,4.4],back:[0,-7.4,5]}}
};

/* ---------- renderer ---------- */
// opt.only: "arm" draws just the arms (ghost arms); "upper" leaves out the legs (arm-only thumbnails).
// opt.fadeLegs: legs drawn light (same stance as the previous count).
function draw(sk,D,opt={}){
  const bc=BELTS[belt],O=D.ink,pr=D.pr;
  let defs="";
  const grad=(A,B,c1,c2)=>{const id="g"+(++gid);defs+=`<linearGradient id="${id}" gradientUnits="userSpaceOnUse" x1="${f(A[0])}" y1="${f(A[1])}" x2="${f(B[0])}" y2="${f(B[1])}"><stop offset="0" stop-color="${c1}"/><stop offset=".55" stop-color="${c1}"/><stop offset="1" stop-color="${c2}"/></linearGradient>`;return`url(#${id})`};
  const out=sk.layers.filter(L=>!opt.only||(opt.only==="arm"?L.part==="arm":L.part!=="leg")).map(L=>{
    const gi=L.far?D.giFar:D.gi,skin=L.far?D.skinFar:D.skin,hair=D.hair;
    const shapes=[];let det="";
    L.legs.forEach(l=>{
      const W=pr.legW.map((w,i)=>w*(l.front?1.08:1)+(i===TS.length-1?pr.flare:0));
      const c=contour(l.ch,W,true);shapes.push({d:spline(c.pts),c});
      const e=c.mid[TS.length-1],a=add(e.p,mul(e.d,-.6));det+=ln(add(a,mul(e.n,e.w*.96)),add(a,mul(e.n,-e.w*.96)));
      if(D.folds){const kk=c.mid[4];det+=openCurve([add(kk.p,mul(kk.n,-kk.w*.2)),add(add(kk.p,mul(kk.d,3)),mul(kk.n,-kk.w*.65))]);
        const sh=c.mid[6];det+=ln(add(sh.p,mul(sh.n,sh.w*.3)),add(c.mid[7].p,mul(c.mid[7].n,c.mid[7].w*.35)))}
    });
    L.arms.forEach(a=>{
      const W=pr.armW.map((w,i)=>w*(a.front?1.05:1)+(i===TS.length-1?pr.flare*.8:0));
      const c=contour(a.ch,W,true);shapes.push({d:spline(c.pts),c});
      if(!a.front){const e=c.mid[TS.length-1];det+=ln(add(e.p,mul(e.n,e.w*.96)),add(e.p,mul(e.n,-e.w*.96)))}
      if(D.folds&&!a.front){const el=c.mid[4];det+=openCurve([add(el.p,mul(el.n,el.w*.15)),add(add(el.p,mul(el.d,-3.2)),mul(el.n,el.w*.75))])+openCurve([add(c.mid[6].p,mul(c.mid[6].n,-c.mid[6].w*.7)),add(c.mid[7].p,mul(c.mid[7].n,-c.mid[7].w*.1))])}
    });
    if(L.torso){shapes.push({d:spline(L.torso.pts,1.1),torso:true});det+=L.torso.lapel+L.torso.under+(D.folds?L.torso.gather:"")}
    let g="";
    if(shapes.length){
      const all=shapes.map(s=>s.d).join("");
      g+=`<path d="${all}" fill="none" stroke="${O}" stroke-width="${D.ow*2}" stroke-linejoin="round"/>`;
      shapes.forEach(s=>{
        let fill=gi;
        if(D.shade){
          if(s.c){const m=s.c.mid[4];fill=grad(add(m.p,mul(m.n,m.w)),add(m.p,mul(m.n,-m.w)),gi,L.far?D.shadeFar:D.shadeCol)}
          else fill=grad(L.torso.shadeA,L.torso.shadeB,gi,D.shadeCol);
        }
        g+=`<path d="${s.d}" fill="${fill}"/>`;
      });
      if(det)g+=`<path d="${det}" fill="none" stroke="${O}" stroke-width="${D.dw}" stroke-linecap="round" stroke-linejoin="round"/>`;
    }
    const skinPath=d=>g+=`<path d="${d}" fill="${skin}" stroke="${O}" stroke-width="${D.sw}" stroke-linejoin="round"/>`;
    L.feet.forEach(ft=>skinPath(spline(ft.pts)));
    L.fists.forEach(q=>{
      if(q.front&&q.flat){skinPath(spline(xf(KNIFE_FACE,q.c,0,1.05,1.05)))}
      else if(q.front){skinPath(spline(xf(FIST_FACE,q.c,0,1.05,1.05)));g+=`<path d="${[-2.7,0,2.7].map(x=>ln([q.c[0]+x,q.c[1]-4],[q.c[0]+x,q.c[1]-.6])).join("")}" stroke="${O}" stroke-width="${D.dw}" stroke-linecap="round"/>`}
      else if(q.flat){const ang=Math.atan2(q.d[1],q.d[0]);skinPath(spline(xf(HAND_FLAT,q.w,ang,pr.fist,pr.fist)));g+=`<path d="${openCurve(xf([[4,1.4],[8.6,1.6],[12,1.1]],q.w,ang,pr.fist,pr.fist))}" fill="none" stroke="${O}" stroke-width="${D.dw}" stroke-linecap="round"/>`}
      else{const ang=Math.atan2(q.d[1],q.d[0]);skinPath(spline(xf(FIST,q.w,ang,pr.fist,pr.fist)));g+=`<path d="${openCurve(xf([[3.2,1.4],[6,1.9],[8.4,1.6]],q.w,ang,pr.fist,pr.fist))}" fill="none" stroke="${O}" stroke-width="${D.dw}" stroke-linecap="round"/>`}
    });
    if(L.neck)skinPath(spline(L.neck.pts,1.4));
    if(L.head){
      const h=L.head,Hd=HAIR[pr.hair],bun=Hd.bun;
      const loc=P=>xf(P,h.c,h.ang,h.s,h.s);
      const hairPath=d=>g+=`<path d="${d}" fill="${hair}" stroke="${O}" stroke-width="${D.sw}" stroke-linejoin="round"/>`;
      if(bun&&h.view!=="back"){const b=bun[h.view];hairPath(spline(ellPts(loc([[b[0],b[1]]])[0],b[2]*h.s,b[2]*h.s*.9)))}
      if(h.view==="side"){
        skinPath(spline(loc(HEAD_SIDE)));
        hairPath(spline(loc(Hd.side)));
        skinPath(spline(ellPts(loc([[-2.2,.6]])[0],1.9*h.s,2.9*h.s,h.ang)));
      }else if(h.view==="front"){
        [-1,1].forEach(s=>skinPath(spline(ellPts(loc([[s*7.8,.6]])[0],1.7*h.s,2.8*h.s))));
        skinPath(spline(loc(HEAD_FRONT)));
        hairPath(spline(loc(Hd.front)));
      }else{
        [-1,1].forEach(s=>skinPath(spline(ellPts(loc([[s*7.8,.6]])[0],1.7*h.s,2.8*h.s))));
        hairPath(spline(loc(HEAD_FRONT.map(([x,y])=>[x*1.02,y<6?y*1.02:y*.86]))));
        if(bun){const b=bun.back;hairPath(spline(ellPts(loc([[b[0],b[1]]])[0],b[2]*h.s,b[2]*h.s*.92)))}
      }
    }
    if(L.torso){
      const t=L.torso;
      g+=`<path d="${t.collar}" fill="none" stroke="${D.collarCol||O}" stroke-width="${D.collar}" stroke-linecap="round" stroke-linejoin="round"/>`;
      let b=spline(t.band,2);t.tails.forEach(([a,c])=>{const d=norm(sub(c,a)),n=[-d[1],d[0]];b+=spline([add(a,mul(n,1.5)),add(c,mul(n,1.4)),add(c,mul(n,-1.4)),add(a,mul(n,-1.5))],3)});
      if(t.knot)b+=spline(t.knot,2);
      g+=`<path d="${b}" fill="${bc}" stroke="${O}" stroke-width="${D.dw}" stroke-linejoin="round"/>`;
    }
    return opt.fadeLegs&&L.part==="leg"&&g?`<g opacity=".3">${g}</g>`:g;
  }).join("");
  return{defs,out};
}


/* ---------- figure: Textbook line A1 "Natural" ---------- */
const LEG=[9.8,9.5,8.7,7.7,7.4,7.3,7,7.2,7.9],ARM=[6.6,6.3,5.9,5.4,5.1,5,4.9,5.1,5.8];
const PR={thigh:33,shin:32,upper:24,fore:23,torso:55,head:.95,shW:18.5,hipW:9,waist:1,legW:LEG,armW:ARM,flare:.6,fist:.95,foot:1,hair:"short"};
const STY={ink:"#1b2030",gi:"#fdfdfb",giFar:"#dfe3ea",skin:"#ecd0b6",skinFar:"#cfb39b",hair:"#2a2f3a",ow:1.45,dw:1,sw:1.6,collar:3.2,pr:PR};
/* opt (same-stance treatments, issue #4):
     fade   legs drawn light: the stance is carried over from the previous count
     from   the previous move: a dashed arc from where each changed hand was to where it ends
     ghosts earlier counts on the same stance, drawn as light arms only
     badges [{m,label,on}]: count numbers at the hand that acts in each count
     crop   upper body only, cropped (arm-only thumbnail) */
const actHand=m=>m.hand&&m.hand.length===1?m.hand:(["R","L"].find(s=>m.arms&&m.arms[s]&&m.arms[s]!=="chamber")||"R");
function motionArc(p,q){
  const d=dist(p,q);if(d<4)return"";
  const mid=lerp(p,q,.5),n=norm([-(q[1]-p[1]),q[0]-p[0]]),c0=[0,-28];
  const c=add(mid,mul(n,(dist(add(mid,n),c0)>dist(sub(mid,n),c0)?1:-1)*Math.min(d*.35,14)));
  const t=norm(sub(q,c)),a=sub(q,mul(t,1.2)),w=[-t[1],t[0]];
  return`<path d="M${f(p[0])} ${f(p[1])}Q${f(c[0])} ${f(c[1])} ${f(a[0])} ${f(a[1])}" fill="none" stroke="var(--fire)" stroke-width="1.5" stroke-dasharray="3 2.2" stroke-linecap="round"/>`+
    `<path d="M${f(q[0]+t[0]*1.5)} ${f(q[1]+t[1]*1.5)}L${f(a[0]-t[0]*3+w[0]*3)} ${f(a[1]-t[1]*3+w[1]*3)}L${f(a[0]-t[0]*3-w[0]*3)} ${f(a[1]-t[1]*3-w[1]*3)}Z" fill="var(--fire)"/>`;
}
/* Per-move images (#7): when the page defines FIGIMG (build_form.py --images, from design/moves/<form>/),
   a count with an image is drawn from it instead of the vector figure, on the same ground line and scale
   (142 units = standing height; r = the image's share of it). Ghost arms and motion arcs need the vector
   skeleton, so they are left out on image figures. */
function figImage(m,opt){
  const I=FIGIMG[m.id],h=142*I.r,w=I.w/I.h*h;
  const img=`<image href="${I.src}" x="${f(-w/2)}" y="${f(65-h)}" width="${f(w)}" height="${f(h)}" preserveAspectRatio="none"${opt.fade?' opacity=".5"':""}/>`;
  return`<svg class="body${opt.crop?" crop":""}" viewBox="${opt.crop?"-62 -90 124 100":"-62 -90 124 160"}" role="img" aria-label="${T[m.tech][2]}">`+
    (opt.crop?"":`<ellipse class="glow" cx="0" cy="64.5" rx="50" ry="5.5" fill="none" stroke="var(--fire)" stroke-width="2"/>`+
    `<ellipse cx="0" cy="64" rx="40" ry="4" fill="var(--ink)" opacity=".09"/>`)+img+`</svg>`;
}
function figure(m,opt={}){
  if(typeof FIGIMG!=="undefined"&&FIGIMG[m.id])return figImage(m,opt);
  const sk=skel(m,PR),{out}=draw(sk,STY,{fadeLegs:opt.fade,only:opt.crop?"upper":null});
  let under="",over="",marks="";
  if(opt.from){const pk=skel(opt.from,PR);
    const s=actHand(m),a=(opt.from.arms||{})[s]||"chamber",b=(m.arms||{})[s]||"chamber";   // the acting hand only: two arcs read as noise
    if(a!==b&&pk.hands[s]&&sk.hands[s])over+=motionArc(pk.hands[s],sk.hands[s])}
  (opt.ghosts||[]).forEach(g=>{under+=`<g opacity=".32">${draw(skel(g,PR),STY,{only:"arm"}).out}</g>`});
  const placed=[];
  (opt.badges||[]).forEach(b=>{const h=skel(b.m,PR).hands[actHand(b.m)];if(!h)return;
    let x=sk.mirror?-h[0]:h[0],y=h[1]-9;const w=b.label.length*3.6+5;
    while(placed.some(([px,py])=>Math.abs(px-x)<w&&Math.abs(py-y)<10))y-=10.5;   // stack badges that would overlap
    placed.push([x,y]);
    marks+=`<g class="badge${b.on?" on":""}"><rect x="${f(x-w/2)}" y="${f(y-4.6)}" width="${f(w)}" height="9.2" rx="4.6" fill="${b.on?"var(--fire)":"var(--surface)"}" stroke="var(--fire)" stroke-width="1"/>`+
      `<text x="${f(x)}" y="${f(y+2.1)}" text-anchor="middle" font-size="6.2" font-family="IBM Plex Mono,monospace" fill="${b.on?"#fff":"var(--fire)"}">${b.label}</text></g>`});
  const inner=under+out+over;
  return`<svg class="body${opt.crop?" crop":""}" viewBox="${opt.crop?"-62 -90 124 100":"-62 -90 124 160"}" role="img" aria-label="${T[m.tech][2]}">`+
    (opt.crop?"":`<ellipse class="glow" cx="0" cy="64.5" rx="50" ry="5.5" fill="none" stroke="var(--fire)" stroke-width="2"/>`+
    `<ellipse cx="0" cy="64" rx="40" ry="4" fill="var(--ink)" opacity=".09"/>`)+
    (sk.mirror?`<g transform="scale(-1,1)">${inner}</g>`:inner)+marks+`</svg>`;
}

/* ---------- stance footprints (top view, na = up) ----------
   Ap seogi: one natural step, feet nearly in line.
   Ap kubi: about 1½ steps long and one fist wide, rear foot turned out. */
const FT=[[0,-7.4],[3,-5.6],[3.5,1.5],[2.4,6.3],[0,7.4],[-2.4,6.3],[-3.5,1.5],[-3,-5.6]];
function feet(m){
  if(m.stance==="ogeum"||m.stance==="oneleg")m={...m,stance:"crane"};
  if(m.stance==="sasun")m={...m,stance:"horse"};
  if(m.stance==="fixed"||m.stance==="vertical")m={...m,stance:"back"};
  if(m.stance==="lowst")m={...m,stance:"front"};
  const rot={na:0,ga:180,na4:0,na5:0,ga4:180,ga5:180,gada2:135,nada2:45,gara2:-135,nara2:-45,da1:90,da2:90,da3:90,ra1:-90,ra2:-90,ra3:-90,gada:135,nada:45,gara:-135,nara:-45}[m.dir]*Math.PI/180;
  const sgn=s=>s==="L"?-1:1,other=s=>s==="L"?"R":"L";
  const foot=(x,y,a,on)=>`<path d="${spline(xf(FT,[x,y],a))}" fill="${on?"var(--fire)":"var(--muted)"}"/>`;
  let s="";
  if(m.stance==="ready")s=foot(-6.5,1,0,0)+foot(6.5,1,0,0);
  else if(m.stance==="walk"){const l=sgn(m.lead),o=sgn(other(m.lead));
    s=foot(l*2.6,-6,0,1)+foot(o*2.6,6.5,o*.5,0)+`<path d="M-11 -6H11M-11 6.5H11" stroke="var(--line)" stroke-width="1" stroke-dasharray="2 2"/>`;}
  else if(m.stance==="front"){const l=sgn(m.lead),o=sgn(other(m.lead));
    s=`<path d="M${l*7} -12V12M${o*7} -12V12" stroke="var(--line)" stroke-width="1" stroke-dasharray="2 2"/>`+foot(l*7,-11,0,1)+foot(o*7,11,o*.5,0);}
  else if(m.stance==="tiger"){const l=sgn(m.lead),o=sgn(other(m.lead));  // beom seogi: short, front foot on the ball
    s=foot(l*1.5,-6,0,1)+foot(o*3,6,o*.6,0);}
  else if(m.stance==="horse")s=foot(-11,1,0,0)+foot(11,1,0,0)+`<path d="M-11 -9V11M11 -9V11" stroke="var(--line)" stroke-width="1" stroke-dasharray="2 2"/>`;
  else if(m.stance==="close")s=foot(-3.5,1,0,0)+foot(3.5,1,0,0);
  else if(m.stance==="crane"){const l=sgn(m.lead),o=sgn(other(m.lead));  // hakdari seogi: one foot down, the other lifted to the knee
    s=foot(l*3,1,0,1)+`<circle cx="${o*5}" cy="1" r="4.6" fill="none" stroke="var(--muted)" stroke-width="1.4" stroke-dasharray="2 1.6"/>`;}
  else if(m.stance==="cross"){const l=sgn(m.lead),o=sgn(other(m.lead));
    s=foot(l*1.5,-3,0,1)+foot(o*-2,7,o*.4,0);}
  else if(m.stance==="gyeot"){const l=sgn(m.lead),o=sgn(other(m.lead));   // gyeotdari seogi: rear foot close behind and beside the front heel
    s=foot(l*2,-4,0,1)+foot(o*2.5,6,o*.35,0);}
  else if(m.stance==="back"){const l=sgn(m.lead),o=sgn(other(m.lead));   // dwit kubi: an L shape, rear foot turned 90° out
    s=`<path d="M0 -14V13" stroke="var(--line)" stroke-width="1" stroke-dasharray="2 2"/>`+foot(0,-8,0,1)+foot(o*3,9,o*Math.PI/2,0);}
  else if(m.stance==="nieun"){const o=sgn(other(m.lead));   // nieunja seogi: a short L, heels about one foot apart
    s=foot(0,-4,0,1)+foot(o*3,6,o*Math.PI/2,0);}
  else{const l=sgn(m.lead),o=sgn(other(m.lead));
    s=foot(o*4,7,0,0)+`<path d="M${l*4} 9V-12M${l*4-3.8} -7.5L${l*4} -12.5L${l*4+3.8} -7.5" stroke="var(--fire)" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;}
  return`<svg class="fp" viewBox="-21 -21 42 42" aria-hidden="true"><circle r="20" fill="var(--surface)" stroke="var(--line)"/><g transform="rotate(${f(rot*180/Math.PI)})">${s}<path d="M0 -20 l-3.2 4.4 h6.4z" fill="var(--heaven)"/></g></svg>`;
}

const sideWord=s=>s==="L"?"Left":"Right";
/* chip names per stance. ITF forms (FORM.family "itf") swap in the ITF names, and name the L-stance
   (niunja sogi) by the rear foot as the ITF does: "R · Niunja sogi" = right foot back, left foot forward. */
const CHIPN={ready:"Naranhi",kick:"Ap chagi",skick:"Yeop chagi",rkick:"Dollyeo chagi",knee:"Mureup",tiger:"Beom seogi",
  horse:"Juchum seogi",cross:"Kkoa seogi",gyeot:"Gyeotdari seogi",close:"Moa seogi",crane:"Hakdari",ogeum:"Ogeum seogi",fixed:"Gojung sogi",lowst:"Nachuo sogi",vertical:"Soojik sogi",oneleg:"Waebal sogi",sasun:"Sasun sogi",
  back:"Dwit kubi",nieun:"Nieunja seogi",walk:"Ap seogi",front:"Ap kubi"};
const CHIPCLS={ready:"ready",close:"ready",kick:"kick",skick:"kick",rkick:"kick",knee:"kick",tiger:"tiger",horse:"horse",
  crane:"crane",ogeum:"crane",oneleg:"crane",sasun:"horse",back:"back",nieun:"back",fixed:"back",vertical:"back",lowst:"front",walk:"walk",front:"front"};
let ITFNAMES=false;
function itfNames(){ITFNAMES=true;Object.assign(CHIPN,{ready:"Narani",front:"Gunnun sogi",back:"Niunja sogi",horse:"Annun sogi",kick:"Apcha busigi",skick:"Yopcha jirugi",crane:"Guburyo sogi",close:"Moa sogi",cross:"Kyocha sogi",tiger:"Dwitbal sogi"})}
const flipLR=s=>s==="L"?"R":"L";
const chipSide=m=>ITFNAMES&&(m.stance==="back"||m.stance==="tiger"||m.stance==="vertical")?flipLR(m.lead):m.lead;
function chip(m){
  const cls=CHIPCLS[m.stance]||"",nm=CHIPN[m.stance];
  if(["ready","horse","close"].includes(m.stance))return`<span class="chip ${cls}">${nm}</span>`;
  return`<span class="chip ${cls}">${chipSide(m)} · ${nm}</span>`;
}
function stanceLabel(m){
  if(m.stance==="ready")return"parallel";
  if(["kick","skick","rkick","knee"].includes(m.stance))return sideWord(m.lead)+" kick";
  if(m.stance==="horse"||m.stance==="close")return m.stance;
  if(ITFNAMES&&m.stance==="front")return sideWord(m.lead)+" walking";
  if(ITFNAMES&&m.stance==="back")return sideWord(flipLR(m.lead))+" L";
  if(ITFNAMES&&m.stance==="crane")return sideWord(m.lead)+" bending";
  if(ITFNAMES&&m.stance==="tiger")return sideWord(flipLR(m.lead))+" rear foot";
  if(m.stance==="vertical")return sideWord(flipLR(m.lead))+" vertical";
  if(m.stance==="oneleg")return sideWord(m.lead)+" one-leg";
  if(m.stance==="sasun")return sideWord(m.lead)+" diagonal";
  return sideWord(m.lead)+({walk:" walking",front:" front",back:" back",tiger:" tiger",cross:" cross",crane:" crane",nieun:" ㄴ-shape",gyeot:" assisting",ogeum:" reverse crane",fixed:" fixed",lowst:" low"})[m.stance];
}
