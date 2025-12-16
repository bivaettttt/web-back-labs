from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for
from flask_login import current_user, login_required
import random

lab9 = Blueprint("lab9", __name__, template_folder="templates")

BOX_COUNT = 10
MAX_OPEN = 3

GREETINGS = [
    "С Новым годом! Пусть мечты превращаются в планы, а планы — в результат.",
    "Пусть в новом году будет больше спокойствия, уверенности и сил.",
    "Желаю здоровья, стабильности и приятных сюрпризов каждый месяц.",
    "Пусть учеба и работа идут легко, а отдых приносит настоящее восстановление.",
    "Пусть рядом будут люди, которые поддерживают и вдохновляют.",
    "Желаю финансового роста и грамотных решений в любом деле.",
    "Пусть новые возможности находят тебя быстрее, чем ты их ищешь.",
    "Желаю удачи в начинаниях и смелости доводить все до конца.",
    "Пусть будет меньше стресса, больше радости и понятных целей.",
    "Пусть новый год принесет важные победы — большие и маленькие.",
]

BOX_IMAGES = [
    "lab9/boxes/box1.jpeg",
    "lab9/boxes/box2.jpeg",
    "lab9/boxes/box3.avif",
    "lab9/boxes/box4.jpeg",
    "lab9/boxes/box5.avif",
    "lab9/boxes/box6.png",
    "lab9/boxes/box7.jpeg",
    "lab9/boxes/box8.jpeg",
    "lab9/boxes/box9.jpeg",
    "lab9/boxes/box10.jpeg",
]

GIFT_IMAGES = [
    "lab9/gifts/gift1.webp",
    "lab9/gifts/gift2.jpg",
    "lab9/gifts/gift3.jpeg",
    "lab9/gifts/gift4.png",
    "lab9/gifts/gift5.jpg",
    "lab9/gifts/gift6.webp",
    "lab9/gifts/gift7.avif",
    "lab9/gifts/gift8.webp",
    "lab9/gifts/gift9.webp",
    "lab9/gifts/gift10.jpg",
]

# Какие коробки содержат "подарки только для авторизованных"
# Можно изменить список — главное, чтобы часть подарков была закрыта
AUTH_ONLY_BOXES = {0, 3, 7}  # 3 коробки из 10 только для вошедших


def _generate_positions():
    positions = []
    min_dist = 14
    attempts_limit = 250

    for _ in range(BOX_COUNT):
        placed = False

        for _attempt in range(attempts_limit):
            top = random.randint(5, 75)
            left = random.randint(5, 85)

            ok = True
            for p in positions:
                dt = top - p["top"]
                dl = left - p["left"]
                dist = (dt * dt + dl * dl) ** 0.5
                if dist < min_dist:
                    ok = False
                    break

            if ok:
                positions.append({"top": top, "left": left})
                placed = True
                break

        if not placed:
            positions.append({"top": random.randint(5, 75), "left": random.randint(5, 85)})

    return positions


def _init_lab9_state(force_refill: bool = False, force_positions: bool = False):
    if force_positions or session.get("lab9_positions") is None:
        session["lab9_positions"] = _generate_positions()

    if force_refill or session.get("lab9_assignment") is None:
        greetings = GREETINGS[:]
        gifts = GIFT_IMAGES[:]
        boxes = BOX_IMAGES[:]

        random.shuffle(greetings)
        random.shuffle(gifts)
        random.shuffle(boxes)

        assignment = []
        for i in range(BOX_COUNT):
            assignment.append({
                "greeting": greetings[i],
                "gift": gifts[i],
                "box_img": boxes[i],
                "auth_only": (i in AUTH_ONLY_BOXES),
            })
        session["lab9_assignment"] = assignment

    if force_refill or session.get("lab9_opened") is None:
        session["lab9_opened"] = []  # список id открытых коробок


@lab9.route("/lab9/")
def index():
    _init_lab9_state()
    opened = set(session.get("lab9_opened", []))
    remaining = BOX_COUNT - len(opened)

    return render_template(
        "lab9/index.html",
        positions=session["lab9_positions"],
        assignment=session["lab9_assignment"],
        opened=opened,
        remaining=remaining,
        max_open=MAX_OPEN,
        opened_count=len(opened),
        authorized=current_user.is_authenticated,
    )


@lab9.route("/lab9/api/open", methods=["POST"])
def api_open():
    _init_lab9_state()

    data = request.get_json(silent=True) or {}
    box_id = data.get("id")

    if not isinstance(box_id, int) or not (0 <= box_id < BOX_COUNT):
        return jsonify({"ok": False, "error": "Некорректный id"}), 400

    opened = set(session.get("lab9_opened", []))

    # уже открывали
    if box_id in opened:
        return jsonify({
            "ok": False,
            "reason": "already_opened",
            "message": "Эта коробка уже открыта.",
            "remaining": BOX_COUNT - len(opened),
            "opened_count": len(opened),
            "max_open": MAX_OPEN,
        })

    # лимит 3 открытия
    if len(opened) >= MAX_OPEN:
        return jsonify({
            "ok": False,
            "reason": "limit",
            "message": f"Можно открыть не более {MAX_OPEN} коробок.",
            "remaining": BOX_COUNT - len(opened),
            "opened_count": len(opened),
            "max_open": MAX_OPEN,
        })

    item = session["lab9_assignment"][box_id]

    # подарки только для авторизованных
    if item.get("auth_only") and (not current_user.is_authenticated):
        return jsonify({
            "ok": False,
            "reason": "auth_required",
            "message": "Этот подарок доступен только авторизованным пользователям.",
            "remaining": BOX_COUNT - len(opened),
            "opened_count": len(opened),
            "max_open": MAX_OPEN,
        })

    # открываем
    opened.add(box_id)
    session["lab9_opened"] = list(opened)

    remaining = BOX_COUNT - len(opened)

    return jsonify({
        "ok": True,
        "greeting": item["greeting"],
        "gift": url_for("static", filename=item["gift"]),
        "remaining": remaining,
        "opened_count": len(opened),
        "max_open": MAX_OPEN,
    })


@lab9.route("/lab9/reset", methods=["POST"])
@login_required
def reset():
    _init_lab9_state(force_refill=True, force_positions=True)
    return redirect("/lab9/")