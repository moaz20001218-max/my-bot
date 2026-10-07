import os, telebot
from telebot import types
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 8678898704
bot = telebot.TeleBot(TOKEN)
pending = {}
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "أهلاً! أرسل اسمك الكامل:")
@bot.message_handler(func=lambda m: True)
def handle(m):
    if m.chat.id in pending: return
    if m.text.startswith('/'): return
    pending[m.chat.id]=m.text
    user = f"@{m.from_user.username}" if m.from_user.username else "بدون يوزر"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ موافقة", callback_data=f"ok_{m.chat.id}"), types.InlineKeyboardButton("❌ رفض", callback_data=f"no_{m.chat.id}"))
    bot.send_message(ADMIN_ID, f"طلب جديد:\nالاسم: {m.text}\nاليوزر: {user}\nالايدي: {m.chat.id}", reply_markup=markup)
    bot.send_message(m.chat.id, "تم استلام طلبك، انتظر موافقة الادارة...")
@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    act, uid = c.data.split("_")
    uid=int(uid)
    if act=="ok":
        bot.send_message(uid, "✅ تمت الموافقة عليك!")
        bot.edit_message_text(f"✅ تمت الموافقة على {uid}", c.message.chat.id, c.message.id)
    else:
        bot.send_message(uid, "❌ تم رفض طلبك")
        bot.edit_message_text(f"❌ تم رفض {uid}", c.message.chat.id, c.message.id)
    pending.pop(uid,None)
bot.infinity_polling()
