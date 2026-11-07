from PySide6.QtWidgets import QLayout, QWidget, QWidgetItem
from PySide6.QtCore import QPoint, QRect, QSize, Qt, QSize


class FlowLayout(QLayout):
    
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self._item_list: list[QWidgetItem] = []

        # 背景用パネルの設定
        self._bg_panel = QWidget(parent)
        self._bg_panel.setObjectName("FlowBackground")
        
        # スタイルシートの背景色へ反映
        self._bg_panel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        
        self._bg_panel.lower() # 背面に送る

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item: QWidgetItem):
        """.addWidget() で自動発火"""
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index: int):
        """レイアウトの 計算/配置 で自動発火"""
        if 0 <= index < len(self._item_list):
            return self._item_list[index]

        return None

    def takeAt(self, index: int):
        """ウィジェットが廃棄 で自動発火"""
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)

        return None

    def expandingDirections(self):
        """レイアウトの初期配置 で自動発火"""
        # 水平方向/水平方向 のどちらにも広げない
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        """レイアウトのサイズが変わる度 自動発火"""
        return True

    def heightForWidth(self, width: int):
        """ウィンドウが変わる度 自動発火"""
        height = self._do_layout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect: QRect):
        """ウィンドウの 初期表示/リサイズ で自動発火"""
        super(FlowLayout, self).setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        """レイアウトの 推奨サイズ を返す"""
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect: QRect, test_only: bool):
        """
        ウィジェットの配置を中央揃えで自動折り返し
        最後の行は左揃え
        """
        
        padding = 15  # 背景とウィジェットの間の隙間
        
        # 開始位置にパディングを考慮（少し内側から並べ始める）
        x = rect.x() + padding
        y = rect.y() + padding
        line_height = 0
        max_row_width = 0

        for item in self._item_list:
            space_x = self.spacing()
            space_y = self.spacing()
            
            # 改行判定（右側のパディングも考慮して rect.right() - padding）
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() - padding and line_height > 0:
                current_row_width = x - (rect.x() + padding) - space_x
                max_row_width = max(max_row_width, current_row_width)
                
                x = rect.x() + padding
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        # 最後の行の幅を計算
        if x > rect.x() + padding:
            current_row_width = x - (rect.x() + padding) - self.spacing()
            max_row_width = max(max_row_width, current_row_width)

        # ウィジェットの塊の合計サイズ（パディング込み）
        total_content_width = max_row_width + (padding * 2)
        total_content_height = (y + line_height) - rect.y() + padding

        # 中央寄せのオフセットを計算
        offset = (rect.width() - total_content_width) // 2 if total_content_width > 0 else 0

        if not test_only:
            # アイテムを中央へスライド
            for item in self._item_list:
                r = item.geometry()
                item.setGeometry(QRect(r.x() + offset, r.y(), r.width(), r.height()))

            # 背景パネルを配置
            if max_row_width > 0:
                # 親ウィジェットが未設定ならレイアウトの親を割り当てる
                if self._bg_panel.parent() is None and self.parentWidget() is not None:
                    self._bg_panel.setParent(self.parentWidget())
                    self._bg_panel.lower()  # 親が設定されたので再度背面に送る

                self._bg_panel.show()
                # ウィジェットの塊の「左端(offset)」から、パディングを含めたサイズで描画
                self._bg_panel.setGeometry(rect.x() + offset, rect.y(), 
                                        total_content_width, total_content_height)
            else:
                self._bg_panel.hide()
        
        return total_content_height
    
    def delete_widget(self, widget: QWidget):
        """FlowLayoutからウィジェットの削除"""
        
        if widget is not None:
            
            # _item_list から該当する QLayoutItem を探して削除する
            for cnt, item in enumerate(self._item_list):
                if item.widget() == widget:
                    self._item_list.pop(cnt)
                    break
            
            # レイアウトの管理下から外す
            self.removeWidget(widget)
            
            # 親子関係を抹消 (ガベージコレクタの対象にする)
            widget.setParent(None)
            widget.deleteLater()  # PyQtの推奨メソッド

            # レイアウトを再計算
            self.update()