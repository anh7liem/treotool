import multiprocessing
import time
import json
import requests
import random
import os
from rich.text import Text
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.box import DOUBLE
from rich.table import Table
from zlapi import *
from zlapi.models import *
from gtts import gTTS

console = Console()

def console_print(text, style="white"):
    console.print(text, style=style)

def create_login_banner():
    banner = Text(justify="center")
    banner.append("""
╔═╗─╔╗───╔═══╗────────────╔╗─╔╗
║║╚╗║║───║╔═╗║────────────║║─║║
║╔╗╚╝╠══╗║║─║╠╗╔╦══╦═╗╔══╗║╚═╝╠╗╔╦╗─╔╗
║║╚╗║║╔╗║║║─║║║║║╔╗║╔╗╣╔╗║║╔═╗║║║║║─║║
║║─║║║╚╝║║╚═╝║╚╝║╔╗║║║║╚╝║║║─║║╚╝║╚═╝║
╚╝─╚═╩═╗║╚══╗╠══╩╝╚╩╝╚╩═╗║╚╝─╚╩══╩═╗╔╝
─────╔═╝║───╚╝────────╔═╝║───────╔═╝║
─────╚══╝─────────────╚══╝───────╚══╝
""", style="cyan")
    banner.append("\n\n🌟 TOOL ZALO SPAM BY HIEU THANH 🌟\n", style="magenta")
    banner.append("🔐 Tool mien phi - Khong can key\n", style="yellow")
    banner.append("ℹ️ Phiên bản: V8.26\n", style="green")
    banner.append(f"⏰ Thời gian: {time.strftime('%I:%M %p, %d/%m/%Y')}\n", style="green")
    return banner

def create_main_banner():
    banner = Text(justify="center")
    banner.append("""
██╗░░░░░░█████╗░░██████╗░██╗███╗░░██╗
██║░░░░░██╔══██╗██╔════╝░██║████╗░██║
██║░░░░░██║░░██║██║░░██╗░██║██╔██╗██║
██║░░░░░██║░░██║██║░░╚██╗██║██║╚████║
███████╗╚█████╔╝╚██████╔╝██║██║░╚███║
╚══════╝░╚════╝░░╚═════╝░╚═╝╚═╝░░╚══╝

████████╗░█████╗░░█████╗░██╗░░░░░
╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
░░░██║░░░██║░░██║██║░░██║██║░░░░░
░░░██║░░░██║░░██║██║░░██║██║░░░░░
░░░██║░░░╚█████╔╝╚█████╔╝███████╗
░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝
""", style="cyan")
    banner.append("\n🌟 TOOL ZALO SPAM BY HIEU THANH 🌟\n", style="magenta")
    banner.append("👑 Admin: Hieu Thanh\n", style="magenta")
    banner.append("📱 Thông tin liên hệ:\n", style="yellow")
    banner.append("   • Facebook: https://www.facebook.com/hieuthanh\n", style="cyan")
    banner.append("   • Zalo: 0868371089\n", style="cyan")
    banner.append("   • Nhóm Zalo: https://zalo.me/g/hieuthanh\n", style="cyan")
    banner.append("\nℹ️ Phiên bản: V8.26\n", style="green")
    banner.append(f"⏰ Thời gian: {time.strftime('%I:%M %p, %d/%m/%Y')}\n", style="green")
    banner.append("🔄 Cập nhật lần cuối: 15/06/2025\n", style="yellow")
    banner.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", style="cyan")
    banner.append("✅ Tool mien phi - Khong can key\n", style="green")
    banner.append("🚀 Chúc bạn sử dụng tool vui vẻ!\n", style="green")
    banner.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", style="cyan")
    return banner

def create_instructions_panel():
    instructions = Text(justify="left")
    instructions.append("🔹 HƯỚNG DẪN SỬ DỤNG TOOL 🔹\n", style="bold cyan")
    instructions.append("1️⃣ Tool mien phi, khong can key.\n", style="white")
    instructions.append("2️⃣ Nhập số lượng tài khoản Zalo muốn chạy.\n", style="white")
    instructions.append("3️⃣ Nhập IMEI, Cookie cho từng tài khoản.\n", style="white")
    instructions.append("4️⃣ Chọn chế độ: 1 (Nhây Tag), 2 (Treo Ngôn), 3 (Spam Call - Da fix), 4 (Treo Ảnh), 5 (Đổi Tên Nhóm), 6 (Đổi Avatar Nhóm), 7 (Spam Sticker), 8 (Spam Voice), 9 (Spam Danh Thiếp).\n", style="white")
    instructions.append("📌 Chế độ Nhây Tag (1):\n", style="bold cyan")
    instructions.append("   • Chọn delay cố định hoặc random (Y/N).\n", style="white")
    instructions.append("   • Nếu random, nhập khoảng delay min và max.\n", style="white")
    instructions.append("   • Chọn tag nhiều người trong 1 tin nhắn hay từng người (Y/N).\n", style="white")
    instructions.append("   • Chọn réo ngẫu nhiên hay theo thứ tự (Y/N).\n", style="white")
    instructions.append("   • Chọn nhóm và thành viên để tag (VD: 1,3).\n", style="white")
    instructions.append("📌 Chế độ Treo Ngôn (2):\n", style="bold cyan")
    instructions.append("   • Nhập tên file .txt chứa nội dung spam.\n", style="white")
    instructions.append("   • Nhập delay giữa các tin nhắn (giây).\n", style="white")
    instructions.append("   • Chọn nhóm (VD: 1,3).\n", style="white")
    instructions.append("📌 Chế độ Spam Call (3):\n", style="bold red")
    instructions.append("   • Anh Dexry Dặn: Spam call bị da lô nó fix rồi khỏi chọn nữa!\n", style="bold red")
    instructions.append("📌 Chế độ Treo Ảnh (4):\n", style="bold cyan")
    instructions.append("   • Nhập đường dẫn thư mục chứa ảnh.\n", style="white")
    instructions.append("   • Nhập delay giữa các lần gửi (giây).\n", style="white")
    instructions.append("   • Chọn nhóm (VD: 1,3).\n", style="white")
    instructions.append("📌 Chế độ Đổi Tên Nhóm (5):\n", style="bold cyan")
    instructions.append("   • Nhập delay giữa các lần đổi tên (giây).\n", style="white")
    instructions.append("   • Chọn nhóm (VD: 1,3).\n", style="white")
    instructions.append("📌 Chế độ Đổi Avatar Nhóm (6):\n", style="bold cyan")
    instructions.append("   • Nhập đường dẫn thư mục chứa ảnh.\n", style="white")
    instructions.append("   • Nhập số lần đổi avatar.\n", style="white")
    instructions.append("   • Nhập delay giữa các lần đổi (giây).\n", style="white")
    instructions.append("   • Chọn nhóm (VD: 1,3).\n", style="white")
    instructions.append("📌 Chế độ Spam Sticker (7):\n", style="bold cyan")
    instructions.append("   • Nhập số lượng sticker muốn spam.\n", style="white")
    instructions.append("   • Nhập delay giữa các lần gửi (giây).\n", style="white")
    instructions.append("   • Chọn nhóm (VD: 1,3).\n", style="white")
    instructions.append("📌 Chế độ Spam Voice (8):\n", style="bold cyan")
    instructions.append("   • Nhập delay giữa các lần gửi (giây).\n", style="white")
    instructions.append("   • Chọn nhóm (VD: 1,3).\n", style="white")
    instructions.append("📌 Chế độ Spam Danh Thiếp (9):\n", style="bold cyan")
    instructions.append("   • Nhập delay giữa các lần gửi (giây).\n", style="white")
    instructions.append("   • Chọn nhóm và thành viên để spam danh thiếp (VD: 1,2,3).\n", style="white")
    instructions.append("✅ Bot sẽ tự động chạy theo chế độ đã chọn.\n", style="bold green")
    instructions.append("⚠️ Lưu ý: Đảm bảo file nhaychet.txt, file .txt, thư mục ảnh, và cookie hợp lệ!\n", style="bold yellow")
    return Panel(instructions, title="Hướng Dẫn Sử Dụng", border_style="green", box=DOUBLE, width=60, padding=(0, 1))

def login_screen():
    console.clear()
    console.print(Panel(create_login_banner(), title="Tool Zalo Hieu Thanh", border_style="cyan", box=DOUBLE, width=60, padding=(0, 1)))
    console_print("[✅] Tool mien phi - Khong can key xac thuc!", style="bold green")
    time.sleep(1)
    return True

def read_file_content(filename, mode="lines"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            if mode == "lines":
                return [line.strip() for line in file if line.strip()]
            else:
                return file.read().strip()
    except Exception as e:
        console_print(f"[❌] Lỗi đọc file {filename}: {e}", style="bold red")
        return "" if mode == "text" else []

def parse_selection(input_str, max_index):
    try:
        numbers = [int(i.strip()) for i in input_str.split(',')]
        return [n for n in numbers if 1 <= n <= max_index]
    except:
        console_print("[❌] Định dạng không hợp lệ!", style="bold red")
        return []

def get_random_image_from_folder(folder):
    image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        return None
    return os.path.join(folder, random.choice(image_files))

def convert_text_to_mp3(text):
    try:
        tts = gTTS(text=text, lang='vi')
        mp3_file = 'voice.mp3'
        tts.save(mp3_file)
        return mp3_file
    except Exception as e:
        console_print(f"[❌] Lỗi chuyển đổi text thành voice: {e}", style="bold red")
        return None

def upload_to_host(file_name):
    try:
        with open(file_name, 'rb') as file:
            files = {'files[]': file}
            response = requests.post('https://uguu.se/upload', files=files).json()
            if response['success']:
                return response['files'][0]['url']
        return False
    except Exception as e:
        console_print(f"[❌] Lỗi upload file: {e}", style="bold red")
        return False

class Bot(ZaloAPI):
    def __init__(self, api_key, secret_key, imei, session_cookies, mode="nhaytag", delay_min=0, delay_max=None, tag_multiple=False, tag_random=False, message_text="", repeat_count=0, image_folder="", sticker_count=0, tagged_users=None):
        super().__init__(api_key, secret_key, imei, session_cookies)
        self.mode = mode
        self.delay_min = delay_min
        self.delay_max = delay_max if delay_max is not None else delay_min
        self.tag_multiple = tag_multiple
        self.tag_random = tag_random
        self.message_text = message_text
        self.repeat_count = repeat_count
        self.image_folder = image_folder
        self.sticker_count = sticker_count
        self.tagged_users = tagged_users or {}
        self.message_lines = read_file_content("nhaychet.txt", mode="lines") if mode in ["nhaytag", "doitennhom", "spamvoice", "spamcard"] else []
        self.call_delay = 0.5 if mode == "spamcall" else 0
        self.running_flags = {}
        self.processes = {}
        self.image_index = {}
        self.tagged_users_internal = {}

    def start_spam(self, thread_id, thread_type, tagged_users=None):
        if self.mode == "nhaytag" and not self.message_lines:
            console_print("[❌] File nhaychet.txt rỗng hoặc không đọc được!", style="bold red")
            return
        if self.mode == "treongon" and not self.message_text:
            console_print("[❌] Nội dung spam rỗng!", style="bold red")
            return
        if self.mode == "spamcall":
            console_print("[⚠️] Anh Dexry Dặn: Spam call bị da lô nó fix rồi khỏi chọn nữa!", style="bold red")
            return
        if self.mode == "treoanh" and not os.path.isdir(self.image_folder):
            console_print(f"[❌] Thư mục ảnh {self.image_folder} không tồn tại!", style="bold red")
            return
        if self.mode in ["doitennhom", "spamvoice", "spamcard"] and not self.message_lines:
            console_print("[❌] File nhaychet.txt rỗng hoặc không đọc được!", style="bold red")
            return
        if self.mode == "doianhnhom" and not os.path.isdir(self.image_folder):
            console_print(f"[❌] Thư mục ảnh {self.image_folder} không tồn tại!", style="bold red")
            return
        if self.mode == "spamsticker" and self.sticker_count <= 0:
            console_print("[❌] Số lượng sticker phải lớn hơn 0!", style="bold red")
            return
        if self.mode == "spamcard" and not self.tagged_users.get(thread_id):
            console_print("[❌] Không có thành viên nào để spam danh thiếp!", style="bold red")
            return
        if thread_id not in self.running_flags:
            self.running_flags[thread_id] = multiprocessing.Value('b', False)
        if thread_id not in self.processes:
            self.processes[thread_id] = None
        if thread_id not in self.image_index:
            self.image_index[thread_id] = 0
        if thread_id not in self.tagged_users_internal:
            self.tagged_users_internal[thread_id] = tagged_users or []
        if not self.running_flags[thread_id].value:
            initial_message = """
Bot By: Hieu Thanh
Link facebook: https://www.facebook.com/hieuthanh
Zalo: 0868371089
Link zalo bot: https://zalo.me/g/hieuthanh
Chúc các bạn {} vui vẻ""".format(
                "nhây tag vui vẻ" if self.mode == "nhaytag" else
                "treo ngôn vui vẻ" if self.mode == "treongon" else
                "spam call vui vẻ" if self.mode == "spamcall" else
                "treo ảnh vui vẻ" if self.mode == "treoanh" else
                "đổi tên nhóm vui vẻ" if self.mode == "doitennhom" else
                "đổi avatar nhóm vui vẻ" if self.mode == "doianhnhom" else
                "spam sticker vui vẻ" if self.mode == "spamsticker" else
                "spam voice vui vẻ" if self.mode == "spamvoice" else
                "spam danh thiếp vui vẻ"
            )
            self.send(Message(text=initial_message), thread_id, thread_type, ttl=60000)
            self.running_flags[thread_id].value = True
            if self.mode == "nhaytag":
                self.processes[thread_id] = multiprocessing.Process(
                    target=self.spam_messages_with_tag,
                    args=(thread_id, thread_type, self.running_flags[thread_id])
                )
            elif self.mode == "treongon":
                self.processes[thread_id] = multiprocessing.Process(
                    target=self.spam_messages_treongon,
                    args=(thread_id, thread_type, self.running_flags[thread_id])
                )
            elif self.mode == "spamcall":
                self.processes[thread_id] = None
            elif self.mode == "treoanh":
                self.processes[thread_id] = multiprocessing.Process(
                    target=self.spam_images,
                    args=(thread_id, thread_type, self.running_flags[thread_id])
                )
            elif self.mode == "doitennhom":
                self.processes[thread_id] = multiprocessing.Process(
                    target=self.change_group_name,
                    args=(thread_id, thread_type, self.running_flags[thread_id])
                )
            elif self.mode == "doianhnhom":
                self.processes[thread_id] = multiprocessing.Process(
                    target=self.change_group_avatar,
                    args=(thread_id, thread_type, self.running_flags[thread_id])
                )
            elif self.mode == "spamsticker":
                self.processes[thread_id] = multiprocessing.Process(
                    target=self.spam_sticker,
                    args=(thread_id, thread_type, self.running_flags[thread_id])
                )
            elif self.mode == "spamvoice":
                self.processes[thread_id] = multiprocessing.Process(
                    target=self.spam_voice,
                    args=(thread_id, thread_type, self.running_flags[thread_id])
                )
            else:
                self.processes[thread_id] = multiprocessing.Process(
                    target=self.spam_card,
                    args=(thread_id, thread_type, self.running_flags[thread_id])
                )
            if self.processes[thread_id]:
                self.processes[thread_id].start()

    def spam_messages_with_tag(self, thread_id, thread_type, running_flag):
        user_index = 0
        while running_flag.value and (not self.tagged_users_internal[thread_id] or self.tagged_users_internal[thread_id]):
            if not self.message_lines:
                self.message_lines = read_file_content("nhaychet.txt", mode="lines")
                if not self.message_lines:
                    console_print("[❌] File nhaychet.txt rỗng!", style="bold red")
                    running_flag.value = False
                    break
            raw_msg = random.choice(self.message_lines)
            if self.tag_multiple:
                valid_users = []
                mention_names = []
                users_to_tag = self.tagged_users_internal[thread_id].copy()
                if self.tag_random:
                    random.shuffle(users_to_tag)
                for user_id in users_to_tag:
                    try:
                        user_info = self.fetchUserInfo(user_id)
                        if not user_info or user_id not in user_info.changed_profiles:
                            console_print(f"[⚠️] Thành viên {user_id} không còn trong nhóm, loại bỏ!", style="bold yellow")
                            continue
                        user_name = user_info.changed_profiles[user_id]['displayName']
                        valid_users.append(user_id)
                        mention_names.append(user_name)
                    except Exception as e:
                        console_print(f"[⚠️] Lỗi lấy thông tin user {user_id}: {e}", style="bold yellow")
                        continue
                self.tagged_users_internal[thread_id] = valid_users
                if not self.tagged_users_internal[thread_id]:
                    console_print("[🛑] Không còn thành viên để tag, dừng bot!", style="bold red")
                    running_flag.value = False
                    break
                msg = raw_msg + " "
                mentions = []
                for user_name in mention_names:
                    msg += "@Member "
                final_msg = msg
                for i, user_name in enumerate(mention_names):
                    placeholder = "@Member "
                    final_msg = final_msg.replace(placeholder, f"@{user_name} ", 1)
                    offset = final_msg.find(f"@{user_name}")
                    mentions.append(Mention(valid_users[i], length=len(f"@{user_name}"), offset=offset, auto_format=False))
                try:
                    self.setTyping(thread_id, thread_type)
                    time.sleep(4)
                    message_to_send = Message(text=final_msg.strip(), mention=MultiMention(mentions))
                    self.send(message_to_send, thread_id=thread_id, thread_type=thread_type)
                    console_print(f"[✅] Đã gửi tin nhắn tới nhóm {thread_id}: {final_msg[:30]}...", style="bold green")
                except Exception as e:
                    console_print(f"[❌] Lỗi gửi tin nhắn: {e}", style="bold red")
                    time.sleep(3)
                    continue
            else:
                if self.tag_random:
                    user_id = random.choice(self.tagged_users_internal[thread_id])
                else:
                    user_id = self.tagged_users_internal[thread_id][user_index]
                try:
                    user_info = self.fetchUserInfo(user_id)
                    if not user_info or user_id not in user_info.changed_profiles:
                        console_print(f"[⚠️] Thành viên {user_id} không còn trong nhóm, loại bỏ!", style="bold yellow")
                        self.tagged_users_internal[thread_id].remove(user_id)
                        if not self.tagged_users_internal[thread_id]:
                            console_print("[🛑] Không còn thành viên để tag, dừng bot!", style="bold red")
                            running_flag.value = False
                            break
                        continue
                    user_name = user_info.changed_profiles[user_id]['displayName']
                    msg = f"{raw_msg} @{user_name}"
                    offset_mention = len(raw_msg) + 1
                    mention = Mention(user_id, offset=offset_mention, length=len(f"@{user_name}"))
                    self.setTyping(thread_id, thread_type)
                    time.sleep(4)
                    self.send(Message(text=msg, mention=mention), thread_id, thread_type)
                    console_print(f"[✅] Đã gửi tin nhắn tới nhóm {thread_id}: {msg[:30]}...", style="bold green")
                except Exception as e:
                    console_print(f"[❌] Lỗi gửi tin nhắn: {e}", style="bold red")
                    time.sleep(3)
                    continue
                if not self.tag_random:
                    user_index = (user_index + 1) % len(self.tagged_users_internal[thread_id])
            delay = random.uniform(self.delay_min, self.delay_max)
            console_print(f"[⏳] Delay {delay:.2f} giây trước tin nhắn tiếp theo", style="bold blue")
            time.sleep(delay)

    def spam_messages_treongon(self, thread_id, thread_type, running_flag):
        while running_flag.value:
            mention = Mention("-1", length=len(self.message_text), offset=0)
            try:
                self.setTyping(thread_id, thread_type)
                time.sleep(4)
                self.send(Message(text=self.message_text, mention=mention), thread_id, thread_type)
                console_print(f"[✅ Hieu Thanh] Đã gửi tin nhắn tới nhóm {thread_id}!", style="bold green")
            except Exception as e:
                console_print(f"[❌] Lỗi gửi tin nhắn: {e}", style="bold red")
            time.sleep(self.delay_min)

    def spam_images(self, thread_id, thread_type, running_flag):
        image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not image_files:
            console_print("[⚠️] Không tìm thấy ảnh trong thư mục!", style="bold yellow")
            running_flag.value = False
            return
        while running_flag.value:
            try:
                image_path = os.path.join(self.image_folder, image_files[self.image_index[thread_id]])
                self.setTyping(thread_id, thread_type)
                time.sleep(4)
                self.sendLocalImage(
                    thread_id=thread_id,
                    thread_type=thread_type,
                    message=Message(text=""),
                    imagePath=image_path,
                    width=1920,
                    height=1080
                )
                console_print(f"[✅] Đã gửi ảnh: {image_path}", style="bold green")
                self.image_index[thread_id] = (self.image_index[thread_id] + 1) % len(image_files)
                time.sleep(self.delay_min)
            except Exception as e:
                console_print(f"[❌] Lỗi gửi ảnh: {e}", style="bold red")
                time.sleep(3)

    def change_group_name(self, thread_id, thread_type, running_flag):
        while running_flag.value:
            for content in self.message_lines:
                if not running_flag.value:
                    break
                try:
                    self.changeGroupName(content.strip(), thread_id)
                    console_print(f"[✅] Đã đổi tên nhóm thành: {content.strip()}", style="bold green")
                    time.sleep(self.delay_min)
                except Exception as e:
                    console_print(f"[❌] Lỗi đổi tên nhóm: {e}", style="bold red")
                    time.sleep(3)

    def change_group_avatar(self, thread_id, thread_type, running_flag):
        for _ in range(self.repeat_count):
            if not running_flag.value:
                break
            try:
                image_path = get_random_image_from_folder(self.image_folder)
                if not image_path:
                    console_print("[⚠️] Không tìm thấy ảnh trong thư mục!", style="bold yellow")
                    running_flag.value = False
                    break
                self.changeGroupAvatar(groupId=thread_id, filePath=image_path)
                console_print(f"[✅] Đã đổi ảnh đại diện nhóm: {image_path}", style="bold green")
                time.sleep(self.delay_min)
            except Exception as e:
                console_print(f"[❌] Lỗi đổi ảnh đại diện: {e}", style="bold red")
                time.sleep(3)
        console_print(f"[✅] Hoàn thành đổi ảnh đại diện {self.repeat_count} lần!", style="bold green")
        running_flag.value = False

    def spam_sticker(self, thread_id, thread_type, running_flag):
        sticker_type = 3
        sticker_id = "23339"
        category_id = "10425"
        for _ in range(self.sticker_count):
            if not running_flag.value:
                break
            try:
                response = self.sendSticker(sticker_type, sticker_id, category_id, thread_id, thread_type)
                if not response:
                    console_print("[⚠️] Không thể gửi sticker!", style="bold yellow")
                    time.sleep(3)
                    continue
                console_print("[✅] Đã gửi một sticker!", style="bold green")
                time.sleep(self.delay_min)
            except Exception as e:
                console_print(f"[❌] Lỗi gửi sticker: {e}", style="bold red")
                time.sleep(3)
        console_print("[✅] Hoàn thành spam sticker!", style="bold green")
        running_flag.value = False

    def spam_voice(self, thread_id, thread_type, running_flag):
        while running_flag.value:
            for message in self.message_lines:
                if not running_flag.value:
                    break
                try:
                    self.setTyping(thread_id, thread_type)
                    time.sleep(4)
                    mp3_file = convert_text_to_mp3(message)
                    if mp3_file:
                        voice_url = upload_to_host(mp3_file)
                        if voice_url:
                            file_size = os.path.getsize(mp3_file)
                            self.sendRemoteVoice(voice_url, thread_id, fileSize=file_size, thread_type=thread_type)
                            console_print(f"[✅] Đã gửi voice: {message[:30]}...", style="bold green")
                        else:
                            console_print("[⚠️] Lỗi upload voice!", style="bold yellow")
                    else:
                        console_print("[⚠️] Lỗi tạo voice!", style="bold yellow")
                    time.sleep(self.delay_min)
                except Exception as e:
                    console_print(f"[❌] Lỗi gửi voice: {e}", style="bold red")
                    time.sleep(3)

    def spam_card(self, thread_id, thread_type, running_flag):
        while running_flag.value:
            for user_id in self.tagged_users.get(thread_id, []):
                if not running_flag.value:
                    break
                for content in self.message_lines:
                    if not running_flag.value:
                        break
                    try:
                        self.setTyping(thread_id, thread_type)
                        time.sleep(4)
                        user_info = self.fetchUserInfo(user_id).changed_profiles.get(user_id)
                        avatar_url = user_info.get('avatar') if user_info else None
                        if not avatar_url:
                            console_print(f"[❌] Không tìm thấy ảnh đại diện của user {user_id}!", style="bold red")
                            continue
                        self.sendBusinessCard(
                            userId=user_id,
                            phone=content.strip(),
                            qrCodeUrl=avatar_url,
                            thread_id=thread_id,
                            thread_type=thread_type
                        )
                        console_print(f"[✅] Đã gửi danh thiếp: {content[:30]}...", style="bold green")
                        time.sleep(self.delay_min)
                    except Exception as e:
                        console_print(f"[❌] Lỗi gửi danh thiếp: {e}", style="bold red")
                        time.sleep(3)

    def onMessage(self, *args, **kwargs):
        pass

    def onEvent(self, *args, **kwargs):
        pass

    def onAdminMessage(self, *args, **kwargs):
        pass

    def fetch_groups(self):
        try:
            all_groups = self.fetchAllGroups()
            group_list = []
            for group_id, _ in all_groups.gridVerMap.items():
                group_info = self.fetchGroupInfo(group_id)
                group_name = group_info.gridInfoMap[group_id]["name"]
                group_list.append({
                    'id': group_id,
                    'name': group_name
                })
            return type('GroupObj', (), {'groups': [type('GroupItem', (), {'grid': g['id'], 'name': g['name']})() for g in group_list]})()
        except AttributeError as e:
            console_print(f"[❌] Lỗi: Phương thức hoặc thuộc tính không tồn tại: {e}", style="bold red")
            return None
        except ZaloAPIException as e:
            console_print(f"[❌] Lỗi API Zalo: {e}", style="bold red")
            return None
        except Exception as e:
            console_print(f"[❌] Lỗi không xác định khi lấy danh sách nhóm: {e}", style="bold red")
            return None

    def fetchGroupInfo(self, group_id):
        try:
            return super().fetchGroupInfo(group_id)
        except ZaloAPIException as e:
            console_print(f"[❌] Lỗi API Zalo khi lấy thông tin nhóm {group_id}: {e}", style="bold red")
            return None
        except Exception as e:
            console_print(f"[❌] Lỗi khi lấy thông tin nhóm {group_id}: {e}", style="bold red")
            return None

    def fetchGroupMembers(self, group_id):
        try:
            group_info = self.fetchGroupInfo(group_id)
            if not group_info or not hasattr(group_info, 'gridInfoMap') or group_id not in group_info.gridInfoMap:
                console_print(f"[❌] Không lấy được thông tin nhóm {group_id}", style="bold red")
                return []
            mem_ver_list = group_info.gridInfoMap[group_id]["memVerList"]
            member_ids = [mem.split("_")[0] for mem in mem_ver_list]
            members = []
            for user_id in member_ids:
                try:
                    user_info = self.fetchUserInfo(user_id)
                    user_data = user_info.changed_profiles[user_id]
                    members.append({
                        'id': user_data['userId'],
                        'name': user_data['displayName']
                    })
                except Exception as e:
                    console_print(f"[⚠️] Lỗi lấy thông tin user {user_id}: {e}", style="bold yellow")
                    members.append({
                        'id': user_id,
                        'name': f"[Lỗi: {user_id}]"
                    })
            return members
        except Exception as e:
            console_print(f"[❌] Lỗi lấy danh sách thành viên: {e}", style="bold red")
            return []

def start_bot_nhaytag(api_key, secret_key, imei, session_cookies, delay_min, delay_max, tag_multiple, tag_random, group_ids, tagged_users):
    bot = Bot(api_key, secret_key, imei, session_cookies, mode="nhaytag", delay_min=delay_min, delay_max=delay_max, tag_multiple=tag_multiple, tag_random=tag_random, tagged_users=tagged_users)
    for group_id in group_ids:
        console_print(f"[▶️] Bắt đầu nhây tag nhóm {group_id}", style="bold cyan")
        bot.start_spam(group_id, ThreadType.GROUP, tagged_users.get(group_id, []))
    bot.listen(run_forever=True, thread=False, delay=1, type='requests')

def start_bot_treongon(api_key, secret_key, imei, session_cookies, message_text, delay, group_ids):
    bot = Bot(api_key, secret_key, imei, session_cookies, mode="treongon", delay_min=delay, message_text=message_text)
    for group_id in group_ids:
        console_print(f"[▶️] Bắt đầu treo ngôn nhóm {group_id}", style="bold cyan")
        bot.start_spam(group_id, ThreadType.GROUP)
    bot.listen(run_forever=True, thread=False, delay=1, type='requests')

def start_bot_spamcall(api_key, secret_key, imei, session_cookies, group_ids, tagged_users, repeat_count):
    console_print("[⚠️] Anh Dexry Dặn: Spam call bị da lô nó fix rồi khỏi chọn nữa!", style="bold red")
    return

def start_bot_treoanh(api_key, secret_key, imei, session_cookies, image_folder, delay, group_ids):
    bot = Bot(api_key, secret_key, imei, session_cookies, mode="treoanh", delay_min=delay, image_folder=image_folder)
    for group_id in group_ids:
        console_print(f"[▶️] Bắt đầu treo ảnh nhóm {group_id}", style="bold cyan")
        bot.start_spam(group_id, ThreadType.GROUP)
    bot.listen(run_forever=True, thread=False, delay=1, type='requests')

def start_bot_doitennhom(api_key, secret_key, imei, session_cookies, delay, group_ids):
    bot = Bot(api_key, secret_key, imei, session_cookies, mode="doitennhom", delay_min=delay)
    for group_id in group_ids:
        console_print(f"[▶️] Bắt đầu đổi tên nhóm {group_id}", style="bold cyan")
        bot.start_spam(group_id, ThreadType.GROUP)
    bot.listen(run_forever=True, thread=False, delay=1, type='requests')

def start_bot_doianhnhom(api_key, secret_key, imei, session_cookies, image_folder, repeat_count, delay, group_ids):
    bot = Bot(api_key, secret_key, imei, session_cookies, mode="doianhnhom", image_folder=image_folder, repeat_count=repeat_count, delay_min=delay)
    for group_id in group_ids:
        console_print(f"[▶️] Bắt đầu đổi avatar nhóm {group_id}", style="bold cyan")
        bot.start_spam(group_id, ThreadType.GROUP)
    bot.listen(run_forever=True, thread=False, delay=1, type='requests')

def start_bot_spamsticker(api_key, secret_key, imei, session_cookies, sticker_count, delay, group_ids):
    bot = Bot(api_key, secret_key, imei, session_cookies, mode="spamsticker", sticker_count=sticker_count, delay_min=delay)
    for group_id in group_ids:
        console_print(f"[▶️] Bắt đầu spam sticker nhóm {group_id}", style="bold cyan")
        bot.start_spam(group_id, ThreadType.GROUP)
    bot.listen(run_forever=True, thread=False, delay=1, type='requests')

def start_bot_spamvoice(api_key, secret_key, imei, session_cookies, delay, group_ids):
    bot = Bot(api_key, secret_key, imei, session_cookies, mode="spamvoice", delay_min=delay)
    for group_id in group_ids:
        console_print(f"[▶️] Bắt đầu spam voice nhóm {group_id}", style="bold cyan")
        bot.start_spam(group_id, ThreadType.GROUP)
    bot.listen(run_forever=True, thread=False, delay=1, type='requests')

def start_bot_spamcard(api_key, secret_key, imei, session_cookies, delay, group_ids, tagged_users):
    bot = Bot(api_key, secret_key, imei, session_cookies, mode="spamcard", delay_min=delay, tagged_users=tagged_users)
    for group_id in group_ids:
        console_print(f"[▶️] Bắt đầu spam danh thiếp nhóm {group_id}", style="bold cyan")
        bot.start_spam(group_id, ThreadType.GROUP)
    bot.listen(run_forever=True, thread=False, delay=1, type='requests')

def start_multiple_accounts():
    console.clear()
    console.print(Panel(create_main_banner(), title="Tool Zalo Spam Hieu Thanh", border_style="cyan", box=DOUBLE, width=60, padding=(0, 1)))
    console.print(create_instructions_panel())
    try:
        num_accounts = int(Prompt.ask("[💠] Nhập số lượng tài khoản Zalo muốn chạy", default="1"))
    except ValueError:
        console_print("[❌] Nhập sai, phải là số nguyên!", style="bold red")
        return
    processes = []
    for i in range(num_accounts):
        console.print(f"\n[🔹] Nhập thông tin cho tài khoản {i+1} [🔹]", style="bold cyan")
        try:
            imei = Prompt.ask("[📱] Nhập IMEI của Zalo")
            cookie_str = Prompt.ask("[🍪] Nhập Cookie")
            try:
                session_cookies = eval(cookie_str)
                if not isinstance(session_cookies, dict):
                    console_print("[❌] Cookie phải là dictionary!", style="bold red")
                    continue
            except:
                console_print("[❌] Cookie không hợp lệ, dùng dạng {'key': 'value'}!", style="bold red")
                continue
            while True:
                mode = Prompt.ask("[🎮] Chọn chế độ: 1 (Nhây Tag), 2 (Treo Ngôn), 3 (Spam Call - Da fix), 4 (Treo Ảnh), 5 (Đổi Tên Nhóm), 6 (Đổi Avatar Nhóm), 7 (Spam Sticker), 8 (Spam Voice), 9 (Spam Danh Thiếp)", default="1")
                if mode in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    if mode == '3':
                        console_print("[⚠️] Anh Dexry Dặn: Spam call bị da lô nó fix rồi khỏi chọn nữa!", style="bold red")
                        continue
                    break
                console_print("[❌] Vui lòng nhập 1, 2, 3, 4, 5, 6, 7, 8 hoặc 9!", style="bold red")
            bot = Bot('api_key', 'secret_key', imei, session_cookies, mode="nhaytag" if mode == '1' else "treongon" if mode == '2' else "spamcall" if mode == '3' else "treoanh" if mode == '4' else "doitennhom" if mode == '5' else "doianhnhom" if mode == '6' else "spamsticker" if mode == '7' else "spamvoice" if mode == '8' else "spamcard")
            groups = bot.fetch_groups()
            if not groups or not hasattr(groups, 'groups') or not groups.groups:
                console_print("[⚠️] Không lấy được nhóm nào!", style="bold red")
                continue
            table = Table(show_header=True, header_style="bold cyan", show_lines=False, box=None)
            table.add_column("STT", width=5, justify="center", style="white")
            table.add_column("Tên nhóm", width=25, justify="left", style="bold green")
            table.add_column("ID nhóm", width=15, justify="left", style="cyan")
            for idx, group in enumerate(groups.groups, 1):
                table.add_row(str(idx), group.name, str(group.grid))
            console.print(Panel(table, title="[bold cyan]📋 Danh sách nhóm[/bold cyan]", border_style="bold cyan", width=60, padding=(0, 1)))
            raw = Prompt.ask("[🔸] Nhập số nhóm muốn chạy (VD: 1,3)", default="")
            selected = parse_selection(raw, len(groups.groups))
            if not selected:
                console_print("[⚠️] Không chọn nhóm nào!", style="bold red")
                continue
            selected_ids = [groups.groups[i - 1].grid for i in selected]
            if mode == '1':
                delay_type = Prompt.ask("[⏳] Delay cố định hay random? (Y/N)", default="N").lower()
                if delay_type == 'y':
                    while True:
                        try:
                            delay_min = float(Prompt.ask("[⏳] Nhập delay ít nhất (giây)", default="0"))
                            if delay_min < 0:
                                console_print("[❌] Delay min phải không âm!", style="bold red")
                                continue
                            break
                        except ValueError:
                            console_print("[❌] Delay min phải là số!", style="bold red")
                    while True:
                        try:
                            delay_max = float(Prompt.ask("[⏳] Nhập delay nhiều nhất (giây)", default="5"))
                            if delay_max < delay_min:
                                console_print("[❌] Delay max phải lớn hơn hoặc bằng delay min!", style="bold red")
                                continue
                            break
                        except ValueError:
                            console_print("[❌] Delay max phải là số!", style="bold red")
                else:
                    while True:
                        try:
                            delay_min = float(Prompt.ask("[⏳] Nhập delay cố định (giây)", default="5"))
                            if delay_min < 0:
                                console_print("[❌] Delay phải không âm!", style="bold red")
                                continue
                            break
                        except ValueError:
                            console_print("[❌] Delay phải là số!", style="bold red")
                    delay_max = delay_min
                tag_multiple = Prompt.ask("[🏷] Tag nhiều người trong 1 tin nhắn hay từng người? (Y/N)", default="Y").lower() == 'y'
                tag_random = Prompt.ask("[🔀] Réo ngẫu nhiên hay theo thứ tự? (Y/N)", default="N").lower() == 'y'
                tagged_users = {}
                for group_id in selected_ids:
                    members = bot.fetchGroupMembers(group_id)
                    if not members:
                        console_print(f"[⚠️] Nhóm {group_id} không có thành viên!", style="bold red")
                        continue
                    table = Table(show_header=True, header_style="bold cyan", show_lines=False, box=None)
                    table.add_column("STT", width=5, justify="center", style="white")
                    table.add_column("Tên thành viên", width=25, justify="left", style="bold green")
                    table.add_column("ID", width=15, justify="left", style="cyan")
                    for idx, member in enumerate(members, 1):
                        table.add_row(str(idx), member['name'], member['id'])
                    console.print(Panel(table, title=f"[bold cyan]📋 Thành viên nhóm {group_id}[/bold cyan]", border_style="bold cyan", width=60, padding=(0, 1)))
                    raw = Prompt.ask("[🔸] Nhập số thứ tự thành viên để tag (VD: 1,2,3, 0 để không tag)", default="0")
                    if raw.strip() == "0":
                        tagged_users[group_id] = []
                    else:
                        selected_members = parse_selection(raw, len(members))
                        tagged_users[group_id] = [members[i - 1]['id'] for i in selected_members]
                p = multiprocessing.Process(
                    target=start_bot_nhaytag,
                    args=('api_key', 'secret_key', imei, session_cookies, delay_min, delay_max, tag_multiple, tag_random, selected_ids, tagged_users)
                )
            elif mode == '2':
                file_txt = Prompt.ask("[📂] Nhập tên file .txt chứa nội dung spam")
                message_text = read_file_content(file_txt, mode="text")
                if not message_text:
                    console_print("[⚠️] File rỗng hoặc không đọc được!", style="bold red")
                    continue
                while True:
                    try:
                        delay = float(Prompt.ask("[⏳] Nhập delay giữa các lần gửi (giây)", default="5"))
                        if delay < 0:
                            console_print("[❌] Delay phải không âm!", style="bold red")
                            continue
                        break
                    except ValueError:
                        console_print("[❌] Delay phải là số!", style="bold red")
                p = multiprocessing.Process(
                    target=start_bot_treongon,
                    args=('api_key', 'secret_key', imei, session_cookies, message_text, delay, selected_ids)
                )
            elif mode == '3':
                console_print("[⚠️] Anh Dexry Dặn: Spam call bị da lô nó fix rồi khỏi chọn nữa!", style="bold red")
                continue
            elif mode == '4':
                image_folder = Prompt.ask("[📁] Nhập đường dẫn thư mục chứa ảnh")
                if not os.path.isdir(image_folder):
                    console_print("[❌] Thư mục không tồn tại!", style="bold red")
                    continue
                while True:
                    try:
                        delay = float(Prompt.ask("[⏳] Nhập delay giữa các lần gửi (giây)", default="5"))
                        if delay < 0:
                            console_print("[❌] Delay phải không âm!", style="bold red")
                            continue
                        break
                    except ValueError:
                        console_print("[❌] Delay phải là số!", style="bold red")
                p = multiprocessing.Process(
                    target=start_bot_treoanh,
                    args=('api_key', 'secret_key', imei, session_cookies, image_folder, delay, selected_ids)
                )
            elif mode == '5':
                while True:
                    try:
                        delay = float(Prompt.ask("[⏳] Nhập delay giữa các lần đổi tên (giây)", default="5"))
                        if delay < 0:
                            console_print("[❌] Delay phải không âm!", style="bold red")
                            continue
                        break
                    except ValueError:
                        console_print("[❌] Delay phải là số!", style="bold red")
                p = multiprocessing.Process(
                    target=start_bot_doitennhom,
                    args=('api_key', 'secret_key', imei, session_cookies, delay, selected_ids)
                )
            elif mode == '6':
                image_folder = Prompt.ask("[📁] Nhập đường dẫn thư mục chứa ảnh")
                if not os.path.isdir(image_folder):
                    console_print("[❌] Thư mục không tồn tại!", style="bold red")
                    continue
                while True:
                    try:
                        repeat_count = int(Prompt.ask("[🔢] Nhập số lần đổi avatar", default="5"))
                        if repeat_count <= 0:
                            console_print("[❌] Số lần phải là số nguyên dương!", style="bold red")
                            continue
                        break
                    except ValueError:
                        console_print("[❌] Số lần phải là số nguyên!", style="bold red")
                while True:
                    try:
                        delay = float(Prompt.ask("[⏳] Nhập delay giữa các lần đổi (giây)", default="5"))
                        if delay < 0:
                            console_print("[❌] Delay phải không âm!", style="bold red")
                            continue
                        break
                    except ValueError:
                        console_print("[❌] Delay phải là số!", style="bold red")
                p = multiprocessing.Process(
                    target=start_bot_doianhnhom,
                    args=('api_key', 'secret_key', imei, session_cookies, image_folder, repeat_count, delay, selected_ids)
                )
            elif mode == '7':
                while True:
                    try:
                        sticker_count = int(Prompt.ask("[🔢] Nhập số lượng sticker muốn spam", default="10"))
                        if sticker_count <= 0:
                            console_print("[❌] Số lượng phải là số nguyên dương!", style="bold red")
                            continue
                        break
                    except ValueError:
                        console_print("[❌] Số lượng phải là số nguyên!", style="bold red")
                while True:
                    try:
                        delay = float(Prompt.ask("[⏳] Nhập delay giữa các lần gửi (giây)", default="5"))
                        if delay < 0:
                            console_print("[❌] Delay phải không âm!", style="bold red")
                            continue
                        break
                    except ValueError:
                        console_print("[❌] Delay phải là số!", style="bold red")
                p = multiprocessing.Process(
                    target=start_bot_spamsticker,
                    args=('api_key', 'secret_key', imei, session_cookies, sticker_count, delay, selected_ids)
                )
            elif mode == '8':
                while True:
                    try:
                        delay = float(Prompt.ask("[⏳] Nhập delay giữa các lần gửi (giây)", default="5"))
                        if delay < 0:
                            console_print("[❌] Delay phải không âm!", style="bold red")
                            continue
                        break
                    except ValueError:
                        console_print("[❌] Delay phải là số!", style="bold red")
                p = multiprocessing.Process(
                    target=start_bot_spamvoice,
                    args=('api_key', 'secret_key', imei, session_cookies, delay, selected_ids)
                )
            else:
                while True:
                    try:
                        delay = float(Prompt.ask("[⏳] Nhập delay giữa các lần gửi (giây)", default="5"))
                        if delay < 0:
                            console_print("[❌] Delay phải không âm!", style="bold red")
                            continue
                        break
                    except ValueError:
                        console_print("[❌] Delay phải là số!", style="bold red")
                tagged_users = {}
                for group_id in selected_ids:
                    members = bot.fetchGroupMembers(group_id)
                    if not members:
                        console_print(f"[⚠️] Nhóm {group_id} không có thành viên!", style="bold red")
                        continue
                    table = Table(show_header=True, header_style="bold cyan", show_lines=False, box=None)
                    table.add_column("STT", width=5, justify="center", style="white")
                    table.add_column("Tên thành viên", width=25, justify="left", style="bold green")
                    table.add_column("ID", width=15, justify="left", style="cyan")
                    for idx, member in enumerate(members, 1):
                        table.add_row(str(idx), member['name'], member['id'])
                    console.print(Panel(table, title=f"[bold cyan]📋 Thành viên nhóm {group_id}[/bold cyan]", border_style="bold cyan", width=60, padding=(0, 1)))
                    raw = Prompt.ask("[🔸] Nhập số thứ tự thành viên để spam danh thiếp (VD: 1,2,3)", default="")
                    selected_members = parse_selection(raw, len(members))
                    if not selected_members:
                        console_print("[⚠️] Không chọn thành viên nào!", style="bold red")
                        continue
                    tagged_users[group_id] = [members[i - 1]['id'] for i in selected_members]
                p = multiprocessing.Process(
                    target=start_bot_spamcard,
                    args=('api_key', 'secret_key', imei, session_cookies, delay, selected_ids, tagged_users)
                )
            processes.append(p)
            p.start()
        except Exception as e:
            console_print(f"[❌] Lỗi nhập liệu: {e}", style="bold red")
            continue
    console_print("\n[✅] TẤT CẢ BOT ĐÃ KHỞI ĐỘNG THÀNH CÔNG", style="bold green")

if __name__ == "__main__":
    login_screen()
    start_multiple_accounts()