"""Authoring script used to write forms/taegeuk-5.json … taegeuk-8.json (kept for reference).

The JSON files are the source of truth and may have been edited since; re-running this
OVERWRITES them. Copy its helpers (mv, kick, refs, autopos) when writing a new form.
"""
import json, os
G={"L":"guard","R":"guard"}
def mv(id,dir,view,stance,lead,arms,tech,hand,desc,face=None,**kw):
    d={"id":id,"dir":dir,"view":view,"stance":stance}
    if face: d["face"]=face
    if lead: d["lead"]=lead
    d.update({"arms":arms,"tech":tech})
    if hand: d["hand"]=hand
    d.update(kw); d["desc"]=desc; return d
J=mv("J","na","front","ready",None,{"L":"junbi","R":"junbi"},"junbi",None,"Stand at na facing ga, feet parallel and one foot-width apart, fists in front of the belt.")
W=lambda s:"Right" if s=="R" else "Left"
w=lambda s:"right" if s=="R" else "left"
def kick(id,dir,view,leg,face=None,desc=None,**kw):
    return mv(id,dir,view,"kick",leg,G,"kick",leg,desc or f"{W(leg)} front kick.",face=face,foot=True,**kw)
def refs(n,board,vid):
    return [
  {"go":f"kukkiwon-t{n}","kind":"kuk","icon":"gate","src":"Kukkiwon · Official site","title":f"Taegeuk {n} Jang","desc":"The form’s official description and meaning.","url":f"https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo={board}&page={2 if n<8 else 1}&menuLevel=3&menuNo=72"},
  {"go":"kukkiwon-poomsae","kind":"kuk","icon":"gate","src":"Kukkiwon · Official site","title":"Poomsae index","desc":"Every official poomsae, Taegeuk 1–8 and the black-belt forms.","url":"https://www.kukkiwon.or.kr/eng/board/list?boardManagementNo=55&menuLevel=3&menuNo=72"},
  ({"go":f"video-t{n}","kind":"yt","icon":"play","src":"YouTube · Video","title":f"Taegeuk {n} Jang, full performance","desc":"Kukkiwon Digital Encyclopedia, published by Mookas TV.","url":f"https://www.youtube.com/watch?v={vid}"} if vid else
   {"go":f"video-t{n}","kind":"yt","icon":"channel","src":"YouTube · Playlist","title":"Kukkiwon Digital Encyclopedia series","desc":f"Mookas TV playlist of the full series, including Taegeuk {n} Jang.","url":"https://www.youtube.com/playlist?list=PL4lzP9nwMEv2A-vF-GaNNn2OdjXjZfA6k"}),
  {"go":"kukkiwon-youtube","kind":"yt","icon":"channel","src":"YouTube · Channel","title":"Kukkiwon World Taekwondo Headquarters","desc":"The official Kukkiwon channel.","url":"https://www.youtube.com/channel/UCaQb3jutLu15oSfhPh8FACQ"},
  {"go":"wt-poomsae-rules","kind":"wt","icon":"pdf","src":"World Taekwondo · PDF","title":"Poomsae Competition Rules and Interpretation","desc":"In force from 30 September 2024; how poomsae are judged.","url":"https://www.worldtaekwondo.org/att_file/documents/Poomsae%20Competition%20Rules%20and%20Interpretation%20(In%20force%20as%20of%20September%2030%202024).pdf"}]
def autopos(layout):
    P={}
    for row,y in (("r1",8),("r3",30),("r5",52)):
        ids=[i for x in layout[row] for i in (x if isinstance(x,list) else [x])]
        n=len(ids)
        for k,i in enumerate(ids): P[i]=[round(8+k*(84/(n-1 if n>1 else 1))),y]
    for row,y in (("c2",19),("c4",41)):
        for i in layout[row]: P[i]=[50,y]
    return P
def form(n,title,ko,tri,meaning,lines,note,movements,layout,moves,board,vid,size,footex):
    return {"slug":f"taegeuk/{n}","pdf":f"taegeuk-{n}-print.pdf","title":title,"ko":ko,
     "trigram":{"name":tri[0],"ko":tri[1],"sym":tri[2],"meaning":meaning,"lines":lines},"movements":movements,
     "note":{"h":f"{tri[0]} · {tri[1]} · {meaning}","p":note},
     "footer":f"Move counting follows the Kukkiwon step numbers; a kick and the techniques that follow it in the same step share one number ({footex}). Finish with <b>Baro</b>: turn to face ga and return to the ready stance at the starting point.",
     "boardMin":size[0],"cardW":size[1],"figH":size[2],"layout":layout,"pos":autopos(layout),"moves":moves,"refs":refs(n,board,vid)}

# ======================= Taegeuk 5 (Oh Jang) =======================
def kbi(n,dir,view,leg,face=None):   # kick, back-fist, inside block (5: steps 6 and 7)
    o="L" if leg=="R" else "R"
    return [kick(f"{n}-1",dir,view,leg,face),
            mv(f"{n}-2",dir,view,"front",leg,{leg:"backfist"},"backfist",leg,f"Land forward in a {w(leg)} front stance. {W(leg)} back-fist strike.",face=face),
            mv(f"{n}-3",dir,view,"front",leg,{o:"inside"},"inside",o,f"{W(o)} inside middle block.",face=face)]
M5=[J,
 mv("1","da1","side","front","L",{"L":"low"},"low","L","Turn 90° left toward da¹, left front stance. Left low block.",face="R"),
 mv("2","da1","side","walk","L",{"L":"hammer"},"hammer","L","Draw the left foot back into a short stance (oen seogi). Left hammer-fist strike.",face="R"),
 mv("3","ra1","side","front","R",{"R":"low"},"low","R","Turn 180° to the right toward ra¹, right front stance. Right low block.",face="L"),
 mv("4","ra1","side","walk","R",{"R":"hammer"},"hammer","R","Draw the right foot back into a short stance (oreun seogi). Right hammer-fist strike.",face="L"),
 mv("5-1","ga","front","front","L",{"L":"inside"},"inside","L","Turn 90° left toward ga, left front stance. Left inside middle block."),
 mv("5-2","ga","front","front","L",{"R":"inside"},"inside","R","Right inside middle block."),
 *kbi(6,"ga","front","R"), *kbi(7,"ga","front","L"),
 mv("8","ga","front","front","R",{"R":"backfist"},"backfist","R","Step forward into a right front stance. Right back-fist strike."),
 mv("9","ra3","side","back","L",{"L":"ksout"},"ksout","L","Turn 270° to the left toward ra³, back stance with the left foot forward. Left knife-hand outer block.",face="L"),
 mv("10","ra3","side","front","R",{"R":"elbow","L":"eltarget"},"elbow","R","Step forward into a right front stance. Right elbow strike into the left palm.",face="L"),
 mv("11","da3","side","back","R",{"R":"ksout"},"ksout","R","Turn 180° to the right toward da³, back stance with the right foot forward. Right knife-hand outer block.",face="R"),
 mv("12","da3","side","front","L",{"L":"elbow","R":"eltarget"},"elbow","L","Step forward into a left front stance. Left elbow strike into the right palm.",face="R"),
 mv("13-1","na","back","front","L",{"L":"low"},"low","L","Turn 90° left toward na, left front stance. Left low block."),
 mv("13-2","na","back","front","L",{"R":"inside"},"inside","R","Right inside middle block."),
 kick("14-1","na","back","R"),
 mv("14-2","na","back","front","R",{"R":"low"},"low","R","Land forward in a right front stance. Right low block."),
 mv("14-3","na","back","front","R",{"L":"inside"},"inside","L","Left inside middle block."),
 mv("15","ra2","side","front","L",{"L":"high"},"high","L","Turn 90° left toward ra², left front stance. Left high block.",face="L"),
 mv("16-1","ra2","side","skick","R",{"R":"sidepunch"},"skick","R","Right side kick, right arm extended toward the target.",face="L",foot=True),
 mv("16-2","ra2","side","front","R",{"L":"elbow","R":"eltarget"},"eltarget","L","Land in a right front stance. Left elbow strike into the right palm.",face="L"),
 mv("17","da2","side","front","R",{"R":"high"},"high","R","Turn 180° to the right toward da², right front stance. Right high block.",face="R"),
 mv("18-1","da2","side","skick","L",{"L":"sidepunch"},"skick","L","Left side kick, left arm extended toward the target.",face="R",foot=True),
 mv("18-2","da2","side","front","L",{"R":"elbow","L":"eltarget"},"eltarget","R","Land in a left front stance. Right elbow strike into the left palm.",face="R"),
 mv("19-1","na","back","front","L",{"L":"low"},"low","L","Turn 90° left toward na, left front stance. Left low block."),
 mv("19-2","na","back","front","L",{"R":"inside"},"inside","R","Right inside middle block."),
 kick("20-1","na","back","R"),
 mv("20-2","na","back","cross","R",{"R":"backfist"},"backfist","R","Jump forward into a cross stance, left foot tucked behind the right. Right back-fist strike with a kihap.",kihap=True),
]
L5={"r1":["4","3","J","1","2"],"c2":["5-1","5-2","19-1","19-2","20-1","20-2"],
 "r3":[["16-2","16-1"],"15",["6-1","6-2","6-3"],"17",["18-1","18-2"]],"c4":["7-1","7-2","7-3","14-1","14-2","14-3"],
 "r5":["10","9",["8","13-1","13-2"],"11","12"]}
F5=form(5,"Taegeuk Oh Jang","태극 5장",("Seon","손","☴"),"Wind",[1,1,0],
 "Seon is the wind: gentle as a breeze, fierce as a storm, and able to reach everywhere. The form adds the hammer-fist, elbow strikes, the side kick and a jumping finish into a cross stance.",
 20,L5,M5,1352,"4afL-NT521s",(1340,100,120),"6-1, 6-2, 6-3")

# ======================= Taegeuk 6 (Yuk Jang) =======================
M6=[J,
 mv("1","da1","side","front","L",{"L":"low"},"low","L","Turn 90° left toward da¹, left front stance. Left low block.",face="R"),
 kick("2-1","da1","side","R",face="R"),
 mv("2-2","da1","side","back","L",{"L":"outer"},"outer","L","Bring the right foot back where it started: back stance with the left foot forward. Left outer middle block.",face="R"),
 mv("3","ra1","side","front","R",{"R":"low"},"low","R","Turn 180° to the right toward ra¹, right front stance. Right low block.",face="L"),
 kick("4-1","ra1","side","L",face="L"),
 mv("4-2","ra1","side","back","R",{"R":"outer"},"outer","R","Bring the left foot back: back stance with the right foot forward. Right outer middle block.",face="L"),
 mv("5","ga","front","front","L",{"R":"twist"},"twist","R","Turn 90° left toward ga, left front stance. Right twisted knife-hand high block."),
 mv("6-1","ga","side","rkick","R",G,"rkick","R","Right roundhouse kick at face height.",face="R",foot=True),
 mv("6-2","da2","side","front","L",{"L":"houter"},"houter","L","Land, then turn 90° left toward da², left front stance. Left high outer block.",face="R"),
 mv("6-3","da2","side","front","L",{"R":"punch"},"punch","R","Right middle punch.",face="R",note="baro"),
 kick("7-1","da2","side","R",face="R"),
 mv("7-2","da2","side","front","R",{"L":"punch"},"punch","L","Land forward in a right front stance. Left middle punch.",face="R",note="baro"),
 mv("8-1","ra2","side","front","R",{"R":"houter"},"houter","R","Turn 180° to the right toward ra², right front stance. Right high outer block.",face="L"),
 mv("8-2","ra2","side","front","R",{"L":"punch"},"punch","L","Left middle punch.",face="L",note="baro"),
 kick("9-1","ra2","side","L",face="L"),
 mv("9-2","ra2","side","front","L",{"R":"punch"},"punch","R","Land forward in a left front stance. Right middle punch.",face="L",note="baro"),
 mv("10","ga","front","ready",None,{"L":"spread","R":"spread"},"spread",None,"Turn 90° left toward ga into a parallel stance. Low spread block, performed slowly."),
 mv("11","ga","front","front","R",{"L":"twist"},"twist","L","Step forward into a right front stance. Left twisted knife-hand high block."),
 mv("12-1","ga","side","rkick","L",G,"rkick","L","Left roundhouse kick at face height, with a kihap.",face="L",foot=True,kihap=True),
 mv("12-2","da3","side","front","R",{"R":"low"},"low","R","Land, then turn toward da³ into a right front stance. Right low block.",face="R"),
 kick("13-1","da3","side","L",face="R"),
 mv("13-2","da3","side","back","R",{"L":"outer"},"outer","L","Bring the left foot back: back stance with the right foot forward. Left outer middle block.",face="R"),
 mv("14","ra3","side","front","L",{"L":"low"},"low","L","Turn 180° to the left toward ra³, left front stance. Left low block.",face="L"),
 kick("15-1","ra3","side","R",face="L"),
 mv("15-2","ra3","side","back","L",{"R":"outer"},"outer","R","Bring the right foot back: back stance with the left foot forward. Right outer middle block.",face="L"),
 mv("16","ga","front","back","L",{"L":"ksblock","R":"ksguard"},"ksblock","L","Turn 90° left toward ga, back stance with the left foot forward. Double knife-hand block."),
 mv("17","ga","front","back","R",{"R":"ksblock","L":"ksguard"},"ksblock","R","Step back with the left foot: back stance with the right foot forward. Double knife-hand block."),
 mv("18-1","ga","front","front","L",{"L":"palm"},"palm","L","Step back with the right foot into a left front stance. Left palm inside block."),
 mv("18-2","ga","front","front","L",{"R":"punch"},"punch","R","Right middle punch.",note="baro"),
 mv("19-1","ga","front","front","R",{"R":"palm"},"palm","R","Step back with the left foot into a right front stance. Right palm inside block."),
 mv("19-2","ga","front","front","R",{"L":"punch"},"punch","L","Left middle punch.",note="baro"),
]
L6={"r1":[["4-2","4-1"],"3","J","1",["2-1","2-2"]],"c2":["5","6-1","19-1","19-2"],
 "r3":[["9-2","9-1"],["8-1","8-2"],["10","18-1","18-2"],["6-2","6-3"],["7-1","7-2"]],"c4":["11","12-1","17"],
 "r5":[["15-2","15-1"],"14","16","12-2",["13-1","13-2"]]}
F6=form(6,"Taegeuk Yuk Jang","태극 6장",("Gam","감","☵"),"Water",[0,1,0],
 "Gam is water: it keeps flowing and finds its way past every obstacle. The form adds the roundhouse kick, high outer block, twisted knife-hand block, low spread block and palm block, and finishes by stepping backwards.",
 19,L6,M6,1353,"oPtUzvCsz3g",(1360,100,120),"2-1, 2-2")

# ======================= Taegeuk 7 (Chil Jang) =======================
M7=[J,
 mv("1","da1","side","tiger","L",{"R":"palm"},"palm","R","Turn 90° left toward da¹, left tiger stance. Right palm inside block.",face="R"),
 kick("2-1","da1","side","R",face="R"),
 mv("2-2","da1","side","tiger","L",{"L":"inside"},"inside","L","Bring the right foot back: left tiger stance. Left inside middle block.",face="R"),
 mv("3","ra1","side","tiger","R",{"L":"palm"},"palm","L","Turn 180° to the right toward ra¹, right tiger stance. Left palm inside block.",face="L"),
 kick("4-1","ra1","side","L",face="L"),
 mv("4-2","ra1","side","tiger","R",{"R":"inside"},"inside","R","Bring the left foot back: right tiger stance. Right inside middle block.",face="L"),
 mv("5","ga","front","back","L",{"L":"kslow","R":"ksguard"},"kslow","L","Turn 90° left toward ga, back stance with the left foot forward. Low knife-hand guarding block."),
 mv("6","ga","front","back","R",{"R":"kslow","L":"ksguard"},"kslow","R","Step forward: back stance with the right foot forward. Low knife-hand guarding block."),
 mv("7","da2","side","tiger","L",{"R":"palm","L":"assist"},"apalm","R","Turn 90° left toward da², left tiger stance. Right palm inside block, left fist under the right elbow.",face="R"),
 mv("8","da2","side","tiger","L",{"R":"backfist"},"backfist","R","Feet in place. Right back-fist strike.",face="R"),
 mv("9","ra2","side","tiger","R",{"L":"palm","R":"assist"},"apalm","L","Turn 180° to the right toward ra², right tiger stance. Left palm inside block, right fist under the left elbow.",face="L"),
 mv("10","ra2","side","tiger","R",{"L":"backfist"},"backfist","L","Feet in place. Left back-fist strike.",face="L"),
 mv("11","ga","front","close",None,{"L":"cover","R":"cover"},"cover",None,"Turn 90° left toward ga, feet together. Covered fist: the right fist wrapped in the left hand, raised slowly in front of the chest."),
 mv("12-1","ga","front","front","L",{"L":"outer","R":"low"},"scissors",None,"Step forward into a left front stance. Scissors block: left outer middle block, right low block."),
 mv("12-2","ga","front","front","L",{"R":"outer","L":"low"},"scissors",None,"Scissors block reversed: right outer middle block, left low block."),
 mv("13-1","ga","front","front","R",{"R":"outer","L":"low"},"scissors",None,"Step forward into a right front stance. Scissors block: right outer middle block, left low block."),
 mv("13-2","ga","front","front","R",{"L":"outer","R":"low"},"scissors",None,"Scissors block reversed: left outer middle block, right low block."),
 mv("14","ra3","side","front","L",{"L":"wedge","R":"wedge"},"wedge",None,"Turn 270° to the left toward ra³, left front stance. Middle wedge block.",face="L"),
 mv("15-1","ra3","side","knee","R",{"L":"grab","R":"grab"},"knee","R","Pull down with both hands and drive the right knee up.",face="L",foot=True),
 mv("15-2","ra3","side","cross","R",{"L":"uppercut","R":"uppercut"},"duppercut",None,"Jump forward into a cross stance, left foot tucked behind the right. Double uppercut.",face="L"),
 mv("16","ra3","side","front","R",{"L":"xlow","R":"xlow"},"xlow",None,"Step back with the left foot into a right front stance. Low X block.",face="L"),
 mv("17","da3","side","front","R",{"L":"wedge","R":"wedge"},"wedge",None,"Turn 180° to the right toward da³, right front stance. Middle wedge block.",face="R"),
 mv("18-1","da3","side","knee","L",{"L":"grab","R":"grab"},"knee","L","Pull down with both hands and drive the left knee up.",face="R",foot=True),
 mv("18-2","da3","side","cross","L",{"L":"uppercut","R":"uppercut"},"duppercut",None,"Jump forward into a cross stance, right foot tucked behind the left. Double uppercut.",face="R"),
 mv("19","da3","side","front","L",{"L":"xlow","R":"xlow"},"xlow",None,"Step back with the right foot into a left front stance. Low X block.",face="R"),
 mv("20","na","back","walk","L",{"L":"backfist"},"obackfist","L","Turn 90° left toward na, left walking stance. Left outward back-fist strike."),
 mv("21-1","na","back","kick","R",{"L":"eltarget"},"tkick","R","Right target kick into the left palm.",foot=True),
 mv("21-2","na","back","horse",None,{"R":"elbow","L":"eltarget"},"eltarget","R","Land in a horse stance. Right elbow strike into the left palm."),
 mv("22","na","back","walk","R",{"R":"backfist"},"obackfist","R","Step into a right walking stance. Right outward back-fist strike."),
 mv("23-1","na","back","kick","L",{"R":"eltarget"},"tkick","L","Left target kick into the right palm.",foot=True),
 mv("23-2","na","back","horse",None,{"L":"elbow","R":"eltarget"},"eltarget","L","Land in a horse stance. Left elbow strike into the right palm."),
 mv("24","na","back","horse",None,{"L":"ksside"},"ksside","L","Feet in place. Left knife-hand side block."),
 mv("25","na","back","horse",None,{"R":"sidepunch"},"sidepunch","R","Step the right foot forward into a horse stance. Right side punch with a kihap.",kihap=True),
]
L7={"r1":[["4-2","4-1"],"3",["J","24","25"],"1",["2-1","2-2"]],"c2":["5","23-1","23-2"],
 "r3":["10","9",["6","11","22"],"7","8"],"c4":["12-1","12-2","21-1","21-2"],
 "r5":[["16","15-2","15-1"],"14",["13-1","13-2","20"],"17",["18-1","18-2","19"]]}
F7=form(7,"Taegeuk Chil Jang","태극 7장",("Gan","간","☶"),"Mountain",[1,0,0],
 "Gan is the mountain: steady, unmoving, and moving only when the moment is right. The form brings in the tiger stance, palm blocks, scissors and wedge blocks, knee strikes and the horse stance.",
 25,L7,M7,1354,None,(1360,100,120),"2-1, 2-2")

# ======================= Taegeuk 8 (Pal Jang) =======================
def bep(n,dir,view,face,leg):   # back-stance knife block / elbow / back-fist / punch (8: 20-27)
    o="L" if leg=="R" else "R"
    return [mv(f"{n}",dir,view,"back",leg,{leg:"ksout"},"ksout",leg,"",face=face)]
M8=[J,
 mv("1","ga","front","back","L",{"L":"outer","R":"assist"},"aouter","L","Step forward with the left foot toward ga, back stance with the left foot forward. Augmented outer middle block."),
 mv("2","ga","front","front","L",{"R":"punch"},"punch","R","Slide forward into a left front stance. Right middle punch.",note="baro"),
 kick("3-1","ga","front","R",desc="Right front kick, springing into the jump."),
 mv("3-2","ga","front","kick","L",G,"jkick","L","Jumping left front kick, higher, with a kihap.",foot=True,kihap=True),
 mv("3-3","ga","front","front","L",{"L":"inside"},"inside","L","Land in a left front stance. Left inside middle block."),
 mv("3-4","ga","front","front","L",{"R":"punch"},"punch","R","Right middle punch, the first of a double punch.",note="baro"),
 mv("3-5","ga","front","front","L",{"L":"punch"},"punch","L","Left middle punch, completing the double punch.",note="bandae"),
 mv("4","ga","front","front","R",{"R":"punch"},"punch","R","Step forward into a right front stance. Right middle punch.",note="bandae"),
 mv("5","ra3","side","front","R",{"R":"houter","L":"low"},"mountain",None,"Turn 270° to the left; right front stance facing ra³. Single mountain block: right arm high, left arm low.",face="L"),
 mv("6","da3","side","front","L",{"R":"uppercut","L":"grab"},"uppercut","R","Pivot in place to face da³, left front stance. Slow pulling uppercut with the right fist while the left hand pulls.",face="R"),
 mv("7","da3","side","front","L",{"L":"houter","R":"low"},"mountain",None,"Cross the left foot in front of the right and step out; left front stance facing da³. Single mountain block: left arm high, right arm low.",face="R"),
 mv("8","ra3","side","front","R",{"L":"uppercut","R":"grab"},"uppercut","L","Pivot in place to face ra³, right front stance. Slow pulling uppercut with the left fist while the right hand pulls.",face="L"),
 mv("9","ga","front","back","L",{"L":"ksblock","R":"ksguard"},"ksblock","L","Turn 90° left toward ga, back stance with the left foot forward. Double knife-hand block."),
 mv("10","ga","front","front","L",{"R":"punch"},"punch","R","Slide forward into a left front stance. Right middle punch.",note="baro"),
 kick("11-1","ga","front","R"),
 mv("11-2","ga","front","tiger","R",{"R":"palm"},"palm","R","Bring the kicking foot back and draw the left foot back: right tiger stance. Right palm inside block."),
 mv("12","da2","side","tiger","L",{"L":"ksblock","R":"ksguard"},"ksblock","L","Turn 90° left toward da², left tiger stance. Double knife-hand block.",face="R"),
 kick("13-1","da2","side","L",face="R"),
 mv("13-2","da2","side","front","L",{"R":"punch"},"punch","R","Land forward in a left front stance. Right middle punch.",face="R",note="baro"),
 mv("14","da2","side","tiger","L",{"L":"palm"},"palm","L","Slide the left foot back into a left tiger stance. Left palm inside block.",face="R"),
 mv("15","ra2","side","tiger","R",{"R":"ksblock","L":"ksguard"},"ksblock","R","Turn 180° to the right toward ra², right tiger stance. Double knife-hand block.",face="L"),
 kick("16-1","ra2","side","R",face="L"),
 mv("16-2","ra2","side","front","R",{"L":"punch"},"punch","L","Land forward in a right front stance. Left middle punch.",face="L",note="baro"),
 mv("17","ra2","side","tiger","R",{"R":"palm"},"palm","R","Slide the right foot back into a right tiger stance. Right palm inside block.",face="L"),
 mv("18","na","back","back","R",{"R":"low","L":"assist"},"alow","R","Turn 90° toward na, back stance with the right foot forward. Augmented low block."),
 kick("19-1","na","back","L",desc="Left front kick, springing into the jump."),
 mv("19-2","na","back","kick","R",G,"jkick","R","Jumping right front kick, with a kihap.",foot=True,kihap=True),
 mv("19-3","na","back","front","R",{"R":"inside"},"inside","R","Land in a right front stance. Right inside middle block."),
 mv("19-4","na","back","front","R",{"L":"punch"},"punch","L","Left middle punch, the first of a double punch.",note="baro"),
 mv("19-5","na","back","front","R",{"R":"punch"},"punch","R","Right middle punch, completing the double punch.",note="bandae"),
 mv("20","da1","side","back","L",{"L":"ksout"},"ksout","L","Turn 270° to the left toward da¹, back stance with the left foot forward. Knife-hand outer block.",face="R"),
 mv("21","da1","side","front","L",{"R":"elbow"},"elbow","R","Slide forward into a left front stance. Right elbow strike.",face="R"),
 mv("22","da1","side","front","L",{"R":"backfist"},"backfist","R","Feet in place. Right back-fist strike.",face="R"),
 mv("23","da1","side","front","L",{"L":"punch"},"punch","L","Feet in place. Left middle punch.",face="R",note="bandae"),
 mv("24","ra1","side","back","R",{"R":"ksout"},"ksout","R","Pivot 180° to the right toward ra¹, back stance with the right foot forward. Knife-hand outer block.",face="L"),
 mv("25","ra1","side","front","R",{"L":"elbow"},"elbow","L","Slide forward into a right front stance. Left elbow strike.",face="L"),
 mv("26","ra1","side","front","R",{"L":"backfist"},"backfist","L","Feet in place. Left back-fist strike.",face="L"),
 mv("27","ra1","side","front","R",{"R":"punch"},"punch","R","Feet in place. Right middle punch.",face="L",note="bandae"),
]
L8={"r1":[["27","26","25","24"],"J",["20","21","22","23"]],"c2":["1","2","18","19-1","19-2","19-3","19-4","19-5"],
 "r3":[["17","16-2","16-1","15"],["12","13-1","13-2","14"]],"c4":["3-1","3-2","3-3","3-4","3-5","4"],
 "r5":[["8","5"],["9","10","11-1","11-2"],["6","7"]]}
F8=form(8,"Taegeuk Pal Jang","태극 8장",("Gon","곤","☷"),"Earth",[0,0,0],
 "Gon is the earth: the root of all things, where life begins and returns. The last Taegeuk gathers the whole set, adding the jumping double kick, mountain block and pulling uppercut before the black-belt forms.",
 24,L8,M8,1355,None,(1360,98,118),"3-1 to 3-5")

VID={5:None,6:"x",7:None,8:None}
for n,F in ((5,F5),(6,F6),(7,F7),(8,F8)):
    json.dump(F,open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"forms",f"taegeuk-{n}.json"),"w"),ensure_ascii=False,indent=1)
    print(n,len(F["moves"]),"figures")
