# What Is Bro Doing

一個使用 Discord Rich Presence 顯示當前正在使用應用程式的工具。

## 功能

- 即時顯示當前使用的應用程式
- 可自訂顯示文字
- 支援應用程式名稱對照表
- 可動態編輯應用程式清單

## 使用方法

1. 安裝必要套件：
```bash
pip install pypresence pygetwindow psutil pywin32
```

2. 執行程式：
```bash
python main.py
```

3. 選擇模式：
   - 0: 開始監控
   - 1: 編輯應用程式清單

## 設定

在 `applist.py` 中可以自定義應用程式的顯示名稱。