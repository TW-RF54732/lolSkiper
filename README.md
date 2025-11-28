# 這是啥?
這是一個超級懶的費柴因為不想看生涯規劃而做的腳本，可以幾秒**看完**影片
# 使用
[下載exe發行版](https://github.com/TW-RF54732/lolSkiper/releases/tag/GUI%E7%99%BC%E8%A1%8C%E7%89%88)
執行。 Windows 可能會誤認為病毒，請案詳細資訊後按繼續執行
在session中輸入session和影片/課程號碼(不會的到完全保母及教學第五項)
---
# 一般教學
## Setup
```
git clone https://github.com/TW-RF54732/tronclassHelper.git
cd .\tronclassHelper\
pip install -r requirement.txt
```
## Setting
打開腳本，把session以字串貼入變數`session_id`
## Execute
跳過一部影片運行`TronClassSkiper.py`
想刷掉整節課的影片運行`classScanner.py`
找到URL中的代碼一串數字貼入
# 完全保母級教學

這是一個使用 Python 撰寫的簡單工具。  
本說明將一步步教你如何在 **Windows 電腦** 上執行這個程式。 
（完全不需要電腦背景知識，只要照著做就行 👌）

---

## 🪟 一、安裝 Python  ✅ 已安裝者可略過

1. 打開你的瀏覽器（例如 Edge 或 Chrome）  
2. 前往 [Python 官方網站](https://www.python.org/downloads/)  
3. 點擊黃色按鈕 **「Download Python 3.x.x」**  
4. 開啟剛下載的安裝檔（例如 `python-3.12.0.exe`）  
5. ⚠️ **請務必勾選** `Add Python to PATH`  
   然後再按下 **Install Now**

安裝完成後，關閉安裝程式。

---

## 🧪 二、確認 Python 是否安裝成功

1. 按下鍵盤上的 **Windows 鍵 + R**  
2. 輸入 `cmd` 然後按 Enter  
3. 在黑色的視窗中輸入：
```

python --version

```
若顯示出類似：
```

Python 3.12.0

```
表示安裝成功 🎉

---

## 📦 三、下載這個專案

1. 到此專案的 GitHub 頁面  
2. 點擊右上角的 **綠色按鈕「Code」** → 選擇 **「Download ZIP」**  
3. 下載完成後，右鍵點擊壓縮檔 → 選擇「全部解壓縮」  

---

## 🧰 四、安裝依賴套件（非常重要）

1. 打開解壓後的資料夾  
2. 資料夾中空白部分按右鍵->(win11需要先按下"顯示其他選項")在終端中開啟
3. 執行以下指令來安裝套件：
```

pip install -r requirement.txt

```
安裝過程會出現一些文字，等待它跑完即可。  
如果看到「Successfully installed ...」代表成功 ✅

---

## 🚀 五、設定腳本
腳本會需要以當入你的帳號的狀況下去刷影片，所以會需要你提供Session
Chrome和Edge以及多數瀏覽器是一樣的
1. 打開瀏覽器並且打開Tronclass並且登入
2. 按下F12或`ctrl+shift+I`打開開發者工具
3. 在最上方會有主控台、原始碼等等，從中選擇"應用程式"的選項(如果沒看到可能是視窗不夠大被摺疊了，按下">>"或"+"或把視窗拉開都可)
4. 找到Cookie並打開捲折選單，複製名叫session的內容，開頭應該為V2-1...後面會是亂碼(⚠️⚠️這個代碼跟密碼很像，取得就能直接登入你的帳號，請保管好⚠️⚠️)
<img width="1593" height="815" alt="image" src="https://github.com/user-attachments/assets/69c15329-c17a-4fc4-9906-35632103c1c6" />


5. 用任何文字編輯器打開`TronClassSkiper.py`和`classScanner.py`(也可以在檔案中對檔案按右鍵->在記事本中編輯)
6. 找到一行叫:
```
session_id = "" #用字串輸入你的session!!!!
```
做並在兩個引號中把你在地4步驟複製的session貼上去
<img width="942" height="403" alt="image" src="https://github.com/user-attachments/assets/b6e36500-b993-42e9-a272-8a67c479e453" />
7. 儲存(`ctrl+S`)
## 六、運行腳本
打開終端: 在腳本的資料夾中空白部分按右鍵->(win11需要先按下"顯示其他選項")在終端中開啟
### 你只想跳過一部影片
1. 在終端中執行:
```
python TronClassSkiper.py
```
之後會向你要求課程碼
2.從瀏覽器中打開你要跳過的影片的頁面，找到URL中最後部分的一串數字，複製下貼給終端
<img width="1521" height="835" alt="image" src="https://github.com/user-attachments/assets/c25d713b-78da-40a7-883d-ddd9cc98ccda" />

---

<img width="1095" height="107" alt="image" src="https://github.com/user-attachments/assets/a39fd437-213d-4a2b-8a94-d9b25b29b15d" />
3. 然後按下Enter，等待爆破小隊收工，進度條完成後就已經跳過了。回到Tronclass查看(沒有的話刷新看看，依然沒有可以寫Issues給我)

### 你跟我一樣比較懶，想直接跳過課程中所有的影片:
1. 在終端中執行:
```
python classScanner.py
```
2. 從瀏覽器中打開你要跳過的課程的頁面，找到URL中一部分的一串數字，複製下貼給終端後按下Enter，等爆破大隊完工即可(如果課程比較多，程式會需要幾十秒後才會顯示進度條)
<img width="1519" height="824" alt="image" src="https://github.com/user-attachments/assets/5f9c480d-edb3-4584-8e70-d5e5fa03105a" />

---

<img width="922" height="65" alt="image" src="https://github.com/user-attachments/assets/206540ae-8408-4637-b91e-cf0f7c9e446d" />
3. 打開Tronclass查看

## 🧯 常見問題（給第一次用的人）

| 問題 | 解法 |
|------|------|
| ⚠️ `python` 不是內部或外部命令 | 重新安裝 Python，記得勾選「Add Python to PATH」 |
| ⚠️ `pip` 找不到 | 重新開啟 cmd 後再試一次 |
| ⚠️ 權限錯誤（Permission denied） | 嘗試「以系統管理員身分執行」命令提示字元 |
| 想知道程式做什麼 | 回到 GitHub 首頁查看說明區段 |



---

（End of README）
