import json, os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(rel):
    with open(os.path.join(BASE_DIR, rel), 'r', encoding='utf-8') as f:
        return json.load(f)

def calc_standings(predictions, group_prefix):
    preds = {k: v for k, v in predictions.items() if k.startswith(group_prefix)}
    teams = {}
    for p in preds.values():
        ta, tb = p['team_a'], p['team_b']; sa, sb = p['predicted_score_a'], p['predicted_score_b']
        for t in [ta, tb]:
            teams.setdefault(t, {'p': 0, 'w': 0, 'd': 0, 'l': 0, 'gf': 0, 'ga': 0, 'pts': 0})
        teams[ta]['p'] += 1; teams[tb]['p'] += 1
        teams[ta]['gf'] += sa; teams[ta]['ga'] += sb
        teams[tb]['gf'] += sb; teams[tb]['ga'] += sa
        if sa > sb: teams[ta]['w'] += 1; teams[ta]['pts'] += 3; teams[tb]['l'] += 1
        elif sa < sb: teams[tb]['w'] += 1; teams[tb]['pts'] += 3; teams[ta]['l'] += 1
        else: teams[ta]['d'] += 1; teams[tb]['d'] += 1; teams[ta]['pts'] += 1; teams[tb]['pts'] += 1
    return sorted(teams.items(), key=lambda x: (-x[1]['pts'], -(x[1]['gf'] - x[1]['ga']), -x[1]['gf']))

def get_iso2(team_name):
    iso = {"墨西哥":"MX","南非":"ZA","韩国":"KR","捷克":"CZ","加拿大":"CA","波黑":"BA",
        "卡塔尔":"QA","瑞士":"CH","巴西":"BR","摩洛哥":"MA","海地":"HT","苏格兰":"GB",
        "美国":"US","巴拉圭":"PY","澳大利亚":"AU","土耳其":"TR","德国":"DE","库拉索":"CW",
        "科特迪瓦":"CI","厄瓜多尔":"EC","荷兰":"NL","日本":"JP","瑞典":"SE","突尼斯":"TN",
        "比利时":"BE","埃及":"EG","伊朗":"IR","新西兰":"NZ","西班牙":"ES","佛得角":"CV",
        "沙特阿拉伯":"SA","乌拉圭":"UY","法国":"FR","塞内加尔":"SN","伊拉克":"IQ","挪威":"NO",
        "阿根廷":"AR","阿尔及利亚":"DZ","奥地利":"AT","约旦":"JO","葡萄牙":"PT",
        "刚果民主共和国":"CD","乌兹别克斯坦":"UZ","哥伦比亚":"CO","英格兰":"GB","克罗地亚":"HR",
        "加纳":"GH","巴拿马":"PA"}
    return iso.get(team_name, "UN").lower()

def code2flag(c):
    return ''.join(chr(0x1F1E6 + ord(l) - ord('a')) for l in c[:2])

def flag_span(name):
    return f'<span style="font-size:1.2rem">{code2flag(get_iso2(name))}</span>'

def render_bracket(ko_by_round, ko_order):
    """Build bracket tree HTML using CSS Grid."""
    ko_map = {}
    for rn in ko_order:
        for m in ko_by_round.get(rn, []):
            ko_map[m['match_id']] = m

    sorted_ids = sorted(ko_map.keys(), key=lambda x: int(x.split('_')[1]))
    if not sorted_ids:
        return ''

    r32_ids = [i for i in sorted_ids if 1 <= int(i.split('_')[1]) <= 16]
    r16_ids = [i for i in sorted_ids if 17 <= int(i.split('_')[1]) <= 24]
    qf_ids  = [i for i in sorted_ids if 25 <= int(i.split('_')[1]) <= 28]
    sf_ids  = [i for i in sorted_ids if 29 <= int(i.split('_')[1]) <= 30]
    fn_ids  = [i for i in sorted_ids if int(i.split('_')[1]) == 31]
    tp_ids  = [i for i in sorted_ids if int(i.split('_')[1]) == 32]

    def card(m):
        if not m: return '<div class="bc"><span></span><span></span><span></span></div>'
        ta, tb = m['team_a'], m['team_b']
        sa, sb = m['predicted_score_a'], m['predicted_score_b']
        w = m.get('predicted_winner', '')
        t1_w = w == 'team_a'; t2_w = w == 'team_b'
        if t1_w:
            l = f'<span class="bw">{flag_span(ta)} {ta}</span>'
            r = f'<span class="bl">{tb} {flag_span(tb)}</span>'
        elif t2_w:
            l = f'<span class="bl">{flag_span(ta)} {ta}</span>'
            r = f'<span class="bw">{tb} {flag_span(tb)}</span>'
        else:
            l = f'<span>{flag_span(ta)} {ta}</span>'
            r = f'<span>{tb} {flag_span(tb)}</span>'
        return f'<div class="bc">{l}<span class="bs">{sa}:{sb}</span>{r}</div>'

    def row_range(idx, total_in_round):
        """Return (start, end) 1-indexed grid rows for match idx in a round with total_in_round matches."""
        span = 32 // total_in_round
        start = idx * span + 1
        return start, start + span - 1

    total_rows = 32
    html = '<div class="bracket-wrap"><div class="bracket-grid" style="grid-template-rows: repeat(32, minmax(28px, 1fr));">'

    # Column headers
    col_labels = [("32强", len(r32_ids)), ("16强", len(r16_ids)), ("8强", len(qf_ids)), ("4强", len(sf_ids)), ("决赛", len(fn_ids))]
    for ci, (label, cnt) in enumerate(col_labels):
        if cnt == 0: continue
        col = ci + 1
        gs, ge = row_range(0, cnt) if cnt > 0 else (1, 32)
        html += f'<div class="rl" style="grid-column:{col};grid-row:1/2;">{label}</div>'

    # R32
    for i, mid in enumerate(r32_ids):
        ci = 1; s, e = row_range(i, len(r32_ids))
        html += f'<div class="bracket-match" style="grid-column:{ci};grid-row:{s}/{e+1};">{card(ko_map.get(mid))}</div>'

    # R16
    for i, mid in enumerate(r16_ids):
        ci = 2; s, e = row_range(i, len(r16_ids))
        html += f'<div class="bracket-match" style="grid-column:{ci};grid-row:{s}/{e+1};">{card(ko_map.get(mid))}</div>'

    # QF
    for i, mid in enumerate(qf_ids):
        ci = 3; s, e = row_range(i, len(qf_ids))
        html += f'<div class="bracket-match" style="grid-column:{ci};grid-row:{s}/{e+1};">{card(ko_map.get(mid))}</div>'

    # SF
    for i, mid in enumerate(sf_ids):
        ci = 4; s, e = row_range(i, len(sf_ids))
        html += f'<div class="bracket-match" style="grid-column:{ci};grid-row:{s}/{e+1};">{card(ko_map.get(mid))}</div>'

    # Final
    for i, mid in enumerate(fn_ids):
        ci = 5; s, e = row_range(i, max(len(fn_ids), 1))
        html += f'<div class="bracket-match bf" style="grid-column:{ci};grid-row:{s}/{e+1};">{card(ko_map.get(mid))}</div>'

    html += '</div></div>'

    # 3rd place
    if tp_ids:
        tp = ko_map.get(tp_ids[0])
        if tp:
            html += f'<div class="tp-section"><span class="tp-label">🥉 季军赛</span>'
            html += f'<span class="tp-match">{card(tp)}</span></div>'

    return html

def generate_html(pred_data, standings, ko_by_round):
    model = pred_data['model_name']
    all_preds = pred_data['predictions']
    grp_preds = [p for p in all_preds if p['match_id'].startswith('GRP_')]
    ko_preds = [p for p in all_preds if p['match_id'].startswith('KO_')]

    groups = defaultdict(list)
    for p in grp_preds:
        g = p['match_id'].split('_')[1]
        groups[g].append(p)

    ko_order = ['32强', '16强', '四分之一决赛', '半决赛', '季军赛', '决赛']

    html = []
    html.append(f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🏆 2026世界杯预测 - {model}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:#0f172a; color:#e2e8f0; padding:20px 30px; }}
h1 {{ text-align:center; font-size:2rem; margin-bottom:4px; background:linear-gradient(135deg,#f59e0b,#ef4444); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
.subtitle {{ text-align:center; color:#64748b; margin-bottom:24px; font-size:0.9rem; }}
.section {{ background:#1e293b; border-radius:12px; padding:20px 24px; margin-bottom:20px; border:1px solid #334155; }}
.section h2 {{ font-size:1.2rem; margin-bottom:14px; color:#f59e0b; border-bottom:2px solid #334155; padding-bottom:8px; display:flex; align-items:center; gap:8px; }}
.group-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr)); gap:16px; }}
.group-card {{ background:#0f172a; border-radius:8px; padding:14px; border:1px solid #334155; }}
.group-card h3 {{ color:#38bdf8; margin-bottom:8px; font-size:1rem; }}
table {{ width:100%; border-collapse:collapse; font-size:0.82rem; }}
th {{ text-align:left; padding:4px 6px; color:#94a3b8; font-weight:500; border-bottom:1px solid #334155; font-size:0.72rem; }}
td {{ padding:4px 6px; border-bottom:1px solid #1e293b; }}
.rank-1 {{ color:#22c55e; font-weight:700; }}
.rank-2 {{ color:#38bdf8; font-weight:700; }}
.match-row {{ display:grid; grid-template-columns:1fr auto 1fr; align-items:center; padding:7px 0; gap:4px; }}
.match-sep {{ border-bottom:1px solid #1e293b; }}
.team-name {{ font-weight:500; font-size:0.88rem; white-space:nowrap; }}
.score-num {{ font-weight:700; color:#f59e0b; font-size:1.05rem; min-width:40px; text-align:center; }}
.win-badge {{ display:inline-block; background:#22c55e; color:#052e16; font-size:0.62rem; padding:1px 5px; border-radius:4px; font-weight:600; }}
.draw-badge {{ display:inline-block; background:#64748b; color:#0f172a; font-size:0.62rem; padding:1px 5px; border-radius:4px; font-weight:600; }}
.reason {{ font-size:0.7rem; color:#64748b; font-style:italic; }}
.stats-row {{ display:flex; gap:16px; flex-wrap:wrap; }}
.stat-card {{ background:#0f172a; border-radius:8px; padding:12px 18px; text-align:center; border:1px solid #334155; flex:1; min-width:100px; }}
.stat-card .num {{ font-size:1.6rem; font-weight:700; color:#f59e0b; }}
.stat-card .lbl {{ font-size:0.7rem; color:#94a3b8; margin-top:3px; }}
.footer {{ text-align:center; color:#475569; font-size:0.78rem; margin-top:24px; padding:12px; }}
.flag-em {{ font-size:1.2rem; }}

/* === BRACKET === */
.bracket-wrap {{ overflow-x:auto; padding:10px 0; }}
.bracket-grid {{ display:grid; gap:0; min-width:800px; align-items:stretch; }}
.rl {{ font-size:0.72rem; color:#94a3b8; font-weight:600; text-align:center; padding:4px; border-bottom:1px solid #334155; display:flex; align-items:center; justify-content:center; text-transform:uppercase; letter-spacing:1px; }}
.bracket-match {{ display:flex; align-items:center; padding:2px; }}
.bc {{ background:#0f172a; border:1px solid #334155; border-radius:6px; padding:4px 8px; width:100%; display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:4px; font-size:0.72rem; line-height:1.3; }}
.bc > span:first-child {{ text-align:left; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.bc > span:last-child {{ text-align:right; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.bc .bw {{ color:#22c55e; font-weight:600; }}
.bc .bl {{ color:#64748b; }}
.bc .bs {{ color:#f59e0b; font-weight:700; text-align:center; }}
.bf .bc {{ border-color:#f59e0b; border-width:2px; }}
.tp-section {{ text-align:center; margin-top:8px; padding:6px; background:#0f172a; border-radius:6px; border:1px solid #334155; }}
.tp-label {{ color:#94a3b8; font-size:0.75rem; margin-right:8px; }}
.tp-match {{ display:inline-block; }}
.tp-match .bc {{ border-color:#64748b; }}
@media (max-width:768px) {{ .bc {{ font-size:0.65rem; padding:3px 5px; }} }}
</style>
</head>
<body>
<h1>🏆 2026 FIFA 世界杯预测</h1>
<p class="subtitle">{model} · {pred_data.get('prediction_date','')} · 共 {pred_data['total_predictions']} 场预测</p>
''')

    # Stats
    wins = sum(1 for p in all_preds if p.get('predicted_winner') in ['team_a','team_b'])
    draws = sum(1 for p in all_preds if p.get('predicted_winner') == 'draw')
    avg_c = sum(p.get('confidence',0) for p in all_preds) / max(len(all_preds),1)
    html.append(f'''
<div class="section">
<h2>📊 预测概览</h2>
<div class="stats-row">
<div class="stat-card"><div class="num">{len(all_preds)}</div><div class="lbl">总预测场次</div></div>
<div class="stat-card"><div class="num">{wins}</div><div class="lbl">有胜负预测</div></div>
<div class="stat-card"><div class="num">{draws}</div><div class="lbl">平局预测</div></div>
<div class="stat-card"><div class="num">{avg_c:.0%}</div><div class="lbl">平均置信度</div></div>
</div>
</div>''')

    # Group Stage
    html.append('<div class="section"><h2>📋 小组赛预测</h2><div class="group-grid">')
    for g in sorted(groups.keys()):
        g_ms = sorted(groups[g], key=lambda x: x['match_id'])
        html.append(f'<div class="group-card"><h3>{g}组</h3>')
        for m in g_ms:
            ta, tb = m['team_a'], m['team_b']
            sa, sb = m['predicted_score_a'], m['predicted_score_b']
            w = m.get('predicted_winner',''); c = m.get('confidence',0); r = m.get('reasoning','')
            badge = ''
            if w == 'team_a': badge = '<span class="win-badge">WIN</span>'; t1d = f'<strong>{ta}</strong>'; t2d = tb
            elif w == 'team_b': badge = '<span class="win-badge">WIN</span>'; t1d = ta; t2d = f'<strong>{tb}</strong>'
            else: badge = '<span class="draw-badge">平</span>'; t1d = ta; t2d = tb
            f1 = flag_span(ta); f2 = flag_span(tb)
            html.append(f'''
<div class="match-row match-sep">
<div style="text-align:right;overflow:hidden;text-overflow:ellipsis;">{f1} <span class="team-name">{t1d}</span></div>
<span class="score-num">{sa}:{sb}</span>
<div style="text-align:left;overflow:hidden;text-overflow:ellipsis;"><span class="team-name">{t2d}</span> {f2} {badge}</div>
</div>''')
        html.append('</div>')
    html.append('</div></div>')

    # Standings
    if standings:
        html.append('<div class="section"><h2>🏅 小组排名 & 晋级球队</h2><div class="group-grid">')
        for g, st in sorted(standings.items()):
            html.append(f'<div class="group-card"><h3>{g}组</h3><table><tr><th>#</th><th>球队</th><th>赛</th><th>胜</th><th>平</th><th>负</th><th>进</th><th>失</th><th>净</th><th>分</th></tr>')
            for i, (team, s) in enumerate(st):
                cls = 'rank-1' if i == 0 else ('rank-2' if i == 1 else '')
                rk = '🥇' if i == 0 else ('🥈' if i == 1 else str(i+1))
                f = flag_span(team)
                html.append(f'<tr class="{cls}"><td>{rk}</td><td>{f} {team}</td><td>{s["p"]}</td><td>{s["w"]}</td><td>{s["d"]}</td><td>{s["l"]}</td><td>{s["gf"]}</td><td>{s["ga"]}</td><td>{s["gf"]-s["ga"]}</td><td><strong>{s["pts"]}</strong></td></tr>')
            html.append('</table></div>')
        html.append('</div></div>')

    # KO Tournament - Bracket
    if ko_by_round:
        html.append('<div class="section"><h2>🏆 淘汰赛晋级图</h2>')
        total_ko = sum(len(v) for v in ko_by_round.values())
        html.append(f'<div style="color:#94a3b8;font-size:0.78rem;margin-bottom:8px;">共 {total_ko} 场淘汰赛 · 绿色=胜者晋级</div>')
        html.append(render_bracket(ko_by_round, ko_order))
        html.append('</div>')

    # Champion
    final_ms = ko_by_round.get('决赛', [])
    if final_ms:
        fm = final_ms[0]
        champ = fm['team_a'] if fm['predicted_winner'] == 'team_a' else fm['team_b']
        runner = fm['team_b'] if fm['predicted_winner'] == 'team_a' else fm['team_a']
        f_champ = flag_span(champ)
        html.append(f'''
<div class="section" style="text-align:center;border:2px solid #f59e0b;">
<h2 style="border:none;justify-content:center;font-size:1.5rem;">🏆 预测冠军</h2>
<div style="font-size:3rem;margin:10px 0;">{f_champ}</div>
<div style="font-size:1.8rem;font-weight:700;color:#f59e0b;">{champ}</div>
<div style="color:#94a3b8;margin-top:8px;">亚军: {runner}</div>
<div style="color:#64748b;font-size:0.82rem;margin-top:4px;">决赛 {fm['predicted_score_a']}:{fm['predicted_score_b']}</div>
</div>''')

    html.append(f'<div class="footer">2026 FIFA World Cup · Generated on 2026-06-04</div></body></html>')
    return '\n'.join(html)

def main():
    import sys
    pred_file = sys.argv[1] if len(sys.argv) > 1 else 'predictions/gpt4_full.json'
    pred_data = load_json(pred_file)

    preds_by_id = {p['match_id']: p for p in pred_data['predictions']}

    groups_seen = set()
    for p in pred_data['predictions']:
        if p['match_id'].startswith('GRP_'):
            groups_seen.add(p['match_id'].split('_')[1])

    standings = {}
    for g in sorted(groups_seen):
        st = calc_standings(preds_by_id, f'GRP_{g}_')
        if st: standings[g] = st

    ko_by_round = defaultdict(list)
    for p in pred_data['predictions']:
        if p['match_id'].startswith('KO_'):
            r = p.get('round', '')
            ko_by_round[r].append(p)

    html = generate_html(pred_data, standings, ko_by_round)

    out = os.path.join(BASE_DIR, 'predictions_dashboard.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'✅ 仪表盘已生成: {out}')
    print(f'   模型: {pred_data["model_name"]} | 共 {len(pred_data["predictions"])} 场预测')
    print(f'   在浏览器中打开查看可视化结果')

if __name__ == '__main__':
    main()
