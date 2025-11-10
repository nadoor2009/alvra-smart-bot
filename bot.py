from telebot import TeleBot
import random

# ضع التوكن هنا من BotFather 👇
bot = TeleBot("YOUR_BOT_TOKEN_HERE")

# قائمة الأسئلة والأجوبة
riddles = [
    {"q": "شيء يُكسر إذا تحدثت؟ 🤔", "a": "الصمت"},
    {"q": "يمشي بلا قدمين ويبكي بلا عينين؟ 💧", "a": "السحاب"},
    {"q": "ما الشيء الذي يراك ولا تراه؟ 👁️", "a": "المرآة"},
]

# قائمة أفكار المشاريع
ideas = [
    "خدمة الردود الذكية للمتاجر الصغيرة 🤖",
    "نشرة واتساب لفرص العمل اليومية 📱",
    "قناة تليجرام للاقتباسات التحفيزية 💬",
    "بوت لترشيح أدوات الذكاء المجانية 💡",
]

# لتخزين النقاط
user_scores = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
    "👋 أهلاً بك في *ALVRA Smart Bot – ذكاءك اليومي ⚡*\n\n"
    "اختر أحد الأوامر التالية:\n"
    "🧠 /لغز  — لغز اليوم\n"
    "🎁 /فكرة  — فكرة مشروع جديدة\n"
    "⭐ /نقاطي — عرض نقاطك الحالية\n\n"
    "استعد لاختبار ذكاءك اليومي! 💪", parse_mode="Markdown")

@bot.message_handler(commands=['لغز'])
def send_riddle(message):
    riddle = random.choice(riddles)
    user_scores[message.chat.id] = {"question": riddle, "points": user_scores.get(message.chat.id, {}).get("points", 0)}
    bot.send_message(message.chat.id, f"🧩 {riddle['q']}\n\nاكتب إجابتك هنا:")

@bot.message_handler(commands=['فكرة'])
def send_idea(message):
    idea = random.choice(ideas)
    bot.send_message(message.chat.id, f"💡 فكرة اليوم:\n{idea}")

@bot.message_handler(commands=['نقاطي'])
def show_points(message):
    score = user_scores.get(message.chat.id, {}).get("points", 0)
    bot.send_message(message.chat.id, f"⭐ نقاطك الحالية: {score}")

@bot.message_handler(func=lambda msg: True)
def check_answer(message):
    data = user_scores.get(message.chat.id)
    if data and "question" in data:
        correct = data["question"]["a"]
        if correct in message.text:
            data["points"] = data.get("points", 0) + 1
            bot.send_message(message.chat.id, f"✅ إجابة صحيحة! زادت نقاطك إلى {data['points']} ⭐")
        else:
            bot.send_message(message.chat.id, f"❌ خطأ! الإجابة الصحيحة هي: {correct}")
        data.pop("question", None)
    else:
        bot.send_message(message.chat.id, "اكتب /لغز لبدء تحدي جديد 🧠")

bot.polling()
