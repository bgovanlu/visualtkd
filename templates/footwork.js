/* Floor simulator (issue #3): where both feet are after every count, worked out from the move data.

   World frame, seen from above with na at the top of the page: x toward da (right), y toward ga (down).
   Units are foot lengths. You start in naranhi seogi at the origin facing ga.

   For each count the stance (with its lead foot) is placed against one planted foot:
   - the instruction names the foot that moves ("step back with the right foot", "draw the left foot"),
     so the other foot is planted; otherwise the planted foot is the one that keeps the step shortest,
     preferring to move the lead foot;
   - kicks leave the standing foot planted and put the kicking foot in the air, ahead;
   - "feet in place", "without stepping" and carried stances move nothing; "pivot in place" turns both
     feet about the centre; "jump" and "travelling toward …" move both feet;
   - a move's optional `step` field overrides all of this: {"plant":"L"|"R"|"both"|"none", "move":[forward,right]
     (both feet shift by this, in foot lengths relative to the facing; implies plant "none"), "horse":"along"
     (horse stance straddling the line of travel instead of across it)}.
   Returns one entry per move: {feet:{L,R} (each {p:[x,y], a:angle, air}), prev, moved:[sides], how, pivot}.
   Usable in the browser (inlined) and in Node (module.exports) for the checks in tools/check/footwork.py. */
const FW=(()=>{
const DIRV={na:[0,-1],ga:[0,1],da1:[1,0],da2:[1,0],da3:[1,0],ra1:[-1,0],ra2:[-1,0],ra3:[-1,0],
  gada:[Math.SQRT1_2,Math.SQRT1_2],nada:[Math.SQRT1_2,-Math.SQRT1_2],gara:[-Math.SQRT1_2,Math.SQRT1_2],nara:[-Math.SQRT1_2,-Math.SQRT1_2]};   // diagonals (Hansu)
// stance shapes: lead foot relative to the other foot, in the body frame [forward, toward the lead foot's side]
const SHAPE={ready:[0,.8],close:[0,.42],walk:[1.6,.42],front:[2.7,.85],back:[2.1,0],nieun:[1.1,0],gyeot:[.6,.15],tiger:[1.1,.3],
  horse:[0,2.4],cross:[.6,-.2],crane:[0,.32]};
// how far the rear foot turns out (degrees) and which way: outward = away from the lead foot's side
const TURN={walk:15,front:30,back:90,nieun:90,tiger:30,cross:20,gyeot:20};
const KICK=new Set(["kick","skick","rkick","knee"]);
const other=s=>s==="L"?"R":"L";
const ang=v=>Math.atan2(v[1],v[0]);
const rot=(v,a)=>[v[0]*Math.cos(a)-v[1]*Math.sin(a),v[0]*Math.sin(a)+v[1]*Math.cos(a)];
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],sub=(a,b)=>[a[0]-b[0],a[1]-b[1]],mul=(a,k)=>[a[0]*k,a[1]*k];
const len=a=>Math.hypot(a[0],a[1]);
// the person's right, for a facing vector in this frame (x right, y down): facing ga [0,1] -> right is ra [-1,0]
const rightOf=f=>[-f[1],f[0]];

function said(m){
  const d=(m.desc||"").toLowerCase();
  const mv=d.match(/\b(?:step|stepping|steps|slide|sliding|draw|drawing|bring|bringing|move|moving|cross|crossing|set|setting|pull|pulling|stamp|stamping|lift|lifting)\b[^.;:]*?\b(left|right) foot/);
  const pv=d.match(/pivot(?:ing)? on the (left|right) foot|on the (left|right) foot/);
  return{
    moving:mv?(mv[1]==="left"?"L":"R"):null,
    planted:pv?((pv[1]||pv[2])==="left"?"L":"R"):null,
    still:/feet in place|without stepping|^hold|holding the stance/.test(d),
    pivotInPlace:/pivot(?:ing)? in place/.test(d),
    jump:/\bjump/.test(d),
    landThen:/\bland(?:s|ing)?\b[^.]*?\bthen\b/.test(d),
    travel:(d.match(/travell?ing toward (na|ga|da|ra)/)||[])[1]
  };
}

// both feet for stance m with foot `plant` fixed at position P (its angle is recomputed)
function place(m,plant,P,face){
  const st=m.stance,lead=m.lead||"R",right=rightOf(face);
  const side=s=>s==="L"?mul(right,-1):right;           // unit vector toward that foot's side of the body
  const sh=SHAPE[st]||SHAPE.ready;
  let rel;   // position of the lead foot relative to the other foot
  const along=st==="horse"&&m.step&&m.step.horse==="along";   // horse stance straddling the line of travel
  if(along){const Pos={},A={},mv=other(plant);Pos[plant]=P;Pos[mv]=add(P,mul(face,sh[1]));
    A.L=A.R=ang(face)+Math.PI/2;return{L:{p:Pos.L,a:A.L},R:{p:Pos.R,a:A.R}}}
  if(st==="ready"||st==="close"||st==="horse")rel=mul(right,sh[1]);           // side by side: R is to the right
  else rel=add(mul(face,sh[0]),mul(side(lead),sh[1]));
  const sym=st==="ready"||st==="close"||st==="horse";
  const A={},Pos={};
  if(sym){Pos[plant]=P;Pos[other(plant)]=plant==="L"?add(P,rel):sub(P,rel)}
  else if(plant===lead){Pos[lead]=P;Pos[other(lead)]=sub(P,rel)}
  else{Pos[other(lead)]=P;Pos[lead]=add(P,rel)}
  const a0=ang(face);
  ["L","R"].forEach(s=>{
    let a=a0;
    if(!sym&&s!==lead&&TURN[st]){const out=s==="L"?-1:1;a=a0+out*TURN[st]*Math.PI/180}  // rear foot turned out
    A[s]=a;
  });
  return{L:{p:Pos.L,a:A.L},R:{p:Pos.R,a:A.R}};
}

function simulate(M){
  const out=[];let cur=null,air=null;
  M.forEach((m,i)=>{
    if(m.stance==="ogeum")m={...m,stance:"crane"};   // ogeum seogi stands like crane stance
    if(m.stance==="fixed"||m.stance==="vertical")m={...m,stance:"back"};    // ITF gojung sogi (fixed stance): an L-stance with the weight even
    if(m.stance==="lowst")m={...m,stance:"front"};   // ITF nachuo sogi (low stance): a long walking stance
    const face=DIRV[m.dir],S=said(m),st=m.stance,step=m.step||{};
    let feet,moved=[],how="";
    if(i===0||!cur){
      feet=place({stance:st==="ready"||st==="close"?st:"ready",lead:"R"},"L",[.4,0],face);
      feet.L.p=[.4,0];feet.R.p=[-.4,0];     // facing ga: left foot toward da (+x)
      cur=feet;out.push({feet,prev:null,moved,how:"start"});return;
    }
    const prev={L:{...cur.L},R:{...cur.R}};
    const centre=mul(add(prev.L.p,prev.R.p),.5);
    if(KICK.has(st)){
      // standing foot stays (turning to the kick); the kicking foot is in the air, ahead
      const k=m.lead||"R",s=other(k),right=rightOf(face);
      feet={[s]:{p:prev[s].p,a:ang(face)+(st==="skick"||st==="rkick"?(s==="L"?-1:1)*Math.PI/2:0)},
            [k]:{p:add(add(prev[s].p,mul(face,1.7)),mul(right,k==="R"?.35:-.35)),a:ang(face),air:true}};
      moved=[k];how=S.jump?"jump kick":"kick";
      if(S.jump){moved=["L","R"]}
    }else if(st==="crane"){
      const s=m.lead||"R",k=other(s);
      // step.plant naming the lifted foot: the standing foot is brought to it ("bring the right foot to the left foot")
      const at=m.step&&m.step.plant===k?add(prev[k].p,mul(rightOf(face),k==="R"?-.32:.32)):prev[s].p;
      feet={[s]:{p:at,a:ang(face)},[k]:{p:add(at,mul(rightOf(face),k==="R"?.32:-.32)),a:ang(face),air:true}};
      moved=m.step&&m.step.plant===k?[s,k]:[k];how="lift";
    }else{
      // candidates: plant either foot where it is, or keep the centre (pivot / jump / travel)
      const cand=["L","R"].map(pl=>{const fe=place(m,pl,prev[pl].p,face),mv=other(pl);
        return{fe,plant:pl,cost:len(sub(fe[mv].p,prev[mv].p)),mv}});
      const inPlace=()=>{const fe=place(m,"L",[0,0],face),c=mul(add(fe.L.p,fe.R.p),.5),d=sub(centre,c);
        fe.L.p=add(fe.L.p,d);fe.R.p=add(fe.R.p,d);return fe};
      let pick=null;
      const sameStance=prev&&out[i-1]&&!out[i-1].feet.L.air&&!out[i-1].feet.R.air&&M[i-1].stance===st&&M[i-1].lead===m.lead&&M[i-1].dir===m.dir;
      if(step.plant==="both"||((S.still||(sameStance&&!S.moving))&&!S.jump&&!S.travel&&m.carry!==false)){feet=prev;how="hold"}
      // horse stance turned to a new facing without naming a foot: the body turns about its centre
      else if(step.plant==="none"||step.move||S.jump||S.travel||S.pivotInPlace||
              (st==="horse"&&M[i-1].stance==="horse"&&M[i-1].dir!==m.dir&&!S.moving&&!(m.step&&m.step.horse))){
        feet=inPlace();
        const shift=step.move?add(mul(face,step.move[0]),mul(rightOf(face),step.move[1]||0)):(S.travel?mul(DIRV[S.travel+(S.travel==="na"||S.travel==="ga"?"":"1")],2.2):S.jump?mul(face,1.4):null);
        if(shift){feet.L.p=add(feet.L.p,shift);feet.R.p=add(feet.R.p,shift)}
        moved=["L","R"].filter(s=>len(sub(feet[s].p,prev[s].p))>.15);
        how=S.jump?"jump":S.travel?"turn and travel":"pivot";
      }else{
        if(step.plant)pick=cand.find(c=>c.plant===step.plant);
        else if(S.moving)pick=cand.find(c=>c.mv===S.moving);
        else if(S.planted)pick=cand.find(c=>c.plant===S.planted);
        else{
          // after a kick the kicking foot lands: the standing foot is planted
          const wasAir=["L","R"].find(s=>prev[s].air);
          if(wasAir&&S.landThen){   // "land, then turn …": the kicking foot lands ahead and is the pivot
            prev[wasAir]={...prev[wasAir],air:false};
            const fe=place(m,wasAir,prev[wasAir].p,face),mv=other(wasAir);pick={fe,plant:wasAir,mv};
          }
          else if(wasAir)pick=cand.find(c=>c.mv===wasAir);
          else{cand.sort((a,b)=>Math.abs(a.cost-b.cost)>.3?a.cost-b.cost:(a.mv===m.lead?0:1)-(b.mv===m.lead?0:1));pick=cand[0]}  // near-ties: the lead foot steps
        }
        feet=pick.fe;moved=[pick.mv].filter(s=>len(sub(feet[s].p,prev[s].p))>.15||prev[s].air);
        how=moved.length?"step":"pivot";
      }
    }
    const pivot=["L","R"].filter(s=>!moved.includes(s)&&!feet[s].air&&Math.abs(norma(feet[s].a-prev[s].a))>.2);
    cur={L:{...feet.L},R:{...feet.R}};
    out.push({feet:cur,prev,moved,how,pivot});
  });
  return out;
}
function norma(a){while(a>Math.PI)a-=2*Math.PI;while(a<-Math.PI)a+=2*Math.PI;return a}
return{simulate,DIRV};
})();
if(typeof module!=="undefined")module.exports=FW;

/* ---------- drawing (browser only: needs spline/xf/FT/f from figure.js) ----------
   Top view with na at the top of the page, like the floor plan. */
const FWDRAW=(()=>{
  // Z: scale set: u = svg units per foot length, k = footprint size, r = pivot ring, h = arrowhead
  const GLYPH={u:8.5,k:.78,r:7.5,h:3.6},PLAN={u:12,k:.4,r:3.6,h:2.6};
  let Z=GLYPH;
  const foot=(p,a,cls,k=Z.k)=>`<path class="${cls}" d="${spline(xf(FT,[p[0]*Z.u,p[1]*Z.u],a+Math.PI/2,k,k))}"/>`;
  function arrow(p,q,cls){
    const A=[p[0]*Z.u,p[1]*Z.u],B=[q[0]*Z.u,q[1]*Z.u],dx=B[0]-A[0],dy=B[1]-A[1],d=Math.hypot(dx,dy),h=Z.h;
    if(d<h*1.5)return"";
    const ux=dx/d,uy=dy/d,e=[B[0]-ux*h*1.4,B[1]-uy*h*1.4],s=[A[0]+ux*h,A[1]+uy*h];
    return`<path class="${cls}" d="M${f(s[0])} ${f(s[1])}L${f(e[0])} ${f(e[1])}"/>`+
      `<path class="${cls} head" d="M${f(e[0]+ux*h)} ${f(e[1]+uy*h)}L${f(e[0]-uy*h*.7)} ${f(e[1]+ux*h*.7)}L${f(e[0]+uy*h*.7)} ${f(e[1]-ux*h*.7)}Z"/>`;
  }
  const ring=(p,cls)=>`<circle class="${cls}" cx="${f(p[0]*Z.u)}" cy="${f(p[1]*Z.u)}" r="${Z.r}"/>`;
  // one count: previous feet outlined, new feet filled (red = lead / standing foot), the step as an arrow
  function glyph(sim,i,M){
    Z=GLYPH;const S=Z.u;
    const r=sim[i],m=M[i],F=r.feet,P=r.prev||F;
    const c=[(F.L.p[0]+F.R.p[0]+P.L.p[0]+P.R.p[0])/4,(F.L.p[1]+F.R.p[1]+P.L.p[1]+P.R.p[1])/4];
    const lead=m.stance==="crane"?m.lead:(m.lead||null);
    let g="";
    r.moved.forEach(s=>{if(!P[s].air)g+=foot(P[s].p,P[s].a,"was")});
    r.moved.forEach(s=>{g+=arrow(P[s].p,F[s].p,"step")});
    (r.pivot||[]).forEach(s=>{g+=ring(F[s].p,"pivot")});
    ["L","R"].forEach(s=>{g+=F[s].air?foot(F[s].p,F[s].a,"air"):foot(F[s].p,F[s].a,s===lead?"lead":"other")});
    const still=i>0&&!r.moved.length&&!(r.pivot||[]).length;   // no step: say so, or the glyph looks like a missing arrow
    const fv=FW.DIRV[m.dir],t=[fv[0]*27,fv[1]*27];
    return`<svg class="fp fw" viewBox="-30 -30 60 60" aria-hidden="true"><circle r="29" class="rim"/>`+
      `<g transform="translate(${f(-c[0]*S)} ${f(-c[1]*S)})">${g}</g>`+
      (still?`<text class="still" x="0" y="22.5">NO STEP</text>`:"")+
      `<path class="tick" transform="translate(${f(t[0])} ${f(t[1])}) rotate(${f(Math.atan2(fv[1],fv[0])*180/Math.PI+90)})" d="M0 -3.5L-3.2 2.2H3.2Z"/></svg>`;
  }
  // the whole form: every footprint labelled with the counts that stand on it, steps dashed.
  // Counts with no step (a block then a punch, "feet in place") are added to the label of the feet they stand on.
  function plan(sim,M){
    Z=PLAN;const S=Z.u;
    let xs=[],ys=[];sim.forEach(r=>["L","R"].forEach(s=>{xs.push(r.feet[s].p[0]);ys.push(r.feet[s].p[1])}));
    const x0=Math.min(...xs)-1.2,x1=Math.max(...xs)+1.2,y0=Math.min(...ys)-1.4,y1=Math.max(...ys)+1.2;
    let steps="";const spots=[];   // spots: {p,a,ids:[]} one per placed footprint
    const last={L:null,R:null};
    sim.forEach((r,i)=>{
      const P=r.prev;
      if(i===0){["L","R"].forEach(s=>{last[s]={p:r.feet[s].p,a:r.feet[s].a,ids:[0],start:true};spots.push(last[s])});return}
      r.moved.forEach(s=>{
        const q=r.feet[s];
        if(P&&!P[s].air)steps+=`<g data-i="${i}">${arrow(P[s].p,q.p,"step")}</g>`;
        if(!q.air){last[s]={p:q.p,a:q.a,ids:[i]};spots.push(last[s])}
      });
      (r.pivot||[]).forEach(s=>{steps+=`<g data-i="${i}">${ring(r.feet[s].p,"pivot")}</g>`});
      // a count with no step (block then punch, "feet in place", a pivot on the spot) is added to the feet it stands on
      ["L","R"].forEach(s=>{if(!r.moved.length&&!r.feet[s].air&&last[s]&&!last[s].ids.includes(i))last[s].ids.push(i)});
    });
    let prints="",labels="";
    spots.forEach(sp=>{
      const is=sp.ids.join(" ");
      prints+=`<g data-is="${is}">${foot(sp.p,sp.a,sp.start?"start":"print")}</g>`;
      // label: the count that put the foot here, then any no-step counts made on it
      const names=sp.ids.map(i=>M[i].id==="J"?"준비":M[i].id);
      const txt=names.length>3?names[0]+"…"+names[names.length-1]:names.join(" ");
      labels+=`<text data-is="${is}" x="${f(sp.p[0]*S)}" y="${f(sp.p[1]*S-4.6)}">${txt}</text>`;
    });
    return`<svg class="fwplan" viewBox="${f(x0*S)} ${f(y0*S)} ${f((x1-x0)*S)} ${f((y1-y0)*S)}" role="img" aria-label="Footwork for the whole form: every footprint, labelled with the counts that stand on it">`+
      `<text class="nesw" x="${f((x0+x1)/2*S)}" y="${f(y0*S+4)}">NA · 나</text>`+
      `<g class="steps">${steps}</g><g class="prints">${prints}</g><g class="labels">${labels}</g>`+
      `<g class="cur"></g></svg>`;
  }
  // highlight count i: its step and the footprints it uses in red, the feet you stand on outlined
  function mark(svg,sim,i){
    if(!svg)return;Z=PLAN;
    svg.querySelectorAll("[data-i]").forEach(e=>e.classList.toggle("on",+e.dataset.i===i));
    svg.querySelectorAll("[data-is]").forEach(e=>{const ids=e.dataset.is.split(" ").map(Number);
      e.classList.toggle("on",ids[0]===i&&i>0);e.classList.toggle("stand",ids.includes(i)&&!(ids[0]===i&&i>0))});
    const F=sim[i].feet;
    svg.querySelector(".cur").innerHTML=["L","R"].filter(s=>!F[s].air).map(s=>foot(F[s].p,F[s].a,"now",.46)).join("");
  }
  // one line for the caption under the plan
  const SIDE={L:"left",R:"right"};
  function say(sim,i,M){
    const r=sim[i],m=M[i];
    if(i===0)return"Ready: feet parallel, one foot-width apart.";
    if(r.how==="kick"||r.how==="jump kick")return`${r.how==="jump kick"?"Jumping kick":"Kick"} with the ${SIDE[m.lead||"R"]} leg; the ${SIDE[(m.lead||"R")==="L"?"R":"L"]} foot stays planted.`;
    if(r.how==="lift")return`Stand on the ${SIDE[m.lead]} foot; the ${SIDE[m.lead==="L"?"R":"L"]} foot lifts to the knee.`;
    if(!r.moved.length)return r.pivot&&r.pivot.length?`No step: pivot on the spot to face ${m.dir.replace(/\d/,"")}.`:"No step: the feet stay where they are; only the arms move.";
    if(r.moved.length===2)return r.how==="jump"?"Jump: both feet leave the floor and land together.":r.how==="pivot"?"Both feet pivot to the new facing.":"Both feet move (turn and travel).";
    const mv=r.moved[0],pl=mv==="L"?"R":"L";
    return`The ${SIDE[mv]} foot ${r.prev[mv].air?"lands":"steps"}; the ${SIDE[pl]} foot stays planted${r.pivot&&r.pivot.includes(pl)?" and pivots":""}.`;
  }
  return{glyph,plan,mark,say};
})();
