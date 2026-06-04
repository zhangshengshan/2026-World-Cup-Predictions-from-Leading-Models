import json, os, math, random
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEAM_STRENGTH = {
    "阿根廷":95,"法国":93,"巴西":92,"英格兰":91,"西班牙":90,"葡萄牙":88,"德国":87,
    "荷兰":86,"比利时":85,"克罗地亚":84,"乌拉圭":83,"哥伦比亚":82,"摩洛哥":81,"日本":80,
    "瑞士":79,"墨西哥":78,"美国":77,"厄瓜多尔":76,"塞内加尔":75,"奥地利":74,"伊朗":73,
    "韩国":72,"瑞典":71,"挪威":70,"苏格兰":69,"巴拉圭":68,"澳洲":67,"加拿大":66,"突尼斯":65,
    "阿尔及利亚":64,"捷克":63,"埃及":62,"波黑":61,"科特迪瓦":60,"加纳":59,"沙特":58,
    "土耳其":57,"卡塔尔":56,"巴拿马":55,"南非":54,"伊拉克":53,"新西兰":52,"约旦":51,
    "乌兹别克":50,"佛得角":49,"刚果":48,"库拉索":46,"海地":44,
}

SHORT_NAMES = {"澳大利亚":"澳洲","沙特阿拉伯":"沙特","刚果民主共和国":"刚果","乌兹别克斯坦":"乌兹别克"}
ALL_TEAMS = {
    "A":["墨西哥","南非","韩国","捷克"],"B":["加拿大","波黑","卡塔尔","瑞士"],
    "C":["巴西","摩洛哥","海地","苏格兰"],"D":["美国","巴拉圭","澳洲","土耳其"],
    "E":["德国","库拉索","科特迪瓦","厄瓜多尔"],"F":["荷兰","日本","瑞典","突尼斯"],
    "G":["比利时","埃及","伊朗","新西兰"],"H":["西班牙","佛得角","沙特","乌拉圭"],
    "I":["法国","塞内加尔","伊拉克","挪威"],"J":["阿根廷","阿尔及利亚","奥地利","约旦"],
    "K":["葡萄牙","刚果","乌兹别克","哥伦比亚"],"L":["英格兰","克罗地亚","加纳","巴拿马"],
}

def load_json(rel):
    with open(os.path.join(BASE_DIR, rel), 'r', encoding='utf-8') as f:
        return json.load(f)

def short_name(name):
    return SHORT_NAMES.get(name, name)

def get_iso2(name):
    m = {"墨西哥":"MX","南非":"ZA","韩国":"KR","捷克":"CZ","加拿大":"CA","波黑":"BA",
        "卡塔尔":"QA","瑞士":"CH","巴西":"BR","摩洛哥":"MA","海地":"HT","苏格兰":"GB",
        "美国":"US","巴拉圭":"PY","澳洲":"AU","土耳其":"TR","德国":"DE","库拉索":"CW",
        "科特迪瓦":"CI","厄瓜多尔":"EC","荷兰":"NL","日本":"JP","瑞典":"SE","突尼斯":"TN",
        "比利时":"BE","埃及":"EG","伊朗":"IR","新西兰":"NZ","西班牙":"ES","佛得角":"CV",
        "沙特":"SA","乌拉圭":"UY","法国":"FR","塞内加尔":"SN","伊拉克":"IQ","挪威":"NO",
        "阿根廷":"AR","阿尔及利亚":"DZ","奥地利":"AT","约旦":"JO","葡萄牙":"PT",
        "刚果":"CD","乌兹别克":"UZ","哥伦比亚":"CO","英格兰":"GB","克罗地亚":"HR",
        "加纳":"GH","巴拿马":"PA"}
    return m.get(name, "UN").lower()

def code2flag(c):
    return ''.join(chr(0x1F1E6 + ord(l) - ord('a')) for l in c[:2])

def flag_span(name):
    return f'<span style="font-size:1.2rem">{code2flag(get_iso2(name))}</span>'

def group_label_to_team(label, group_preds):
    """Convert 'A1' → actual team name from group predictions."""
    if len(label) < 2: return label
    g = label[0].upper(); pos = label[1:]
    if g not in group_preds: return label
    if pos == "1": return group_preds[g]["1st"]
    if pos == "2": return group_preds[g]["2nd"]
    return label

def build_ko_from_predictions(group_preds, ko_preds, seed=42):
    """Build ko_by_round from model's knockout predictions."""
    random.seed(seed)
    ko_by_round = {"32强":[],"16强":[],"四分之一决赛":[],"半决赛":[],"季军赛":[],"决赛":[]}
    ko_results = {}
    ko_idx = 1

    def make_match(t1, t2, rnd, mid=None):
        nonlocal ko_idx
        if mid is None: mid = f"KO_{ko_idx}"
        if t1 not in TEAM_STRENGTH or t2 not in TEAM_STRENGTH:
            return None
        rA, rB = TEAM_STRENGTH[t1], TEAM_STRENGTH[t2]
        diff = rA - rB
        win_p = 1 / (1 + math.exp(-diff / 15))
        r = random.random()
        if r < win_p:
            sa = max(1, round(rA / 22 + random.gauss(0, 0.4)))
            sb = max(0, round(rB / 28 + random.gauss(0, 0.3)))
            if sa <= sb: sa = sb + 1
            w = t1
        else:
            sb = max(1, round(rB / 22 + random.gauss(0, 0.4)))
            sa = max(0, round(rA / 28 + random.gauss(0, 0.3)))
            if sb <= sa: sb = sa + 1
            w = t2
        return {"match_id": mid, "team_a": t1, "team_b": t2,
                "predicted_winner": "team_a" if w == t1 else "team_b",
                "predicted_score_a": sa, "predicted_score_b": sb, "round": rnd}

    # Determine third-placed teams from group predictions
    thirds = []
    for g in sorted(group_preds):
        adv = {group_preds[g]["1st"], group_preds[g]["2nd"]}
        for t in ALL_TEAMS.get(g, []):
            if t not in adv:
                thirds.append(t)
                break
    # Sort third-place teams by strength, take top 8
    thirds.sort(key=lambda t: -TEAM_STRENGTH.get(t, 50))
    best_8 = thirds[:8]

    r32_pred = ko_preds.get("round_of_32", [])
    if r32_pred:
        # R32: 12 predicted by model
        for m in r32_pred:
            mid = f"KO_{ko_idx}"
            winner = group_label_to_team(m.get("winner",""), group_preds)
            parts = m.get("match","").split(" vs ")
            if len(parts) == 2:
                t1 = group_label_to_team(parts[0].strip(), group_preds)
                t2 = group_label_to_team(parts[1].strip(), group_preds)
            else:
                continue
            p = make_match(t1, t2, "32强", mid)
            if p and winner and winner in TEAM_STRENGTH:
                if winner == t1: p["predicted_winner"] = "team_a"
                elif winner == t2: p["predicted_winner"] = "team_b"
            if p:
                ko_by_round["32强"].append(p)
                w = t1 if p["predicted_winner"] == "team_a" else t2
                ko_results[mid] = w
                ko_idx += 1
    else:
        # No knockout predictions: auto-generate all R32 using standard bracket
        # 12 matches: group winners vs group runners-up/3rd
        g_list = sorted(group_preds.keys())
        # Pair 6 group winners with 6 runners-up, 6 group winners with 6 best 3rds
        for i in range(6):
            w_g = g_list[i]
            r_g = g_list[(i + 6) % 12]
            t1 = group_preds[w_g]["1st"]
            t2 = group_preds[r_g]["2nd"]
            mid = f"KO_{ko_idx}"
            p = make_match(t1, t2, "32强", mid)
            if p:
                ko_by_round["32强"].append(p)
                w = t1 if p["predicted_winner"] == "team_a" else t2
                ko_results[mid] = w
                ko_idx += 1
        for i in range(6):
            w_g = g_list[i + 6]
            t1 = group_preds[w_g]["1st"]
            t2 = best_8[i] if i < len(best_8) else None
            if not t2: continue
            mid = f"KO_{ko_idx}"
            p = make_match(t1, t2, "32强", mid)
            if p:
                ko_by_round["32强"].append(p)
                w = t1 if p["predicted_winner"] == "team_a" else t2
                ko_results[mid] = w
                ko_idx += 1

    # 4 more R32 matches between 8 best third-placed teams
    for i in range(0, min(8, len(best_8)), 2):
        if i + 1 >= len(best_8): break
        t1, t2 = best_8[i], best_8[i+1]
        mid = f"KO_{ko_idx}"
        p = make_match(t1, t2, "32强", mid)
        if p:
            ko_by_round["32强"].append(p)
            w = t1 if p["predicted_winner"] == "team_a" else t2
            ko_results[mid] = w
            ko_idx += 1

    # Subsequent rounds: use model's predictions
    SOURCE_ROUND = {"16强":"32强","四分之一决赛":"16强","半决赛":"四分之一决赛"}

    def sim_round(kp_key, rnd_name, count):
        nonlocal ko_idx
        preds = ko_preds.get(kp_key, [])
        src_name = SOURCE_ROUND[rnd_name]
        src_matches = ko_by_round[src_name]
        for i in range(count):
            idx = i * 2
            if idx + 1 >= len(src_matches):
                break
            w1 = ko_results.get(src_matches[idx]["match_id"])
            w2 = ko_results.get(src_matches[idx+1]["match_id"])
            if not w1 or not w2: continue
            pred_winner = preds[i].get("winner", "") if i < len(preds) else ""
            mid = f"KO_{ko_idx}"
            p = make_match(w1, w2, rnd_name, mid)
            if p and pred_winner and pred_winner in [w1, w2]:
                if pred_winner == w1: p["predicted_winner"] = "team_a"
                else: p["predicted_winner"] = "team_b"
            if p:
                ko_by_round[rnd_name].append(p)
                w = w1 if p["predicted_winner"] == "team_a" else w2
                ko_results[mid] = w
                ko_idx += 1

    sim_round("round_of_16", "16强", 8)
    sim_round("quarterfinals", "四分之一决赛", 4)
    sim_round("semifinals", "半决赛", 2)

    # Final
    sf_matches = ko_by_round["半决赛"]
    if len(sf_matches) >= 2:
        w1 = ko_results.get(sf_matches[0]["match_id"])
        w2 = ko_results.get(sf_matches[1]["match_id"])
        if w1 and w2:
            f_pred = ko_preds.get("final", {})
            f_winner = f_pred.get("winner", "") if isinstance(f_pred, dict) else ""
            mid = f"KO_{ko_idx}"
            p = make_match(w1, w2, "决赛", mid)
            if p and f_winner and f_winner in [w1, w2]:
                if f_winner == w1: p["predicted_winner"] = "team_a"
                else: p["predicted_winner"] = "team_b"
            if p:
                ko_by_round["决赛"].append(p)
                ko_idx += 1

            # 3rd place
            l1 = sf_matches[0]["team_b"] if ko_results.get(sf_matches[0]["match_id"]) == sf_matches[0]["team_a"] else sf_matches[0]["team_a"]
            l2 = sf_matches[1]["team_b"] if ko_results.get(sf_matches[1]["match_id"]) == sf_matches[1]["team_a"] else sf_matches[1]["team_a"]
            tp_pred = ko_preds.get("third_place", {})
            tp_w = tp_pred.get("winner", "") if isinstance(tp_pred, dict) else ""
            mid3 = f"KO_{ko_idx}"
            p3 = make_match(l1, l2, "季军赛", mid3)
            if p3 and tp_w and tp_w in [l1, l2]:
                if tp_w == l1: p3["predicted_winner"] = "team_a"
                else: p3["predicted_winner"] = "team_b"
            if p3:
                ko_by_round["季军赛"].append(p3)

    return ko_by_round


def render_bracket(ko_by_round):
    ko_map = {}
    for rn in ["32强","16强","四分之一决赛","半决赛","季军赛","决赛"]:
        for m in ko_by_round.get(rn, []):
            ko_map[m['match_id']] = m

    sorted_ids = sorted(ko_map.keys(), key=lambda x: int(x.split('_')[1]))
    r32 = [i for i in sorted_ids if 1 <= int(i.split('_')[1]) <= 16]
    r16 = [i for i in sorted_ids if 17 <= int(i.split('_')[1]) <= 24]
    qf  = [i for i in sorted_ids if 25 <= int(i.split('_')[1]) <= 28]
    sf  = [i for i in sorted_ids if 29 <= int(i.split('_')[1]) <= 30]
    fn  = [i for i in sorted_ids if int(i.split('_')[1]) == 31]
    tp  = [i for i in sorted_ids if int(i.split('_')[1]) == 32]

    def card(m):
        if not m: return '<div class="bc"><span></span><span></span><span></span><span></span><span></span></div>'
        ta, tb = short_name(m['team_a']), short_name(m['team_b'])
        sa, sb = m['predicted_score_a'], m['predicted_score_b']
        w = m.get('predicted_winner','')
        fl, fr = flag_span(ta), flag_span(tb)
        lc = 'bw' if w == 'team_a' else ('bl' if w == 'team_b' else '')
        rc = 'bw' if w == 'team_b' else ('bl' if w == 'team_a' else '')
        return f'<div class="bc"><span style="text-align:right;">{fl}</span><span style="text-align:right;"><span class="{lc}">{ta}</span></span><span class="bs">{sa}:{sb}</span><span style="text-align:left;"><span class="{rc}">{tb}</span></span><span style="text-align:left;">{fr}</span></div>'

    def rr(idx, total):
        span = 32 // max(total, 1); s = idx * span + 1
        return s, s + span - 1

    html = '<div class="bracket-wrap"><div class="bracket-grid" style="grid-template-rows:repeat(32,minmax(28px,1fr));">'
    for ci, (lb, ms) in enumerate([("32强",r32),("16强",r16),("8强",qf),("4强",sf),("决赛",fn)]):
        if not ms: continue
        html += f'<div class="rl" style="grid-column:{ci+1};grid-row:1/2;">{lb}</div>'
        for i, mid in enumerate(ms):
            s, e = rr(i, len(ms))
            html += f'<div class="bracket-match" style="grid-column:{ci+1};grid-row:{s}/{e+1};">{card(ko_map.get(mid))}</div>'
    html += '</div></div>'

    if tp:
        tpm = ko_map.get(tp[0])
        if tpm:
            html += f'<div class="tp-section"><span class="tp-label">🥉 季军赛</span>{card(tpm)}</div>'
    return html


def generate_html(group_preds, model_name, ko_by_round):
    html = []
    html.append(f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🏆 2026世界杯预测 - {model_name}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:#0f172a; color:#e2e8f0; padding:20px 30px; }}
h1 {{ text-align:center; font-size:2rem; margin-bottom:4px; background:linear-gradient(135deg,#f59e0b,#ef4444); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
.subtitle {{ text-align:center; color:#64748b; margin-bottom:24px; font-size:0.9rem; }}
.section {{ background:#1e293b; border-radius:12px; padding:20px 24px; margin-bottom:20px; border:1px solid #334155; }}
.section h2 {{ font-size:1.2rem; margin-bottom:14px; color:#f59e0b; border-bottom:2px solid #334155; padding-bottom:8px; display:flex; align-items:center; gap:8px; }}
.group-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:14px; }}
.group-card {{ background:#0f172a; border-radius:8px; padding:14px; border:1px solid #334155; }}
.group-card h3 {{ color:#38bdf8; margin-bottom:8px; font-size:1rem; }}
table {{ width:100%; border-collapse:collapse; font-size:0.85rem; }}
th {{ text-align:left; padding:5px 6px; color:#94a3b8; font-weight:500; border-bottom:1px solid #334155; font-size:0.72rem; }}
td {{ padding:5px 6px; border-bottom:1px solid #1e293b; }}
.r1 {{ color:#22c55e; font-weight:700; }}
.r2 {{ color:#38bdf8; font-weight:700; }}
.footer {{ text-align:center; color:#475569; font-size:0.78rem; margin-top:24px; padding:12px; }}
.bracket-wrap {{ overflow-x:auto; padding:10px 0; }}
.bracket-grid {{ display:grid; gap:0; min-width:750px; align-items:stretch; }}
.rl {{ font-size:0.72rem; color:#94a3b8; font-weight:600; text-align:center; padding:4px; border-bottom:1px solid #334155; display:flex; align-items:center; justify-content:center; letter-spacing:1px; }}
.bracket-match {{ display:flex; align-items:center; padding:2px; }}
.bc {{ background:#0f172a; border:1px solid #334155; border-radius:6px; padding:3px 6px; width:100%; display:grid; grid-template-columns:20px 1fr 30px 1fr 20px; align-items:center; gap:2px; font-size:0.72rem; line-height:1.3; }}
.bc > span {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.bc .bw {{ background:rgba(34,197,94,0.25); border-radius:3px; padding:1px 4px; font-weight:700; color:#22c55e; }}
.bc .bl {{ color:#64748b; }}
.bc .bs {{ color:#f59e0b; font-weight:700; text-align:center; }}
.bf .bc {{ border-color:#f59e0b; border-width:2px; }}
.tp-section {{ text-align:center; margin-top:8px; padding:6px; background:#0f172a; border-radius:6px; border:1px solid #334155; }}
.tp-label {{ color:#94a3b8; font-size:0.75rem; margin-right:8px; }}
.tp-match {{ display:inline-block; }}
.tp-match .bc {{ border-color:#64748b; }}
</style>
</head>
<body>
<h1>🏆 2026 FIFA 世界杯预测</h1>
<p class="subtitle">{model_name}</p>
''')

    html.append('<div class="section"><h2>📋 小组出线预测</h2><div class="group-grid">')
    for g in sorted(group_preds.keys()):
        p = group_preds[g]
        html.append(f'<div class="group-card"><h3>{g}组</h3><table><tr><th>排名</th><th>球队</th></tr>')
        html.append(f'<tr class="r1"><td>🥇 第1</td><td>{flag_span(p["1st"])} {short_name(p["1st"])}</td></tr>')
        html.append(f'<tr class="r2"><td>🥈 第2</td><td>{flag_span(p["2nd"])} {short_name(p["2nd"])}</td></tr>')
        html.append('</table></div>')
    html.append('</div></div>')

    if ko_by_round and any(ko_by_round.values()):
        html.append('<div class="section"><h2>🏆 淘汰赛晋级图</h2>')
        total = sum(len(v) for v in ko_by_round.values())
        html.append(f'<div style="color:#94a3b8;font-size:0.78rem;margin-bottom:8px;">共 {total} 场淘汰赛 · 绿色=胜者晋级</div>')
        html.append(render_bracket(ko_by_round))
        html.append('</div>')

    final_ms = ko_by_round.get('决赛', [])
    if final_ms:
        fm = final_ms[0]
        champ = short_name(fm['team_a'] if fm['predicted_winner'] == 'team_a' else fm['team_b'])
        runner = short_name(fm['team_b'] if fm['predicted_winner'] == 'team_a' else fm['team_a'])
        html.append(f'''
<div class="section" style="text-align:center;border:2px solid #f59e0b;">
<h2 style="border:none;justify-content:center;font-size:1.5rem;">🏆 预测冠军</h2>
<div style="font-size:3rem;margin:10px 0;">{flag_span(champ)}</div>
<div style="font-size:1.8rem;font-weight:700;color:#f59e0b;">{champ}</div>
<div style="color:#94a3b8;margin-top:8px;">亚军: {runner}</div>
</div>''')

    html.append(f'<div class="footer">2026 FIFA World Cup · Generated on 2026-06-04</div></body></html>')
    return '\n'.join(html)


def main():
    import sys
    pred_file = sys.argv[1] if len(sys.argv) > 1 else 'predictions/gpt4.json'
    data = load_json(pred_file)

    # Detect format
    if "groups" in data:
        # New format with optional "knockout"
        group_preds = data["groups"]
        model_name = data.get("model_name", pred_file.split("/")[-1].replace(".json",""))
        ko_preds = data.get("knockout", {})
        ko_by_round = build_ko_from_predictions(group_preds, ko_preds)
    elif "predictions" in data:
        raw = data["predictions"]
        if isinstance(raw, dict):
            group_preds = raw
            model_name = data.get("model_name", pred_file.split("/")[-1].replace(".json",""))
            ko_by_round = build_ko_from_predictions(group_preds, {})
        elif isinstance(raw, list):
            # Legacy full match format
            print("⚠️  旧格式检测到，转换为分组预测…")
            pts = defaultdict(lambda: defaultdict(int))
            for p in raw:
                if not p["match_id"].startswith("GRP_"): continue
                g = p["match_id"].split("_")[1]
                ta, tb = p["team_a"], p["team_b"]
                sa, sb = p["predicted_score_a"], p["predicted_score_b"]
                if sa > sb: pts[g][ta] += 3; pts[g][tb] += 0
                elif sa < sb: pts[g][tb] += 3; pts[g][ta] += 0
                else: pts[g][ta] += 1; pts[g][tb] += 1
            group_preds = {}
            for g in sorted(ALL_TEAMS):
                if g not in pts: continue
                st = sorted(pts[g].keys(), key=lambda t: -pts[g][t])
                if len(st) >= 2:
                    group_preds[g] = {"1st": st[0], "2nd": st[1]}
            model_name = data.get("model_name", pred_file.split("/")[-1].replace(".json",""))
            ko_by_round = build_ko_from_predictions(group_preds, {})
    else:
        print("❌ 无法识别的文件格式")
        return

    html = generate_html(group_preds, model_name, ko_by_round)

    out = os.path.join(BASE_DIR, 'predictions_dashboard.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'✅ 仪表盘已生成: {out}')
    print(f'   模型: {model_name}')

if __name__ == '__main__':
    main()
