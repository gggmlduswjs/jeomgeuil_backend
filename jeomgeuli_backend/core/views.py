
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from .learn_bank import SETS
from .braille import send_keywords

@require_GET
def health(request):
    return JsonResponse({"ok": True})

SESS = {}

@require_POST
@csrf_exempt
def learn_reset(request):
    data = json.loads(request.body.decode() or "{}")
    mode = data.get("mode", "자모")
    SESS[(request.META.get("REMOTE_ADDR"), mode)] = 0
    return JsonResponse({"ok": True, "mode": mode, "idx": 0, "total": len(SETS.get(mode, []))})

@require_GET
def learn_next(request):
    mode = request.GET.get("mode", "자모")
    key = (request.META.get("REMOTE_ADDR"), mode)
    idx = SESS.get(key, 0)
    arr = SETS.get(mode, [])
    if idx >= len(arr):
        return JsonResponse({"done": True, "mode": mode, "total": len(arr)})
    item = arr[idx]
    SESS[key] = idx + 1
    return JsonResponse({"done": False, "mode": mode, "idx": idx, "total": len(arr), "item": item})

@require_POST
@csrf_exempt
def chat_ask(request):
    data = json.loads(request.body.decode() or "{}")
    query = data.get("query","")
    if "뉴스" in query or "news" in query.lower():
        cards = [
            {"title":"경제 성장률 2% 전망","summary":"정부가 올해 성장률을 2%로 전망했습니다."},
            {"title":"물가 안정 대책 발표","summary":"생활 물가 안정화를 위한 대책이 나왔습니다."},
            {"title":"국제 유가 하락","summary":"국제 유가가 소폭 하락했습니다."},
            {"title":"신규 AI 서비스 출시","summary":"새로운 인공지능 서비스가 공개되었습니다."},
            {"title":"국제 스포츠 대회 개막","summary":"오늘 국제 스포츠 대회가 개막했습니다."},
        ]
        answer = "오늘 주요 뉴스를 정리했습니다. 경제 성장률 2% 전망, 물가 안정 대책 발표, 국제 유가 하락, 신규 AI 서비스 출시, 국제 스포츠 대회 개막."
        return JsonResponse({"mode":"news","answer":answer,"cards":cards,"keywords":["경제","물가","정부"]})
    else:
        answer = "데모에서는 간단히 답변합니다. 예: 오늘 뉴스 5개 요약해줘"
        return JsonResponse({"mode":"simple","answer":answer,"keywords":["핵심","요약","정보"]})

@require_POST
@csrf_exempt
def braille_output(request):
    data = json.loads(request.body.decode() or "{}")
    keywords = data.get("keywords", [])
    res = send_keywords(keywords[:3])
    return JsonResponse({"ok": True, "keywords": keywords[:3], "io": res})
