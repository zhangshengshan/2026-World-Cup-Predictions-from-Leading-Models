import json

GROUPS = {
    "A": {"name": "A组", "teams": [
        ("墨西哥", "MEX"), ("南非", "RSA"), ("韩国", "KOR"), ("捷克", "CZE")
    ]},
    "B": {"name": "B组", "teams": [
        ("加拿大", "CAN"), ("波黑", "BIH"), ("卡塔尔", "QAT"), ("瑞士", "SUI")
    ]},
    "C": {"name": "C组", "teams": [
        ("巴西", "BRA"), ("摩洛哥", "MAR"), ("海地", "HAI"), ("苏格兰", "SCO")
    ]},
    "D": {"name": "D组", "teams": [
        ("美国", "USA"), ("巴拉圭", "PAR"), ("澳大利亚", "AUS"), ("土耳其", "TUR")
    ]},
    "E": {"name": "E组", "teams": [
        ("德国", "GER"), ("库拉索", "CUW"), ("科特迪瓦", "CIV"), ("厄瓜多尔", "ECU")
    ]},
    "F": {"name": "F组", "teams": [
        ("荷兰", "NED"), ("日本", "JPN"), ("瑞典", "SWE"), ("突尼斯", "TUN")
    ]},
    "G": {"name": "G组", "teams": [
        ("比利时", "BEL"), ("埃及", "EGY"), ("伊朗", "IRN"), ("新西兰", "NZL")
    ]},
    "H": {"name": "H组", "teams": [
        ("西班牙", "ESP"), ("佛得角", "CPV"), ("沙特阿拉伯", "KSA"), ("乌拉圭", "URU")
    ]},
    "I": {"name": "I组", "teams": [
        ("法国", "FRA"), ("塞内加尔", "SEN"), ("伊拉克", "IRQ"), ("挪威", "NOR")
    ]},
    "J": {"name": "J组", "teams": [
        ("阿根廷", "ARG"), ("阿尔及利亚", "ALG"), ("奥地利", "AUT"), ("约旦", "JOR")
    ]},
    "K": {"name": "K组", "teams": [
        ("葡萄牙", "POR"), ("刚果民主共和国", "COD"), ("乌兹别克斯坦", "UZB"), ("哥伦比亚", "COL")
    ]},
    "L": {"name": "L组", "teams": [
        ("英格兰", "ENG"), ("克罗地亚", "CRO"), ("加纳", "GHA"), ("巴拿马", "PAN")
    ]}
}

MATCHDAY_DATES = {
    "A": [("2026-06-11", "2026-06-11"), ("2026-06-16", "2026-06-16"), ("2026-06-20", "2026-06-20")],
    "B": [("2026-06-12", "2026-06-12"), ("2026-06-17", "2026-06-17"), ("2026-06-21", "2026-06-21")],
    "C": [("2026-06-13", "2026-06-13"), ("2026-06-18", "2026-06-18"), ("2026-06-22", "2026-06-22")],
    "D": [("2026-06-12", "2026-06-12"), ("2026-06-16", "2026-06-16"), ("2026-06-21", "2026-06-21")],
    "E": [("2026-06-14", "2026-06-14"), ("2026-06-18", "2026-06-18"), ("2026-06-22", "2026-06-22")],
    "F": [("2026-06-13", "2026-06-13"), ("2026-06-17", "2026-06-17"), ("2026-06-22", "2026-06-22")],
    "G": [("2026-06-14", "2026-06-14"), ("2026-06-19", "2026-06-19"), ("2026-06-23", "2026-06-23")],
    "H": [("2026-06-15", "2026-06-15"), ("2026-06-19", "2026-06-19"), ("2026-06-23", "2026-06-23")],
    "I": [("2026-06-15", "2026-06-15"), ("2026-06-20", "2026-06-20"), ("2026-06-24", "2026-06-24")],
    "J": [("2026-06-14", "2026-06-14"), ("2026-06-19", "2026-06-19"), ("2026-06-24", "2026-06-24")],
    "J": [("2026-06-14", "2026-06-14"), ("2026-06-19", "2026-06-19"), ("2026-06-24", "2026-06-24")],
    "K": [("2026-06-15", "2026-06-15"), ("2026-06-20", "2026-06-20"), ("2026-06-24", "2026-06-24")],
    "L": [("2026-06-15", "2026-06-15"), ("2026-06-20", "2026-06-20"), ("2026-06-25", "2026-06-25")],
}

# Fix duplicate J group key
MATCHDAY_DATES = {
    "A": [("2026-06-11", "2026-06-11"), ("2026-06-16", "2026-06-16"), ("2026-06-20", "2026-06-20")],
    "B": [("2026-06-12", "2026-06-12"), ("2026-06-17", "2026-06-17"), ("2026-06-21", "2026-06-21")],
    "C": [("2026-06-13", "2026-06-13"), ("2026-06-18", "2026-06-18"), ("2026-06-22", "2026-06-22")],
    "D": [("2026-06-12", "2026-06-12"), ("2026-06-16", "2026-06-16"), ("2026-06-21", "2026-06-21")],
    "E": [("2026-06-14", "2026-06-14"), ("2026-06-18", "2026-06-18"), ("2026-06-22", "2026-06-22")],
    "F": [("2026-06-13", "2026-06-13"), ("2026-06-17", "2026-06-17"), ("2026-06-22", "2026-06-22")],
    "G": [("2026-06-14", "2026-06-14"), ("2026-06-19", "2026-06-19"), ("2026-06-23", "2026-06-23")],
    "H": [("2026-06-15", "2026-06-15"), ("2026-06-19", "2026-06-19"), ("2026-06-23", "2026-06-23")],
    "I": [("2026-06-15", "2026-06-15"), ("2026-06-20", "2026-06-20"), ("2026-06-24", "2026-06-24")],
    "J": [("2026-06-14", "2026-06-14"), ("2026-06-19", "2026-06-19"), ("2026-06-24", "2026-06-24")],
    "K": [("2026-06-15", "2026-06-15"), ("2026-06-20", "2026-06-20"), ("2026-06-24", "2026-06-24")],
    "L": [("2026-06-15", "2026-06-15"), ("2026-06-20", "2026-06-20"), ("2026-06-25", "2026-06-25")],
}

def build_group_matches():
    groups_data = {}
    mid = 1
    for g_letter in sorted(GROUPS.keys()):
        g = GROUPS[g_letter]
        teams = g["teams"]
        dates = MATCHDAY_DATES[g_letter]
        matches = []
        pair_idx = 0
        for md in range(3):
            d1, d2 = dates[md]
            t1, t2 = teams[0], teams[md + 1]
            matches.append({
                "match_id": f"GRP_{g_letter}_{pair_idx + 1}",
                "round": "小组赛",
                "group": g_letter,
                "matchday": md + 1,
                "date": d1,
                "team_a": t1[0], "team_a_code": t1[1],
                "team_b": t2[0], "team_b_code": t2[1],
                "status": "scheduled",
                "actual_score_a": None, "actual_score_b": None,
                "actual_winner": None, "notes": ""
            })
            pair_idx += 1
            for r in range(1, 3):
                t_a = teams[r]
                t_b = teams[r + 1] if r < 2 else teams[1]
                matches.append({
                    "match_id": f"GRP_{g_letter}_{pair_idx + 1}",
                    "round": "小组赛",
                    "group": g_letter,
                    "matchday": md + 1,
                    "date": d2 if r == 2 else d1,
                    "team_a": t_a[0], "team_a_code": t_a[1],
                    "team_b": t_b[0], "team_b_code": t_b[1],
                    "status": "scheduled",
                    "actual_score_a": None, "actual_score_b": None,
                    "actual_winner": None, "notes": ""
                })
                pair_idx += 1

        # Fix: the rotation schedule for a 4-team group is:
        # MD1: 1v2, 3v4
        # MD2: 1v3, 4v2
        # MD3: 1v4, 2v3
        # Proper algorithm:
        matches = []
        t = [teams[0], teams[1], teams[2], teams[3]]
        md_matches = [
            [(0, 1), (2, 3)],  # MD1
            [(0, 2), (3, 1)],  # MD2
            [(0, 3), (1, 2)],  # MD3
        ]
        mid_in_group = 1
        for md in range(3):
            d1, d2 = dates[md]
            for pair_idx, (i, j) in enumerate(md_matches[md]):
                match_date = d1 if pair_idx == 0 else d2
                matches.append({
                    "match_id": f"GRP_{g_letter}_{mid_in_group}",
                    "round": "小组赛",
                    "group": g_letter,
                    "matchday": md + 1,
                    "date": match_date,
                    "team_a": t[i][0], "team_a_code": t[i][1],
                    "team_b": t[j][0], "team_b_code": t[j][1],
                    "status": "scheduled",
                    "actual_score_a": None, "actual_score_b": None,
                    "actual_winner": None, "notes": ""
                })
                mid_in_group += 1

        groups_data[g_letter] = {
            "group_name": g["name"],
            "teams_display": [t[0] for t in teams],
            "matches": matches
        }
    return groups_data


def build_knockout():
    return {
        "round_of_32": {
            "stage_name": "32强淘汰赛",
            "date_range": "2026-06-28 ~ 2026-07-01",
            "matches": []
        },
        "round_of_16": {
            "stage_name": "16强淘汰赛",
            "date_range": "2026-07-04 ~ 2026-07-06",
            "matches": []
        },
        "quarterfinals": {
            "stage_name": "四分之一决赛",
            "date_range": "2026-07-09 ~ 2026-07-11",
            "matches": []
        },
        "semifinals": {
            "stage_name": "半决赛",
            "date_range": "2026-07-14 ~ 2026-07-15",
            "matches": []
        },
        "third_place_playoff": {
            "stage_name": "季军争夺战",
            "date": "2026-07-18",
            "matches": []
        },
        "final": {
            "stage_name": "决赛",
            "date": "2026-07-19",
            "matches": []
        }
    }


def main():
    groups_data = build_group_matches()
    knockout = build_knockout()

    data = {
        "tournament": "2026 FIFA World Cup",
        "host_countries": ["美国", "加拿大", "墨西哥"],
        "total_matches": 104,
        "format": {
            "group_stage": 72,
            "knockout_stage": 32,
            "description": "48支球队分为12组，每组前两名+8个成绩最好的小组第三晋级32强"
        },
        "group_stage": {
            "groups": groups_data
        },
        "knockout_stage": knockout,
        "metadata": {
            "created_date": "2026-06-04",
            "last_updated": "2026-06-04",
            "status": "preparing",
            "notes": "基于2026 FIFA世界杯真实分组（48队，12组），淘汰赛采用32强→16强→8强→4强→决赛赛制"
        }
    }

    import os
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "matches", "matches_sample.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已生成 {path}")
    print(f"   共 {sum(len(g['matches']) for g in data['group_stage']['groups'].values())} 场小组赛")
    print(f"   12个小组，48支球队")


if __name__ == "__main__":
    main()
