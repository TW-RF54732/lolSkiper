import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests
import urllib3
import time
import socket

# 引用你的原始模組
import TronClassSkiper

# 禁用警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TronClassGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TronClass 學習小幫手 GUI (V5 完善版)")
        self.root.geometry("600x600") # 稍微加高一點以容納新按鈕
        
        # 變數設定
        self.session_var = tk.StringVar()
        self.code_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="single")
        
        # 線程控制事件
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.stop_event = threading.Event()
        self.is_running = False

        self.create_widgets()

    def create_widgets(self):
        # 1. 設定區域
        settings_frame = ttk.LabelFrame(self.root, text="設定", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(settings_frame, text="Session ID:").grid(row=0, column=0, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.session_var, width=50).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="課程/影片代碼:").grid(row=1, column=0, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.code_var, width=20).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        mode_frame = ttk.Frame(settings_frame)
        mode_frame.grid(row=2, column=1, sticky="w", pady=5)
        ttk.Radiobutton(mode_frame, text="單個影片 (輸入影片ID)", variable=self.mode_var, value="single").pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="整門課程 (輸入課程ID)", variable=self.mode_var, value="course").pack(side="left", padx=5)

        # 2. 控制區域
        self.ctrl_frame = ttk.Frame(self.root, padding=10)
        self.ctrl_frame.pack(fill="x")
        
        self.btn_start = ttk.Button(self.ctrl_frame, text="開始執行", command=self.start_task)
        self.btn_start.pack(fill="x", pady=5)

        self.run_btns_frame = ttk.Frame(self.ctrl_frame)
        self.btn_pause = ttk.Button(self.run_btns_frame, text="暫停", command=self.toggle_pause)
        self.btn_pause.pack(side="left", fill="x", expand=True, padx=5)
        self.btn_stop = ttk.Button(self.run_btns_frame, text="終止任務", command=self.stop_task)
        self.btn_stop.pack(side="left", fill="x", expand=True, padx=5)

        # 3. 進度與日誌區域
        log_frame = ttk.LabelFrame(self.root, text="執行日誌", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 進度條
        self.progress = ttk.Progressbar(log_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=(0, 10))
        
        # 日誌文字框
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, state='disabled')
        self.log_text.pack(fill="both", expand=True)

        # --- 底部狀態欄與清除按鈕 ---
        bottom_bar = ttk.Frame(log_frame)
        bottom_bar.pack(fill="x", pady=(5, 0))

        # 清除 LOG 按鈕 (左側)
        self.btn_clear_log = ttk.Button(bottom_bar, text="清除日誌", command=self.clear_log)
        self.btn_clear_log.pack(side="left")

        # 狀態標籤 (右側)
        self.status_label = ttk.Label(bottom_bar, text="待機中", foreground="gray")
        self.status_label.pack(side="right")

    def log(self, message):
        self.root.after(0, lambda: self._write_log(message))

    def _write_log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def clear_log(self):
        """清除日誌內容"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')

    def toggle_ui_state(self, running):
        if running:
            self.btn_start.pack_forget()
            self.run_btns_frame.pack(fill="x", pady=5)
            self.status_label.config(text="正在執行...", foreground="blue")
            self.btn_clear_log.config(state="disabled") # 執行中建議鎖住清除，避免混亂，若想開放可拿掉這行
        else:
            self.run_btns_frame.pack_forget()
            self.btn_start.pack(fill="x", pady=5)
            self.btn_pause.config(text="暫停")
            self.status_label.config(text="待機中", foreground="gray")
            self.btn_clear_log.config(state="normal")

    def start_task(self):
        session_id = self.session_var.get().strip()
        code = self.code_var.get().strip()

        if not session_id or not code:
            messagebox.showerror("錯誤", "請輸入 Session ID 和 代碼")
            return

        self.stop_event.clear()
        self.pause_event.set()
        self.is_running = True
        
        self.toggle_ui_state(True)
        self.log("=== 開始任務 (V5) ===")
        
        threading.Thread(target=self.run_logic, args=(session_id, code), daemon=True).start()

    def toggle_pause(self):
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.btn_pause.config(text="繼續執行")
            self.log(">>> 暫停中...")
            self.status_label.config(text="已暫停", foreground="orange")
        else:
            self.pause_event.set()
            self.btn_pause.config(text="暫停")
            self.log(">>> 繼續執行")
            self.status_label.config(text="正在執行...", foreground="blue")

    def stop_task(self):
        if self.is_running:
            if messagebox.askyesno("確認", "確定要終止當前任務嗎？"):
                self.log("!!! 正在發送終止信號...")
                self.stop_event.set()

    def check_flags(self):
        if self.stop_event.is_set():
            raise InterruptedError("使用者終止任務")
        
        while not self.pause_event.is_set():
            if self.stop_event.is_set():
                raise InterruptedError("使用者終止任務")
            time.sleep(0.1)

    def run_logic(self, session_id, code):
        socket.setdefaulttimeout(10)
        
        try:
            TronClassSkiper.session_id = session_id
            TronClassSkiper.session.cookies.set("session", session_id)
            TronClassSkiper.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })

            mode = self.mode_var.get()

            if mode == "single":
                self.process_single_video(code)
            else:
                self.process_course(code)
                
            if not self.stop_event.is_set():
                self.log("=== 任務完成 ===")
                self.root.after(0, lambda: messagebox.showinfo("完成", "任務已完成！"))

        except InterruptedError:
            self.log("=== 任務已強制終止 ===")
            # --- 新增功能：終止後清空進度條 ---
            self.root.after(0, lambda: self.progress.configure(value=0))
            
        except socket.timeout:
            self.log("!!! 錯誤: 網路連線逾時")
            self.root.after(0, lambda: messagebox.showerror("錯誤", "網路連線逾時"))
        except Exception as e:
            self.log(f"發生錯誤: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("錯誤", f"發生異常: {str(e)}"))
        finally:
            self.is_running = False
            self.root.after(0, lambda: self.toggle_ui_state(False))
            socket.setdefaulttimeout(None)

    def process_single_video(self, video_id):
        self.check_flags()
        self.log(f"正在分析影片 ID: {video_id}...")
        
        try:
            total_time = TronClassSkiper.getVideoTime(video_id)
            self.root.after(0, lambda: self.progress.configure(maximum=total_time, value=0))
            
            current_progress = 0
            for added_time in TronClassSkiper.API_Skip(video_id):
                self.check_flags()
                current_progress += added_time
                self.root.after(0, lambda v=current_progress: self.progress.configure(value=v))
        except InterruptedError:
            raise
        except Exception as e:
            self.log(f"警告: 影片 {video_id} 錯誤: {e}")

    def process_course(self, course_id):
        self.check_flags()
        self.log(f"正在掃描課程 ID: {course_id}...")
        
        url = f"https://eclass.yuntech.edu.tw/api/courses/{course_id}/activities?sub_course_id=0"
        try:
            response = TronClassSkiper.session.get(url, verify=False, timeout=10)
        except Exception as e:
            raise Exception(f"連線課程失敗: {e}")
        
        if response.status_code != 200:
            raise Exception(f"無法獲取課程資訊，HTTP: {response.status_code}")
            
        activities = response.json().get("activities", [])
        target_ids = [a["id"] for a in activities if a.get("type") == "online_video"]
        
        self.log(f"找到 {len(target_ids)} 個影片，計算總時長中...")
        
        total_length = 0
        valid_ids = []
        
        for vid in target_ids:
            self.check_flags()
            try:
                t = TronClassSkiper.getVideoTime(vid)
                total_length += t
                valid_ids.append(vid)
            except Exception:
                pass

        self.log(f"總任務時長: {total_length} 秒。開始執行...")
        self.root.after(0, lambda: self.progress.configure(maximum=total_length, value=0))
        
        current_total_progress = 0
        
        for vid in valid_ids:
            self.check_flags()
            self.log(f"-> 處理影片: {vid}")
            try:
                for added_time in TronClassSkiper.API_Skip(vid):
                    self.check_flags()
                    current_total_progress += added_time
                    self.root.after(0, lambda v=current_total_progress: self.progress.configure(value=v))
            except InterruptedError:
                raise 
            except Exception as e:
                self.log(f"影片 {vid} 發生錯誤，跳過: {e}")
                continue

if __name__ == "__main__":
    root = tk.Tk()
    app = TronClassGUI(root)
    root.mainloop()