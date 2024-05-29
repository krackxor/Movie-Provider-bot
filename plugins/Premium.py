# y need to change "6695586027" or "767250672" user_id with yr user_id (thx ki jaruRat.. nhi he !!! )

# SPECIAL THANKS TO @ultroidxTeam FOR MODIFYING and 🤔 neverMind...!
# SPECIAL THANKS TO [Rishikesh Sharma] @Rk_botowner FOR THESE AMAZING CODES
# SPECIAL THANKS TO @DeletedFromEarth FOR MODIFYING THESE AMAZING CODES

from datetime import timedelta
import pytz
import datetime, time
from Script import script 
from info import ADMINS, PREMIUM_LOGS
from utils import get_seconds
from database.users_chats_db import db 
from pyrogram import Client, filters 
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("Pengguna berhasil dihapus!")
            if user:
                await client.send_message(
                    chat_id=user_id,
                    teks = f"<b>Halo {user.mention},\n\nAkses premium Anda telah dihapus.\nTerima kasih telah menggunakan layanan kami 😊\nKlik /plan untuk melihat harga vip.</b>"
                )
            else:
                await message.reply_text("Pengguna berhasil dihapus!")
        else:
            await message.reply_text("Tidak dapat menghapus pengguna tersebut! Apakah Anda yakin bahwa dia adalah pengguna premium?")
    else:
        await message.reply_text("Gunakan: /remove_premium user_id") 


@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    user = message.from_user.mention 
    user_id = message.from_user.id
    data = await db.get_user(message.from_user.id)  # Convert the user_id to integer
    if data and data.get("expiry_time"):
        #expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=data)
        expiry = data.get("expiry_time") 
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ Waktu Kedaluwarsa : %I:%M:%S %p")            
        # Calculate time difference
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
            
        # Calculate days, hours, and minutes
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
            
        # Format time left as a string
        time_left_str = f"{days} ᴅᴀʏꜱ, {hours} ʜᴏᴜʀꜱ, {minutes} ᴍɪɴᴜᴛᴇꜱ"
        await message.reply_text(f"⚜️ Data Pengguna Premium :\n\n👤 Pengguna : {user}\n⚡ ID Pengguna : <code>{user_id}</code>\n⏰ Waktu Tersisa : {time_left_str}\n⌛️ Tanggal Kadaluarsa : {expiry_str_in_ist}")   
    else:
       await message.reply_text(f"Halo {user},\n\nKamu tidak memiliki premium yang aktif. Jika kamu ingin mengaktifkan premium, klik tombol di bawah 👇"),
                                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 Beli Premium 💸", callback_data='seeplans')]]))			 

@Client.on_message(filters.command("get_premium") & filters.user(ADMINS))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await db.get_user(user_id)  # Convert the user_id to integer
        if data and data.get("expiry_time"):
            #expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=data)
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ Waktu Kedaluwarsa : %I:%M:%S %p")            
            # Calculate time difference
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            
            # Calculate days, hours, and minutes
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            # Format time left as a string
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
            await message.reply_text(f"⚜️ Data Pengguna Premium :\n\n👤 Pengguna : {user.mention}\n⚡ ID Pengguna : <code>{user_id}</code>\n⏰ Waktu Tersisa : {time_left_str}\n⌛️ Tanggal Kadaluwarsa : {expiry_str_in_ist}")
        else:
            await message.reply_text("Tidak ada data premium yang ditemukan dalam database!")
    else:
        await message.reply_text("Gunakan : /get_premium user_id")

@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ Waktu Bergabung : %I:%M:%S %p") 
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await client.get_users(user_id)
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}  # Using "id" instead of "user_id"  
            await db.update_user(user_data)  # Use the update_user method to update or insert user data
            data = await db.get_user(user_id)
            expiry = data.get("expiry_time")   
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")         
            await message.reply_text(f"Premium ditambahkan dengan sukses ✅\n\n👤 Pengguna : {user.mention}\n⚡ ID Pengguna : <code>{user_id}</code>\n⏰ Akses Premium : <code>{time}</code>\n\n⏳ Tanggal Bergabung : {current_time}\n\n⌛️ Tanggal Kadaluarsa : {expiry_str_in_ist}", disable_web_page_preview=True)
            await client.send_message(
                chat_id=user_id,
                text=f"👋 Hai {user.mention},\nTerima kasih telah membeli langganan premium. Selamat menikmati!! ✨🎉\n\n⏰ Akses Premium: <code>{time}</code>\n⏳ Tanggal Bergabung: {current_time}\n\n⌛️ Tanggal Kadaluarsa: {expiry_str_in_ist}", disable_web_page_preview=True              
            )    
            await client.send_message(PREMIUM_LOGS, text=f"#Tambah_Premium\n\n👤 Pengguna : {user.mention}\n⚡ ID Pengguna : <code>{user_id}</code>\n⏰ Akses Premium : <code>{time}</code>\n\n⏳ Tanggal Bergabung : {current_time}\n\n⌛️ Tanggal Kadaluarsa : {expiry_str_in_ist}", disable_web_page_preview=True)
     
        else:
            await message.reply_text("Format salah. Gunakam '1 day untuk hari', '1 hour untuk jam', or '1 min untuk menit', or '1 month untuk bulan' or '1 year untuk tahun'")
    else:
        await message.reply_text("Gunakan : /add_premium user_id time (e.g., '1 day untuk hari', '1 hour untuk jam', or '1 min untuk menit', or '1 month untuk bulan' or '1 year untuk tahun')")

@Client.on_message(filters.command("premium_users") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("<i>Tunggu sebentar...</i>")
    new = f"⚜️ Daftar Pengguna Premium :\n\n"
    user_count = 1
    users = await db.get_all_users()
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ Waktu Kedaluwarsa : %I:%M:%S %p")            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"	 
            new += f"{user_count}. {(await client.get_users(user['id'])).mention}\n👤 ID Pengguna : {user['id']}\n⏳ Tanggal Kadaluarsa : {expiry_str_in_ist}\n⏰ Waktu Tersisa : {time_left_str}\n"
            user_count += 1
        else:
            pass
    try:    
        await aa.edit_text(new)
    except MessageTooLong:
        with open('usersplan.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('usersplan.txt', caption="Paid Users:")



@Client.on_message(filters.command("plan"))
async def plan(client, message):
    user_id = message.from_user.id 
    users = message.from_user.mention 
    btn = [
        [InlineKeyboardButton("📲 Kirim Bukti TF", user_id=int(6510365486))],
        [InlineKeyboardButton("❌ Tutup ❌", callback_data="close_data")]
    ]
    await message.reply_photo(photo="https://telegra.ph/file/734170f40b8169830d821.jpg", caption=script.PREMIUM_TEXT.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
