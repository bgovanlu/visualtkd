"""Authoring script used to write forms/koryo.json, keumgang.json, taebaek.json (kept for reference).

The JSON files are the source of truth; re-running this OVERWRITES them.
Shows how a non-王 floor (士 山 工) is described with `floor`.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = {"L": "guard", "R": "guard"}
W = lambda s: "Right" if s == "R" else "Left"
w = lambda s: "right" if s == "R" else "left"
O = lambda s: "L" if s == "R" else "R"

def mv(id, dir, view, stance, lead, arms, tech, hand, desc, face=None, **kw):
    d = {"id": id, "dir": dir, "view": view, "stance": stance}
    if face: d["face"] = face
    if lead: d["lead"] = lead
    d.update({"arms": arms, "tech": tech})
    if hand: d["hand"] = hand
    d.update(kw); d["desc"] = desc
    return d

def kick(id, dir, view, leg, face=None, desc=None, **kw):
    return mv(id, dir, view, "kick", leg, G, "kick", leg, desc or f"{W(leg)} front kick.", face=face, foot=True, **kw)

JUNBI = mv("J", "na", "front", "ready", None, {"L": "junbi", "R": "junbi"}, "junbi", None,
           "Stand at na facing ga, feet parallel and one foot-width apart, fists in front of the belt (gibon junbi).")

def refs(slug, name, board, vid):
    video = ({"go": f"video-{slug}", "kind": "yt", "icon": "play", "src": "YouTube · Video", "title": f"{name}, full performance",
              "desc": "Kukkiwon Digital Encyclopedia, published by Mookas TV.", "url": f"https://www.youtube.com/watch?v={vid}"} if vid else
             {"go": f"video-{slug}", "kind": "yt", "icon": "channel", "src": "YouTube · Playlist", "title": "Kukkiwon Digital Encyclopedia series",
              "desc": f"Mookas TV playlist of the full series, including {name}.", "url": "https://www.youtube.com/playlist?list=PL4lzP9nwMEv2A-vF-GaNNn2OdjXjZfA6k"})
    return [
        {"go": f"kukkiwon-{slug}", "kind": "kuk", "icon": "gate", "src": "Kukkiwon · Official site", "title": name,
         "desc": "The form’s official description and meaning.",
         "url": f"https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo={board}&page=1&menuLevel=3&menuNo=72"},
        {"go": "kukkiwon-poomsae", "kind": "kuk", "icon": "gate", "src": "Kukkiwon · Official site", "title": "Poomsae index",
         "desc": "Every official poomsae, Taegeuk 1–8 and the black-belt forms.",
         "url": "https://www.kukkiwon.or.kr/eng/board/list?boardManagementNo=55&menuLevel=3&menuNo=72"},
        video,
        {"go": "kukkiwon-youtube", "kind": "yt", "icon": "channel", "src": "YouTube · Channel", "title": "Kukkiwon World Taekwondo Headquarters",
         "desc": "The official Kukkiwon channel.", "url": "https://www.youtube.com/channel/UCaQb3jutLu15oSfhPh8FACQ"},
        {"go": "wt-poomsae-rules", "kind": "wt", "icon": "pdf", "src": "World Taekwondo · PDF", "title": "Poomsae Competition Rules and Interpretation",
         "desc": "In force from 30 September 2024; how poomsae are judged.",
         "url": "https://www.worldtaekwondo.org/att_file/documents/Poomsae%20Competition%20Rules%20and%20Interpretation%20(In%20force%20as%20of%20September%2030%202024).pdf"},
    ]

COUNT = ("Move numbers follow the Kukkiwon movement count ({n} movements); a kick and the techniques that follow it in the same "
         "movement share one number ({ex}). ")

def form(slug, title, ko, hanja, meaning, note_h, note_p, movements, floor, layout, pos, moves, board, vid, size, ex, finish):
    F = {"slug": slug, "pdf": f"{slug}-print.pdf", "title": title, "ko": ko,
         "symbol": {"name": title, "hanja": hanja, "meaning": meaning}, "movements": movements,
         "note": {"h": note_h, "p": note_p},
         "footer": COUNT.format(n=movements, ex=ex) + finish,
         "boardMin": size[0], "cardW": size[1], "figH": size[2], "floor": floor,
         "layout": layout, "pos": pos, "moves": moves, "refs": refs(slug, title, board, vid)}
    json.dump(F, open(os.path.join(ROOT, "forms", f"{slug}.json"), "w"), ensure_ascii=False, indent=1)
    print(slug, len(moves), "figures")

# ============================ KORYO 고려 ============================
def koryo_side(n, d, face, lead):
    """1–4 and 5–8: double knife-hand block, double side kick, knife-hand strike, punch, inside block."""
    o = O(lead); rest = O(lead)          # the kicking leg is the rear leg
    k = o
    turn = "Turn 90° left toward da¹" if face == "R" else "Turn 180° right toward ra¹"
    return [
        mv(f"{n}", d, "side", "back", lead, {lead: "ksblock", o: "ksguard"}, "ksblock", lead,
           f"{turn}, back stance with the {w(lead)} foot forward. Double knife-hand middle block.", face=face),
        mv(f"{n+1}-1", d, "side", "skick", k, G, "dskick", k,
           f"{W(k)} double side kick: low to the knee, then high, without setting the foot down.", face=face, foot=True),
        mv(f"{n+1}-2", d, "side", "front", k, {k: "ksstrike"}, "ksstrike", k,
           f"Land forward in a {w(k)} front stance. {W(k)} knife-hand outer strike to the neck.", face=face),
        mv(f"{n+2}", d, "side", "front", k, {O(k): "punch"}, "punch", O(k), f"{W(O(k))} middle punch.", face=face, note="baro"),
        mv(f"{n+3}", d, "side", "back", k, {k: "inside"}, "inside", k,
           f"Shift the weight back into a back stance with the {w(k)} foot forward. {W(k)} inside middle block.", face=face),
    ]

def koryo_fwd(n, lead, view, d, kihap=False, first=False):
    o = O(lead)
    out = [] if first else [kick(f"{n}-1", d, view, lead)]
    a = f"{n}-1" if first else f"{n}-2"; b = f"{n}-2" if first else f"{n}-3"
    step = "Turn 90° left toward ga, left front stance." if first else f"Land forward in a {w(lead)} front stance."
    out += [mv(a, d, view, "front", lead, {lead: "kslow"}, "kslow", lead, f"{step} {W(lead)} knife-hand low block."),
            mv(b, d, view, "front", lead, {o: "arc"}, "arc", o, f"{W(o)} arc-hand strike to the throat (kaljaebi).",
               **({"kihap": True} if kihap else {}))]
    return out

def koryo_horse(n, side):
    """16–20 (side = L, toward da) and 21–25 (side = R, toward ra): side block, target punch, kick, low spear, low block, press, elbow."""
    o = O(side)
    out_d, back_d = ("da2", "ra2") if side == "L" else ("ra2", "da2")
    out_f, back_f = ("R", "L") if side == "L" else ("L", "R")
    toward = "da" if side == "L" else "ra"
    first = (f"Turn toward ga, stepping the right foot out into a horse stance. Left knife-hand side block toward da." if side == "L"
             else "Right knife-hand side block toward ra.")
    return [
        mv(f"{n}", "ga", "front", "horse", None, {side: "ksside"}, "ksside", side, first),
        mv(f"{n+1}", "ga", "front", "horse", None, {side: "target", o: "crosspunch"}, "tpunch", o,
           f"{W(o)} target punch across into the open {w(side)} hand."),
        mv(f"{n+2}-1", out_d, "side", "skick", side, G, "skick", side,
           f"Cross the {w(o)} foot in front of the {w(side)} (ap kkoa seogi), then {w(side)} side kick toward {toward}.", face=out_f, foot=True),
        mv(f"{n+2}-2", back_d, "side", "front", o, {side: "lspear", o: "shoulder"}, "lspear", side,
           f"Set the {w(side)} foot down and turn back to face {'ra' if side == 'L' else 'da'}, {w(o)} front stance. "
           f"{W(side)} low spear hand, palm up; the {w(o)} fist pulls to the {w(side)} shoulder.", face=back_f),
        mv(f"{n+3}", back_d, "side", "walk", o, {o: "low"}, "low", o,
           f"Draw the {w(o)} foot back into a {w(o)} walking stance. {W(o)} low block.", face=back_f),
        mv(f"{n+4}-1", back_d, "side", "walk", side, {side: "pressdown"}, "pressdown", side,
           f"Step forward into a {w(side)} walking stance. {W(side)} palm pressing block.", face=back_f),
        mv(f"{n+4}-2", "ga", "front", "horse", None, {o: "sideelbow", side: "pressdown" if False else "elbowpush"}, "sideelbow", o,
           f"Step the {w(o)} foot forward and turn into a horse stance facing ga. {W(o)} side elbow strike toward "
           f"{'ra' if side == 'L' else 'da'}, the {w(side)} palm pushing the {w(o)} fist."),
    ]

K = [mv("J", "na", "front", "ready", None, {"L": "tongmil", "R": "tongmil"}, "tongmil", None,
        "Stand at na facing ga. Raise both open hands slowly from the belt to the chest, then push them forward to face height, "
        "fingertips angled toward each other (tongmilgi junbi).")]
K += koryo_side(1, "da1", "R", "L")
K += koryo_side(5, "ra1", "L", "R")
K += koryo_fwd(9, "L", "front", "ga", first=True)
K += koryo_fwd(10, "R", "front", "ga")
K += koryo_fwd(11, "L", "front", "ga", kihap=True)
K += [kick("12-1", "ga", "front", "R"),
      mv("12-2", "ga", "front", "front", "R", {"L": "kneebreak", "R": "hold"}, "kneebreak", "L",
         "Land in a right front stance. Knee break: the right hand holds the kicked foot at the waist while the left arc hand presses the knee down."),
      mv("13", "na", "back", "front", "R", {"L": "wedge", "R": "wedge"}, "wedge", None,
         "Turn 180° toward na into a right front stance. Inner-forearm opening block (an palmok momtong hecho makki)."),
      kick("14-1", "na", "back", "L"),
      mv("14-2", "na", "back", "front", "L", {"R": "kneebreak", "L": "hold"}, "kneebreak", "R",
         "Land in a left front stance. Knee break: the left hand holds the foot, the right arc hand presses the knee down."),
      mv("15", "na", "back", "walk", "L", {"L": "wedge", "R": "wedge"}, "wedge", None,
         "Draw the left foot back into a left walking stance. Inner-forearm opening block.")]
K += koryo_horse(16, "L")
K += koryo_horse(21, "R")
K += [mv("26", "ga", "front", "close", None, {"L": "hammerlow", "R": "palmlow"}, "hammerlow", "L",
         "Draw the right foot to the left into a closed stance facing ga. Raise both hands overhead, circle them out and down slowly, "
         "and strike the left hammer fist into the right palm in front of the belly."),
      mv("27-1", "na", "back", "front", "L", {"L": "ksstrike"}, "ksstrike", "L", "Turn 180° left toward na, left front stance. Left knife-hand outer strike."),
      mv("27-2", "na", "back", "front", "L", {"L": "kslow"}, "kslow", "L", "Left knife-hand low block."),
      mv("28-1", "na", "back", "front", "R", {"R": "neck"}, "neck", "R", "Step forward into a right front stance. Right knife-hand inward strike to the neck."),
      mv("28-2", "na", "back", "front", "R", {"R": "kslow"}, "kslow", "R", "Right knife-hand low block."),
      mv("29-1", "na", "back", "walk", "L", {"L": "neck"}, "neck", "L", "Step forward into a left walking stance. Left knife-hand inward strike to the neck."),
      mv("29-2", "na", "back", "walk", "L", {"L": "kslow"}, "kslow", "L", "Left knife-hand low block."),
      mv("30", "na", "back", "walk", "R", {"R": "arc"}, "arc", "R", "Step forward into a right walking stance. Right arc-hand strike to the throat (kaljaebi).", kihap=True)]

KL = {"r1": [["8", "7", "6-2", "6-1"], ["5"], "J", ["1"], ["2-1", "2-2", "3", "4"]],
      "c2": ["9-1", "9-2", "10-1", "10-2", "10-3", "27-1", "27-2", "28-1", "28-2", "29-1", "29-2", "30"],
      "r3": [["24", "23-2", "23-1"], ["25-2", "25-1"], ["22", "21"], "26", ["16", "17"], ["20-1", "20-2"], ["18-1", "18-2", "19"]],
      "c4": ["11-1", "11-2", "11-3", "12-1", "12-2", "13", "14-1", "14-2", "15"]}
KP = {"J": [50, 8], "1": [56, 8], "2-1": [62, 8], "2-2": [66, 8], "3": [66, 8], "4": [66, 8],
      "5": [44, 8], "6-1": [38, 8], "6-2": [34, 8], "7": [34, 8], "8": [34, 8],
      "9-1": [50, 17], "9-2": [50, 17], "10-1": [50, 23], "10-2": [50, 27], "10-3": [50, 27],
      "11-1": [50, 33], "11-2": [50, 39], "11-3": [50, 39], "12-1": [50, 45], "12-2": [50, 51],
      "13": [50, 51], "14-1": [50, 47], "14-2": [50, 42], "15": [50, 40],
      "16": [56, 36], "17": [56, 36], "18-1": [68, 36], "18-2": [80, 36], "19": [76, 36], "20-1": [70, 36], "20-2": [62, 36],
      "21": [62, 36], "22": [62, 36], "23-1": [44, 36], "23-2": [24, 36], "24": [28, 36], "25-1": [34, 36], "25-2": [42, 36],
      "26": [50, 36], "27-1": [50, 29], "27-2": [50, 29], "28-1": [50, 21], "28-2": [50, 21], "29-1": [50, 15], "29-2": [50, 15], "30": [50, 9]}
form("koryo", "Koryo", "고려", "高麗", "Goryeo · the learned warrior",
     "士 · Seonbi · the learned warrior",
     "Named for the Goryeo dynasty, whose people held off the Mongol invasions. The floor line is 士 (seonbi): "
     "a scholar who carries a warrior’s strength and conviction. It opens from the pushing-hands ready posture.",
     30, {"glyph": "士", "bars": {"r1": "fit", "r5": "gone"}, "rail": ["r1", "c4"], "notesBelow": True,
          "map": "M30 8H70M6 36H94M50 8V52"},
     KL, KP, K, 1356, "keZTTPuXHJo", (1700, 98, 118), "2-1 kick, 2-2 strike",
     "Finish with <b>Baro</b>: draw the left foot back, turn to face ga and return to the pushing-hands ready posture at the starting point.")

# ============================ KEUMGANG 금강 ============================
def hinge(id, travel, desc):
    """Keun doljjeogwi toward travel side: elbow on the travel side, the other fist across the chest."""
    return mv(id, "ga", "front", "horse", None, {travel: "sideelbow", O(travel): "hingepunch"}, "khinge", None, desc)

def crane(id, stand, desc):
    lift = O(stand)
    return mv(id, "ga", "front", "crane", stand, {lift: "low", stand: "high"}, "keumgang", None, desc)

def mtn(id, d, face, desc, **kw):
    return mv(id, d, "side", "horse", None, {"L": "houter", "R": "houter"}, "santeul", None, desc, face=face, **kw)

KG = [JUNBI,
      mv("1", "ga", "front", "front", "L", {"L": "wedge", "R": "wedge"}, "wedge", None,
         "Step forward toward ga into a left front stance. Inner-forearm opening block (an palmok momtong hecho makki)."),
      mv("2", "ga", "front", "front", "R", {"R": "palmjaw"}, "palmjaw", "R", "Step forward into a right front stance. Right palm-heel jaw strike.", note="bandae"),
      mv("3", "ga", "front", "front", "L", {"L": "palmjaw"}, "palmjaw", "L", "Step forward into a left front stance. Left palm-heel jaw strike.", note="bandae"),
      mv("4", "ga", "front", "front", "R", {"R": "palmjaw"}, "palmjaw", "R", "Step forward into a right front stance. Right palm-heel jaw strike.", note="bandae"),
      mv("5", "ga", "front", "back", "L", {"L": "ksin"}, "ksin", "L", "Step back with the right foot into a back stance with the left foot forward. Left knife-hand inside block."),
      mv("6", "ga", "front", "back", "R", {"R": "ksin"}, "ksin", "R", "Step back with the left foot into a back stance with the right foot forward. Right knife-hand inside block."),
      mv("7", "ga", "front", "back", "L", {"L": "ksin"}, "ksin", "L", "Step back with the right foot into a back stance with the left foot forward. Left knife-hand inside block."),
      crane("8", "R", "Lift the left foot to the right knee: crane stance on the right leg, looking left toward da. Diamond block, slowly: left low block, right high block."),
      hinge("9", "L", "Step the left foot down toward da into a horse stance. Large hinge: left elbow out toward da, right fist across the chest."),
      hinge("10", "L", "Turn 360° to the left, travelling toward da, and land in a horse stance. Large hinge again."),
      mtn("11", "da1", "R", "Turn 90° left to face da and stamp into a horse stance. Mountain block.", kihap=True),
      mv("12", "ra1", "side", "horse", None, {"L": "wedge", "R": "wedge"}, "wedge", None,
         "Turn 180° to the right, stepping round to face ra, horse stance. Inner-forearm opening block.", face="L"),
      mv("13", "ra1", "side", "ready", None, {"L": "spread", "R": "spread"}, "spread", None,
         "Draw the left foot in to a parallel stance. Low spread block, slowly.", face="L"),
      mtn("14", "da1", "R", "Turn 180° to the right to face da and stamp into a horse stance. Mountain block."),
      crane("15", "L", "Turn to face ga and lift the right foot to the left knee: crane stance on the left leg, looking right toward ra. Diamond block, slowly."),
      hinge("16", "R", "Step the right foot down toward ra into a horse stance. Large hinge: right elbow out toward ra, left fist across the chest."),
      hinge("17", "R", "Turn 360° to the right, travelling toward ra, and land in a horse stance. Large hinge again."),
      crane("18", "L", "Lift the right foot to the left knee: crane stance on the left leg, looking toward ra. Diamond block, slowly."),
      hinge("19", "R", "Step the right foot down toward ra into a horse stance. Large hinge."),
      hinge("20", "R", "Turn 360° to the right, travelling toward ra, and land in a horse stance. Large hinge again."),
      mtn("21", "ra1", "L", "Turn 90° right to face ra and stamp into a horse stance. Mountain block.", kihap=True),
      mv("22", "da1", "side", "horse", None, {"L": "wedge", "R": "wedge"}, "wedge", None,
         "Turn 180° to the left, stepping round to face da, horse stance. Inner-forearm opening block.", face="R"),
      mv("23", "da1", "side", "ready", None, {"L": "spread", "R": "spread"}, "spread", None,
         "Draw the right foot in to a parallel stance. Low spread block, slowly.", face="R"),
      mtn("24", "ra1", "L", "Turn 180° to the left to face ra and stamp into a horse stance. Mountain block."),
      crane("25", "R", "Turn to face ga and lift the left foot to the right knee: crane stance on the right leg, looking left toward da. Diamond block, slowly."),
      hinge("26", "L", "Step the left foot down toward da into a horse stance. Large hinge."),
      hinge("27", "L", "Turn 360° to the left, travelling toward da, and land in a horse stance. Large hinge again.")]
KGL = {"r1": [["25", "20"], ["26", "19"], ["27"], ["J", "8", "18"], ["17"], ["16", "9"], ["15", "10"]],
       "c2l": ["21", "22", "23", "24"], "c2": ["1", "2", "6", "7"], "c2r": ["11", "12", "13", "14"],
       "c4": ["3", "4", "5"]}
KGP = {"J": [50, 8], "1": [50, 16], "2": [50, 24], "3": [50, 32], "4": [50, 40], "5": [50, 32], "6": [50, 24], "7": [50, 16],
       "8": [50, 8], "9": [62, 8], "10": [76, 8], "11": [88, 11], "12": [88, 21], "13": [88, 23], "14": [88, 15], "15": [88, 8],
       "16": [74, 8], "17": [60, 8], "18": [50, 8], "19": [38, 8], "20": [24, 8], "21": [12, 11], "22": [12, 21], "23": [12, 23],
       "24": [12, 15], "25": [12, 8], "26": [26, 8], "27": [40, 8]}
form("keumgang", "Keumgang", "금강", "金剛", "Diamond · too hard to break",
     "山 · San · the mountain",
     "Keumgang means diamond, the hardest thing there is; the name also recalls Keumgangsan, the Diamond Mountains. "
     "The floor line is 山 (mountain). Move with weight and calm, and hold each crane stance still.",
     27, {"glyph": "山", "bars": {"r3": "gone", "r5": "gone"}, "rail": ["r1", "c4"], "notesBelow": True,
          "prongs": [{"at": "c2l", "from": "r1"}, {"at": "c2r", "from": "r1"}],
          "map": "M4 8H96M12 8V26M88 8V26M50 8V44"},
     KGL, KGP, KG, 1357, None, (1500, 100, 120), "one figure per movement",
     "Finish with <b>Baro</b>: draw the left foot in and return to the ready stance facing ga.")

# ============================ TAEBAEK 태백 ============================
def tb_open(n, d, face, lead, turn):
    o = O(lead)
    return [mv(f"{n}", d, "side", "tiger", lead, {"L": "kspread", "R": "kspread"}, "kspread", None,
               f"{turn}, {w(lead)} tiger stance. Knife-hand low spread block.", face=face),
            kick(f"{n+1}-1", d, "side", o, face=face),
            mv(f"{n+1}-2", d, "side", "front", o, {o: "punch"}, "punch", o, f"Land in a {w(o)} front stance. {W(o)} middle punch.", face=face, note="bandae"),
            mv(f"{n+1}-3", d, "side", "front", o, {lead: "punch"}, "punch", lead, f"{W(lead)} middle punch.", face=face, note="baro")]

def tb_grab(n, hand, kihap=False):
    o = O(hand)
    return [mv(f"{n}-1", "ga", "front", "front", o, {hand: "tgrab"}, "tgrab", hand,
               f"Without stepping, twist the {w(hand)} hand over and grab the opponent’s wrist."),
            mv(f"{n}-2", "ga", "front", "front", hand, {o: "punch"}, "punch", o,
               f"Pull with the {w(hand)} hand as you step forward into a {w(hand)} front stance. {W(o)} middle punch.", note="baro",
               **({"kihap": True} if kihap else {}))]

def tb_side(n, d, face, lead, first):
    """9–13 and 14–18: diamond middle block, pulling uppercut, punch, small hinge on one leg, side kick, elbow."""
    o = O(lead)
    return [mv(f"{n}", d, "side", "back", lead, {lead: "outer", o: "high"}, "kmomtong", None,
               f"{first}, back stance with the {w(lead)} foot forward. Diamond middle block: {w(lead)} middle block, {w(o)} high block.", face=face),
            mv(f"{n+1}", d, "side", "back", lead, {o: "uppercut", lead: "grab"}, "uppercut", o,
               f"{W(o)} pulling uppercut to the jaw; the {w(lead)} hand pulls in.", face=face),
            mv(f"{n+2}", d, "side", "back", lead, {lead: "punch"}, "punch", lead, f"{W(lead)} middle punch.", face=face, note="bandae"),
            mv(f"{n+3}", d, "side", "crane", o, {lead: "hingetop"}, "shinge", None,
               f"Draw the {w(lead)} foot up to the {w(o)} knee: crane stance on the {w(o)} leg. Small hinge: both fists at the {w(o)} hip.", face=face),
            mv(f"{n+4}-1", d, "side", "skick", lead, {lead: "hammerout"}, "hskick", lead,
               f"{W(lead)} side kick with a {w(lead)} hammer-fist outer strike.", face=face, foot=True),
            mv(f"{n+4}-2", d, "side", "front", lead, {o: "elbow", lead: "eltarget"}, "eltarget", o,
               f"Land in a {w(lead)} front stance. {W(o)} elbow strike into the {w(lead)} palm.", face=face)]

TB = [JUNBI]
TB += tb_open(1, "da1", "R", "L", "Turn 90° left toward da¹")
TB += tb_open(3, "ra1", "L", "R", "Turn 180° right on the left foot toward ra¹")
TB[-4]["id"], TB[-3]["id"], TB[-2]["id"], TB[-1]["id"] = "3", "4-1", "4-2", "4-3"
TB += [mv("5", "ga", "front", "front", "L", {"L": "khigh", "R": "neck"}, "jebi", "R",
          "Turn 90° left toward ga, left front stance. Swallow-form knife-hand strike: left knife-hand high block, right knife hand to the neck.")]
TB += tb_grab(6, "R") + tb_grab(7, "L") + tb_grab(8, "R", kihap=True)
TB += tb_side(9, "ra3", "L", "L", "Turn 270° to the left on the right foot to face ra³")
TB += tb_side(14, "da3", "R", "R", "Draw the left foot back to the right, then turn to face da³")
TB += [mv("19", "na", "back", "back", "L", {"L": "ksblock", "R": "ksguard"}, "ksblock", "L",
          "Turn left to face na, back stance with the left foot forward. Double knife-hand block (sonnal geodeureo makki)."),
       mv("20", "na", "back", "front", "R", {"R": "spear", "L": "press"}, "spear", "R",
          "Step forward into a right front stance. Right spear-hand thrust over the left pressing hand."),
       mv("21", "na", "back", "back", "L", {"L": "backfist"}, "obackfist", "L",
          "The opponent holds the right wrist: pull it free, turn round to the left and step the left foot forward into a back stance with the left foot forward. Left back-fist strike to the face."),
       mv("22", "na", "back", "front", "R", {"R": "punch"}, "punch", "R", "Step forward into a right front stance. Right middle punch.", note="bandae", kihap=True),
       mv("23", "ra1", "side", "front", "L", {"R": "outer", "L": "low"}, "scissors", None,
          "Turn 90° left toward ra¹, left front stance. Scissors block.", face="L"),
       kick("24-1", "ra1", "side", "R", face="L"),
       mv("24-2", "ra1", "side", "front", "R", {"R": "punch"}, "punch", "R", "Land in a right front stance. Right middle punch.", face="L", note="bandae"),
       mv("24-3", "ra1", "side", "front", "R", {"L": "punch"}, "punch", "L", "Left middle punch.", face="L", note="baro"),
       mv("25", "da1", "side", "front", "R", {"L": "outer", "R": "low"}, "scissors", None,
          "Turn 180° right on the left foot toward da¹, right front stance. Scissors block.", face="R"),
       kick("26-1", "da1", "side", "L", face="R"),
       mv("26-2", "da1", "side", "front", "L", {"L": "punch"}, "punch", "L", "Land in a left front stance. Left middle punch.", face="R", note="bandae"),
       mv("26-3", "da1", "side", "front", "L", {"R": "punch"}, "punch", "R", "Right middle punch.", face="R", note="baro")]
TBL = {"r1": [["24-3", "24-2", "24-1"], ["4-3", "4-2", "4-1"], ["23", "3"], "J", ["1", "25"], ["2-1", "2-2", "2-3"], ["26-1", "26-2", "26-3"]],
       "c2": ["5", "6-1", "6-2", "7-1", "21", "22"],
       "c4": ["7-2", "8-1", "8-2", "19", "20"],
       "r5": [["13-2", "13-1", "12"], ["11", "10", "9"], ["14", "15", "16"], ["17", "18-1", "18-2"]]}
TBP = {"J": [50, 8], "1": [58, 8], "2-1": [64, 8], "2-2": [70, 8], "2-3": [70, 8], "3": [42, 8], "4-1": [36, 8], "4-2": [30, 8], "4-3": [30, 8],
       "5": [50, 15], "6-1": [50, 15], "6-2": [50, 24], "7-1": [50, 24], "7-2": [50, 34], "8-1": [50, 34], "8-2": [50, 44],
       "9": [44, 52], "10": [40, 52], "11": [40, 52], "12": [38, 52], "13-1": [32, 52], "13-2": [26, 52],
       "14": [58, 52], "15": [62, 52], "16": [62, 52], "17": [64, 52], "18-1": [70, 52], "18-2": [76, 52],
       "19": [50, 44], "20": [50, 34], "21": [50, 24], "22": [50, 15],
       "23": [40, 8], "24-1": [34, 8], "24-2": [26, 8], "24-3": [26, 8], "25": [60, 8], "26-1": [66, 8], "26-2": [74, 8], "26-3": [74, 8]}
form("taebaek", "Taebaek", "태백", "太白", "Bright mountain · Baekdusan",
     "工 · Gong · the craftsman",
     "Taebaek is the old name for Baekdusan, the mountain where, in legend, Dangun founded the first Korean kingdom. "
     "The floor line is 工: the character for a skilled maker, read as a bridge between heaven and earth. The first line is walked twice.",
     26, {"glyph": "工", "bars": {"r3": "gone"}, "rail": ["r1", "r5"], "notesBelow": True,
          "map": "M4 8H96M16 52H84M50 8V52"},
     TBL, TBP, TB, 1358, None, (1760, 94, 114), "2-1 kick, 2-2 and 2-3 punches",
     "Finish with <b>Baro</b>: turn to face ga and return to the ready stance at the starting point.")
