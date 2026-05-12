import os
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔑 CONFIG
TOKEN = "8675240270:AAFr1QF-oLLcVXAnjniPWIqBhiXjTB9eyqI"
CANAL = "@yesterpreuwba"
OWNER_ID = 7752782654

print("🚀 INICIANDO BOT...")

# 📁 ARCHIVOS
CARPETA = "data"
os.makedirs(CARPETA, exist_ok=True)

DATOS = os.path.join(CARPETA, "datos.json")
ADMINS = os.path.join(CARPETA, "admins.json")
USERS = os.path.join(CARPETA, "users.json")


def load(file):
    try:
        if not os.path.exists(file):
            return {}
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}


def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f)


# 🔐 PERMISOS
def is_owner(uid):
    return uid == OWNER_ID


def is_admin(uid):
    admins = load(ADMINS)
    return str(uid) in admins or is_owner(uid)


def can_refes(uid):
    users = load(USERS)
    return str(uid) in users or is_admin(uid)


# 👤 ADD USER
async def adduser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("Usa: /adduser ID")
        return

    users = load(USERS)
    users[context.args[0]] = True
    save(USERS, users)

    await update.message.reply_text("Usuario agregado")


# 🛡️ ADD ADMIN
async def addadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("Usa: /addadmin ID")
        return

    admins = load(ADMINS)
    admins[context.args[0]] = Trueimport os
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔑 CONFIG
TOKEN = "8675240270:AAFr1QF-oLLcVXAnjniPWIqBhiXjTB9eyqI"
CANAL = "@yesterpreuwba"
OWNER_ID = 7752782654

print("🚀 INICIANDO BOT...")

# 📁 ARCHIVOS
CARPETA = "data"
os.makedirs(CARPETA, exist_ok=True)

DATOS = os.path.join(CARPETA, "datos.json")
ADMINS = os.path.join(CARPETA, "admins.json")
USERS = os.path.join(CARPETA, "users.json")


def load(file):
    try:
        if not os.path.exists(file):
            return {}
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}


def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f)


# 🔐 PERMISOS
def is_owner(uid):
    save(ADMINS, admins)

    await update.message.reply_text("Admin agregado")


# ❌ REMOVE
async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return

    if not context.args:
        return

    uid = context.args[0]

    admins = load(ADMINS)
    users = load(USERS)

    admins.pop(uid, None)
    users.pop(uid, None)

    save(ADMINS, admins)
    save(USERS, users)

    await update.message.reply_text("Eliminado")


# 🔄 RESET
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    save(DATOS, {})
    await update.message.reply_text("Reset hecho")


# 📊 REPORTE
async def reporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if len(context.args) < 3:
        await update.message.reply_text("Usa: /reporte abril 18 22")
        return

    meses = {
        "enero":1,"febrero":2,"marzo":3,"abril":4,
        "mayo":5,"junio":6,"julio":7,"agosto":8,
        "septiembre":9,"octubre":10,"noviembre":11,"diciembre":12
    }

    mes = meses.get(context.args[0].lower())
    if not mes:
        await update.message.reply_text("Mes inválido")
        return

    inicio = int(context.args[1])
    fin = int(context.args[2])

    datos = load(DATOS)
    res = {}

    for uid, info in datos.items():
        for h in info.get("historial", []):
            fecha = datetime.strptime(h["fecha"], "%Y-%m-%d")
            if fecha.month == mes and inicio <= fecha.day <= fin:
                res[uid] = res.get(uid, 0) + 1

    txt = "📊 REPORTE\n\n"
    for uid, n in res.items():
        txt += f"{uid}: {n}\n"

    await update.message.reply_text(txt)


# 🚀 REFES
async def refes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if not msg or not can_refes(msg.from_user.id):
        return

    if not msg.text or not msg.text.lower().startswith(".refes"):
        return

    if not msg.reply_to_message:
        await msg.reply_text("Responde al mensaje")
        return

    original = msg.reply_to_message
    uid = str(msg.from_user.id)

    datos = load(DATOS)
    if uid not in datos:
        datos[uid] = {"count": 0, "historial": []}

    datos[uid]["count"] += 1
    datos[uid]["historial"].append({
        "fecha": datetime.now().strftime("%Y-%m-%d")
    })

    save(DATOS, datos)

    numero = datos[uid]["count"]
    username = msg.from_user.username or msg.from_user.first_name

    # 🔥 FORMATO FINAL (usuario normal + resto mono)
    caption = (
        f"👑 ADMIN AYLES: @{username}\n\n"
        "```\n"
        "🛍️ REFES NUEVO\n\n"
        f"📊 Tus refes: #{numero}\n\n"
        "💬 Descripción:\n"
        "GRACIAS POR ELEGIRNOS\n"
        "VUELVE PRONTO\n"
        "```"
    )

    try:
        await context.bot.copy_message(
            chat_id=CANAL,
            from_chat_id=original.chat_id,
            message_id=original.message_id,
            caption=caption,
            parse_mode="Markdown"
        )
    except Exception as e:
        print("ERROR:", e)


# 🌐 SERVIDOR RENDER
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


def run_web():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


threading.Thread(target=run_web).start()


# ▶️ START
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("adduser", adduser))
app.add_handler(CommandHandler("addadmin", addadmin))
app.add_handler(CommandHandler("remove", remove))
app.add_handler(CommandHandler("reporte", reporte))
app.add_handler(MessageHandler(filters.Regex(r"^\.reset$"), reset))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, refes))

print("✅ BOT LISTO")
app.run_polling()
