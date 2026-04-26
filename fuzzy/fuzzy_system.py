FUZZY_RULES = [
    {'id': 'R1',  'color': 'green', 'desc': 'Kelembapan ideal + cahaya cukup + suhu normal + penyiraman cukup → Sehat'},
    {'id': 'R2',  'color': 'red',   'desc': 'Kelembapan kering + penyiraman jarang → Kurang Sehat'},
    {'id': 'R3',  'color': 'red',   'desc': 'Kelembapan terlalu basah + penyiraman sering → Kurang Sehat'},
    {'id': 'R4',  'color': 'amber', 'desc': 'Cahaya rendah + kelembapan ideal → Cukup Sehat'},
    {'id': 'R5',  'color': 'red',   'desc': 'Cahaya rendah + suhu dingin → Kurang Sehat'},
    {'id': 'R6',  'color': 'green', 'desc': 'Cahaya cukup + suhu normal → Sehat'},
    {'id': 'R7',  'color': 'red',   'desc': 'Cahaya berlebih + suhu panas → Kurang Sehat'},
    {'id': 'R8',  'color': 'red',   'desc': 'Suhu panas + kelembapan kering → Kurang Sehat'},
    {'id': 'R9',  'color': 'amber', 'desc': 'Suhu normal + penyiraman cukup → Cukup Sehat'},
    {'id': 'R10', 'color': 'red',   'desc': 'Suhu dingin + penyiraman sering → Kurang Sehat'},
    {'id': 'R11', 'color': 'amber', 'desc': 'Kelembapan ideal + cahaya cukup + penyiraman jarang → Cukup Sehat'},
    {'id': 'R12', 'color': 'red',   'desc': 'Kelembapan terlalu basah + cahaya rendah + suhu dingin → Kurang Sehat'},
    {'id': 'R13', 'color': 'red',   'desc': 'Kelembapan kering + cahaya berlebih + suhu panas → Kurang Sehat'},
    {'id': 'R14', 'color': 'amber', 'desc': 'Kelembapan ideal + suhu normal + cahaya rendah → Cukup Sehat'},
    {'id': 'R15', 'color': 'amber', 'desc': 'Kelembapan ideal + cahaya cukup + suhu normal + penyiraman sering → Cukup Sehat'},
]

RULE_BY_ID = {rule['id']: rule for rule in FUZZY_RULES}

CATEGORY_COLOR = {
    'kering': 'red',
    'ideal': 'green',
    'terlalu basah': 'blue',
    'rendah': 'gray',
    'cukup': 'green',
    'berlebih': 'amber',
    'dingin': 'blue',
    'normal': 'green',
    'panas': 'red',
    'jarang': 'red',
    'sering': 'blue',
}

def to_int(value, default, minimum, maximum):
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = default
    return max(minimum, min(maximum, number))

def fuzzify(values):
    kelembapan = values['kelembapan']
    cahaya = values['cahaya']
    suhu = values['suhu']
    siram = values['siram']
    return {
        'k': 'kering' if kelembapan <= 35 else 'ideal' if kelembapan <= 70 else 'terlalu basah',
        'c': 'rendah' if cahaya <= 35 else 'cukup' if cahaya <= 75 else 'berlebih',
        's': 'dingin' if suhu <= 20 else 'normal' if suhu <= 30 else 'panas',
        'p': 'jarang' if siram <= 1 else 'cukup' if siram <= 4 else 'sering',
    }

def evaluate_rules(categories):
    k, c, s, p = categories['k'], categories['c'], categories['s'], categories['p']

    skor_k = 25 if k == 'ideal' else 10
    skor_c = 25 if c == 'cukup' else 10
    skor_s = 25 if s == 'normal' else 10
    skor_p = 25 if p == 'cukup' else 10
    total = skor_k + skor_c + skor_s + skor_p

    fired = []
    if k == 'ideal' and c == 'cukup' and s == 'normal' and p == 'cukup': fired.append('R1')
    if k == 'kering' and p == 'jarang': fired.append('R2')
    if k == 'terlalu basah' and p == 'sering': fired.append('R3')
    if c == 'rendah' and k == 'ideal': fired.append('R4')
    if c == 'rendah' and s == 'dingin': fired.append('R5')
    if c == 'cukup' and s == 'normal': fired.append('R6')
    if c == 'berlebih' and s == 'panas': fired.append('R7')
    if s == 'panas' and k == 'kering': fired.append('R8')
    if s == 'normal' and p == 'cukup': fired.append('R9')
    if s == 'dingin' and p == 'sering': fired.append('R10')
    if k == 'ideal' and c == 'cukup' and p == 'jarang': fired.append('R11')
    if k == 'terlalu basah' and c == 'rendah' and s == 'dingin': fired.append('R12')
    if k == 'kering' and c == 'berlebih' and s == 'panas': fired.append('R13')
    if k == 'ideal' and s == 'normal' and c == 'rendah': fired.append('R14')
    if k == 'ideal' and c == 'cukup' and s == 'normal' and p == 'sering': fired.append('R15')

    return total, [RULE_BY_ID[rule_id] for rule_id in fired]

def defuzzify(score):
    if score >= 71:
        return {'kat': 'Sehat', 'cls': 'green', 'bar': '#639922'}
    if score >= 41:
        return {'kat': 'Cukup Sehat', 'cls': 'amber', 'bar': '#ba7517'}
    return {'kat': 'Kurang Sehat', 'cls': 'red', 'bar': '#e24b4a'}

def label(text):
    return text[:1].upper() + text[1:]

def analyze(values, pakar_url='#'):
    categories = fuzzify(values)
    score, fired_rules = evaluate_rules(categories)
    output = defuzzify(score)

    masalah = []
    if categories['k'] != 'ideal': masalah.append(f"kelembapan tanah {categories['k']}")
    if categories['c'] != 'cukup': masalah.append(f"cahaya {categories['c']}")
    if categories['s'] != 'normal': masalah.append(f"suhu {categories['s']}")
    if categories['p'] != 'cukup': masalah.append(f"penyiraman {categories['p']}")

    if output['kat'] == 'Sehat':
        recommendation = 'Kondisi tanaman tergolong baik. Lanjutkan perawatan rutin dan pantau kondisi daun serta tanah secara berkala.'
    elif output['kat'] == 'Cukup Sehat':
        recommendation = f"Tanaman masih cukup baik, namun perlu perbaikan pada: {', '.join(masalah)}. Gunakan Sistem Pakar untuk panduan lebih detail."
    else:
        recommendation = f"Tanaman membutuhkan perhatian segera pada: {', '.join(masalah)}. Segera cek Sistem Pakar untuk rekomendasi perawatan."

    details = [
        {'label': 'Kelembapan', 'val': categories['k'], 'shown': label(categories['k']), 'ok': categories['k'] == 'ideal'},
        {'label': 'Cahaya', 'val': categories['c'], 'shown': label(categories['c']), 'ok': categories['c'] == 'cukup'},
        {'label': 'Suhu', 'val': categories['s'], 'shown': label(categories['s']), 'ok': categories['s'] == 'normal'},
        {'label': 'Penyiraman', 'val': categories['p'], 'shown': label(categories['p']), 'ok': categories['p'] == 'cukup'},
    ]

    tags = {
        'kelembapan': {'label': label(categories['k']), 'class': CATEGORY_COLOR[categories['k']]},
        'cahaya': {'label': label(categories['c']), 'class': CATEGORY_COLOR[categories['c']]},
        'suhu': {'label': label(categories['s']), 'class': CATEGORY_COLOR[categories['s']]},
        'siram': {'label': label(categories['p']), 'class': CATEGORY_COLOR[categories['p']]},
    }

    return {
        'score': score,
        'category': output['kat'],
        'class': output['cls'],
        'bar': output['bar'],
        'categories': categories,
        'details': details,
        'fired_rules': fired_rules,
        'recommendation': recommendation,
        'tags': tags,
        'pakar_url': pakar_url,
    }
