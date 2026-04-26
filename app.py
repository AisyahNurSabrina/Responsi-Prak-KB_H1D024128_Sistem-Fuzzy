import os
from flask import Flask, render_template, request, send_from_directory
from fuzzy.fuzzy_system import analyze, to_int

app = Flask(__name__, template_folder="templates")

DEFAULT_VALUES = {
    'kelembapan': 50,
    'cahaya': 50,
    'suhu': 27,
    'siram': 3,
}

@app.route('/style.css')
def style_css():
    return send_from_directory('public', 'style.css')

@app.route('/', methods=['GET', 'POST'])
def index():
    values = DEFAULT_VALUES.copy()
    result = None
    if request.method == 'POST':
        values = {
            'kelembapan': to_int(request.form.get('kelembapan'), 50, 0, 100),
            'cahaya': to_int(request.form.get('cahaya'), 50, 0, 100),
            'suhu': to_int(request.form.get('suhu'), 27, 15, 40),
            'siram': to_int(request.form.get('siram'), 3, 0, 7),
        }
        result = analyze(values, pakar_url=os.getenv('PAKAR_URL', '#'))

    # Tag kategori tetap ditampilkan walaupun hasil belum dihitung.
    current_tags = analyze(values, pakar_url=os.getenv('PAKAR_URL', '#'))['tags']
    return render_template(
        'index.html',
        values=values,
        tags=current_tags,
        result=result,
        pakar_url=os.getenv('PAKAR_URL', '#')
    )

if __name__ == '__main__':
    app.run(debug=True)
