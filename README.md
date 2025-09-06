
# Jeomgeuli Backend

## 실행 방법
```bash
python -m venv .venv
. .venv/Scripts/activate    # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## API 엔드포인트
- GET /api/health
- POST /api/learn/reset {"mode":"자모"}
- GET /api/learn/next?mode=자모
- POST /api/chat/ask {"query":"오늘 뉴스 5개 요약해줘"}
- POST /api/braille/output {"keywords":["경제","물가","정부"]}
# jeomgeuil_backend
