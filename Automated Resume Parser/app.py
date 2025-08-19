from flask import Flask, request, jsonify
from models import db, Candidate
from parser import extract_text_from_pdf, extract_info
from config import DATABASE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

@app.route('/')
def home():
    return jsonify({"message": "Resume Parser is running."})

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    text = extract_text_from_pdf(file)
    data = extract_info(text)

    candidate = Candidate(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        education=data['education'],
        skills=data['skills']
    )

    db.session.add(candidate)
    db.session.commit()

    return jsonify({
        "message": "Resume uploaded and parsed successfully!",
        "candidate": {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "skills": candidate.skills,
            "education": candidate.education
        }
    }), 201

@app.route('/search', methods=['GET'])
def search_by_skill():
    skill = request.args.get('skill')
    if not skill:
        return jsonify({'error': 'Skill query param is required'}), 400

    candidates = Candidate.query.filter(Candidate.skills.ilike(f"%{skill}%")).all()

    return jsonify([{
        "name": c.name,
        "email": c.email,
        "phone": c.phone,
        "skills": c.skills,
        "education": c.education
    } for c in candidates])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures tables are created
    app.run(debug=True)






# pip install -r requirements.txt
# python -m spacy download en_core_web_sm


# python app.py




# Upload a resume
# curl -X POST -F "file=@  sample_resume.pdf  " http://localhost:5000/upload

# Search by skill
# curl "http://localhost:5000/search?skill=Python"
