```markdown
# keepWindowsAlive

這個小工具會防止 Windows 進入睡眠或關閉顯示器。它使用 Windows API 呼叫 (SetThreadExecutionState)
來告訴系統目前有活動，並可選擇性地以微小的滑鼠移動作為備援手段。

主要檔案
- `keepAlive.py` — 主程式，可直接以 Python 執行或編譯為單一 exe。
- `build_exe.ps1` — PowerShell 腳本：使用 PyInstaller 建置單一檔案 exe（請先安裝 Python 與 PyInstaller）。
- `requirements.txt` — 建置/開發所需套件清單。

如何使用 (快速)

1. 安裝 Python 3.8+（或你的系統喜愛的版本）。
2. 建議建立虛擬環境：

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. 直接執行（不編譯）：

```powershell
python keepAlive.py --interval 30 --nudge
```

4. 建置單一 exe（Windows）：在 PowerShell 中執行

```powershell
.\build_exe.ps1
```

build_exe.ps1 會呼叫 PyInstaller 並產生 dist\keepAlive\keepAlive.exe。將產物複製到你想要放置的目錄，雙擊即可執行。

注意事項
- 使用這種方式來阻止系統睡眠是受支援的，但請負責任地使用（例如在需要長時間處理工作的情境）。
- 若要停止程式，請在執行中的命令列按 Ctrl+C，或在工作管理員中結束程序。

安全和權限
- 此程式不會修改系統設定或註冊表；它只是暫時告知系統不要睡眠。

若需要協助建置或加入自動開機（task scheduler / startup），請告訴我，我可以幫你把步驟寫成腳本。
```
# keepWindowsAlive