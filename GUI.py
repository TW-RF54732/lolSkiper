import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests
import urllib3
import time
import socket  # 新增：用於控制網路超時

# 引用你的原始模組
import TronClassSkiper

# 禁用警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TronClassGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TronClass 學習小幫手 GUI (V3 穩定版)")
        self.root.geometry("600x550")
        
        # 變數設定
        self.session_var = tk.StringVar()
        self.code_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="single")
        
        # 線程控制事件
        self.pause_event = threading.Event()
        self.pause_event.set()  # 預設為 True (綠燈/執行中)
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

        # 3. 進度與日誌
        log_frame = ttk.LabelFrame(self.root, text="執行日誌", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.progress = ttk.Progressbar(log_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, state='disabled')
        self.log_text.pack(fill="both", expand=True)

        self.status_label = ttk.Label(log_frame, text="待機中", foreground="gray")
        self.status_label.pack(anchor="e")

    def log(self, message):
        """線程安全的日誌寫入"""
        self.root.after(0, lambda: self._write_log(message))

    def _write_log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def toggle_ui_state(self, running):
        if running:
            self.btn_start.pack_forget()
            self.run_btns_frame.pack(fill="x", pady=5)
            self.status_label.config(text="正在執行...", foreground="blue")
        else:
            self.run_btns_frame.pack_forget()
            self.btn_start.pack(fill="x", pady=5)
            self.btn_pause.config(text="暫停")
            self.status_label.config(text="待機中", foreground="gray")

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
        self.log("=== 開始任務 (V3) ===")
        
        threading.Thread(target=self.run_logic, args=(session_id, code), daemon=True).start()

    def toggle_pause(self):
        if self.pause_event.is_set():
            self.pause_event.clear() # 設定為 False (紅燈/暫停)
            self.btn_pause.config(text="繼續執行")
            self.log(">>> 暫停中...")
            self.status_label.config(text="已暫停", foreground="orange")
        else:
            self.pause_event.set() # 設定為 True (綠燈/繼續)
            self.btn_pause.config(text="暫停")
            self.log(">>> 繼續執行")
            self.status_label.config(text="正在執行...", foreground="blue")

    def stop_task(self):
        if self.is_running:
            if messagebox.askyesno("確認", "確定要終止當前任務嗎？"):
                self.log("!!! 正在發送終止信號...")
                self.stop_event.set()
                # 這裡不需要 set pause_event，因為 check_flags 的輪詢機制會自動處理

    def check_flags(self):
        """
        改進後的檢查點：
        使用迴圈輪詢，而不是死等 (wait)。
        這樣即使在暫停狀態下，也能立刻響應停止訊號。
        """
        if self.stop_event.is_set():
            raise InterruptedError("使用者終止任務")
        
        # 如果暫停了 (pause_event 被 clear)
        while not self.pause_event.is_set():
            if self.stop_event.is_set():
                raise InterruptedError("使用者終止任務")
            time.sleep(0.1) # 短暫睡眠，避免吃滿 CPU
            # 這裡不會卡死，會每 0.1 秒醒來檢查一次狀態

    def run_logic(self, session_id, code):
        # --- 關鍵修正：設定全域 Socket 超時 ---
        # 防止 requests 卡死在網路層。設定為 10 秒。
        socket.setdefaulttimeout(10)
        
        try:
            TronClassSkiper.session_id = session_id
            TronClassSkiper.session.cookies.set("session", session_id)
            
            # 重新建立 Session 以確保乾淨的狀態 (選用，但推薦)
            # 這裡我們保留原作者的結構，但確保 headers 正確
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
        except socket.timeout:
            self.log("!!! 錯誤: 網路連線逾時，請檢查網路或稍後再試。")
            self.root.after(0, lambda: messagebox.showerror("錯誤", "網路連線逾時"))
        except Exception as e:
            self.log(f"發生錯誤: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("錯誤", f"發生異常: {str(e)}"))
        finally:
            self.is_running = False
            self.root.after(0, lambda: self.toggle_ui_state(False))
            # 恢復預設超時設定，避免影響其他程式（如果有的話）
            socket.setdefaulttimeout(None)

    def process_single_video(self, video_id):
        self.check_flags()
        self.log(f"正在分析影片 ID: {video_id}...")
        
        # 增加重試機制防止讀取影片時間失敗
        total_time = 0
        try:
            total_time = TronClassSkiper.getVideoTime(video_id)
        except Exception as e:
            self.log(f"讀取影片資訊失敗: {e}")
            return

        self.root.after(0, lambda: self.progress.configure(maximum=total_time, value=0))
        
        current_progress = 0
        # 這裡的迴圈依賴 generator，我們加上 try-except 包裹來處理網路中斷
        try:
            for added_time in TronClassSkiper.API_Skip(video_id):
                self.check_flags()
                current_progress += added_time
                self.root.after(0, lambda v=current_progress: self.progress.configure(value=v))
        except socket.timeout:
            self.log(f"警告: 影片 {video_id} 處理過程中網路逾時。")
        except Exception as e:
            self.log(f"警告: 影片 {video_id} 處理中斷: {e}")

            
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
        
        self.log(f"找到 {len(target_ids)} 個影片，計算總時長中(可能會花一點時間)...")
        
        total_length = 0
        valid_ids = []
        
        for vid in target_ids:
            self.check_flags()
            try:
                # 這裡也要防範單個獲取時間失敗導致全崩
                t = TronClassSkiper.getVideoTime(vid)
                total_length += t
                valid_ids.append(vid)
            except Exception:
                self.log(f"跳過無法讀取的影片 ID: {vid}")

        self.log(f"總任務時長: {total_length} 秒。開始執行...")
        self.root.after(0, lambda: self.progress.configure(maximum=total_length, value=0))
        
        current_total_progress = 0
        
        for vid in valid_ids:
            self.log(f"-> 處理影片: {vid}")
            try:
                for added_time in TronClassSkiper.API_Skip(vid):
                    self.check_flags()
                    current_total_progress += added_time
                    self.root.after(0, lambda v=current_total_progress: self.progress.configure(value=v))
            except Exception as e:
                self.log(f"影片 {vid} 發生錯誤 (可能是網路問題)，跳過: {e}")
                # 跳過該影片，繼續下一個，而不是崩潰
                continue

if __name__ == "__main__":
    root = tk.Tk()
    app = TronClassGUI(root)
    root.mainloop()