import os
from telebot import TeleBot
import random

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)
import os, json, random, time, threading
import schedule
from telebot import TeleBot

# قراءة التوكن من Render Environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

# ملف حفظ النقاط
SCORES_FILE = "scores.json"

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return {}
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_scores():
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(user_scores, f, ensure_ascii=False, indent=2)

user_scores = load_scores()
subscribed_users = set()

# البيانات
riddles = [
    {"q": "شيء يُكسر إذا تحدثت؟ 🤔", "a": "الصمت"},
    {"q": "ما الشيء الذي يمشي بلا قدمين ويبكي بلا عينين؟ 💧", "a": "السحاب"},
    {"q": "ما الشيء الذي يراك ولا تراه؟ 👁️", "a": "المرآة"},
]
ideas = [
    "خدمة الردود الذكية للمتاجر الصغيرة 🤖",
    "نشرة واتساب لفرص العمل اليومية 📱",
    "قناة تلغرام للاقتباسات التحفيزية 💬",
    "بوت لترشيح أدوات الذكاء المجانية 💡",
]
motivations = [
    "ابدأ يومك بطاقة إيجابية، النجاح ينتظرك اليوم! 💪",
    "تذكّر: كل تحدٍ يقوّيك، لا توقف 💥",
    "اليوم فرصة جديدة لتكتب قصتك بنفسك ✨",
]

@bot.message_handler(commands=['start'])
def start(message):
    subscribed_users.add(message.chat.id)
    bot.send_message(message.chat.id,
        "👋 أهلاً بك في ⚡ *ALVRA Smart Bot – ذكاءك اليومي+*\n\n"
        "اختر أحد الأوامر التالية:\n"
        "🧩 /لغز — لغز اليوم\n"
        "🎁 /فكرة — فكرة مشروع جديدة\n"
        "⭐ /نقاطي — عرض نقاطك الحالية\n"
        "🏆 /الترتيب — أفضل أذكياء الأسبوع\n\n"
        "📬 سيتم إرسال لغز يومي كل صباح 🔔",
        parse_mode="Markdown")

@bot.message_handler(commands=['لغز'])
def send_riddle(message):
    riddle = random.choice(riddles)
    user_scores.setdefault(str(message.chat.id), {"points": 0, "question": None})
    user_scores[str(message.chat.id)]["question"] = riddle
    save_scores()
    bot.send_message(message.chat.id, f"🧠 {riddle['q']}\n\nاكتب إجابتك:")

@bot.message_handler(commands=['فكرة'])
def send_idea(message):
    idea = random.choice(ideas)
    bot.send_message(message.chat.id, f"💡 فكرة اليوم:\n{idea}")

@bot.message_handler(commands=['نقاطي'])
def show_points(message):
    score = user_scores.get(str(message.chat.id), {}).get("points", 0)
    bot.send_message(message.chat.id, f"⭐ نقاطك الحالية: {score}")

@bot.message_handler(commands=['الترتيب'])
def show_top(message):
    if not user_scores:
        bot.send_message(message.chat.id, "لا يوجد ترتيب بعد. ابدأ بحل الألغاز أولاً! 🧩")
        return
    sorted_users = sorted(user_scores.items(), key=lambda x: x[1].get("points", 0), reverse=True)
    top = "\n".join([f"{i+1}. مستخدم {u[0][-4:]} — {u[1]['points']} ⭐" for i, u in enumerate(sorted_users[:5])])
    bot.send_message(message.chat.id, f"🏆 *أذكى المستخدمين الآن:*\n{top}", parse_mode="Markdown")

@bot.message_handler(func=lambda msg: True)
def check_answer(message):
    data = user_scores.get(str(message.chat.id))
    if data and "question" in data and data["question"]:
        correct = data["question"]["a"]
        if correct in message.text:
            data["points"] = data.get("points", 0) + 1
            bot.send_message(message.chat.id, f"✅ إجابة صحيحة! نقاطك الآن {data['points']} ⭐")
        else:
            bot.send_message(message.chat.id, f"❌ خطأ، الإجابة الصحيحة هي: {correct}")
        data["question"] = None
        save_scores()
    else:
        bot.send_message(message.chat.id, "🧩 استخدم /لغز لتبدأ تحديًا جديدًا!")

def send_daily_riddle():
    riddle = random.choice(riddles)
    quote = random.choice(motivations)
    for user_id in subscribed_users:
        bot.send_message(user_id, f"صباح الخير ☀️\n\n{quote}\n\n🧠 لغز اليوم:\n{riddle['q']}")
        user_scores.setdefault(str(user_id), {"points": 0, "question": riddle})
    save_scores()

def run_schedule():
    schedule.every().day.at("10:00").do(send_daily_riddle)
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=run_schedule, daemon=True).start()
bot.polling()
