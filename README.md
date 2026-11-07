# PySide6-FlowLayout
PySide6(Qt) で動作するJava SwingやDart FlutterのFlowに似せたカスタムレイアウトです。

## 特徴
- **ウィジェット配置**: 中央揃え
- **最終行の配置**: 左寄せ
- **ウィジェットの削除**: `delete_widget`メソッドから削除可能

## 想定環境
- Python 3.8 ~
- PySide6

## 使い方
通常のレイアウトどと同様の呼び出し方

```
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from App.FlowLayout import FlowLayout

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FlowLayout Example")
        
        # FlowLayout のインスタンス化
        layout = FlowLayout(self, margin=10, spacing=10)
        
        # ウィジェットの追加
        for cnt in range(1, 6):
            layout.addWidget(QPushButton(f"ボタン {cnt}"))
            layout.addWidget(QLabel(f"ラベル {cnt}"))
        
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
```
