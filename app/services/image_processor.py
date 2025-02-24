from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os


class ImageProcessor:
    def __init__(self):
        """
        Настраивает шрифт и базовое изображение.
        """
        # Папки / пути
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(current_dir, ".."))

        # Параметры файлов
        self.image_path = os.path.join(
            project_dir, "static", "images", "oleg_origin.png"
        )
        self.font_path = os.path.join(project_dir, "static", "fonts", "arial_bold.ttf")

        # Параметры отрисовки
        self.font_size = 88
        self.font_color = (255, 255, 255)  # белый текст
        self.text_margin = 16  # отступ от краёв
        self.line_spacing = 4  # промежуток между строками
        self.stroke_width = 2  # толщина обводки
        self.stroke_color = (0, 0, 0)  # цвет обводки (чёрный)

        # Инициализация
        self.font = self._load_font()
        self.base_image = Image.open(self.image_path)

    def _load_font(self) -> ImageFont.FreeTypeFont:
        """
        Загружает шрифт (TrueType).
        Если не получается, возвращаем шрифт по умолчанию.
        """
        try:
            return ImageFont.truetype(self.font_path, self.font_size)
        except IOError:
            return ImageFont.load_default()

    def _get_default_line_height(self, draw: ImageDraw.Draw) -> int:
        """
        Возвращает «стандартную» (фиксированную) высоту строки для данного шрифта.
        Часто используют строку 'Hg', чтобы учесть верхние/нижние выносные элементы.
        """
        left, top, right, bottom = draw.textbbox((0, 0), "Hg", font=self.font)
        return bottom - top

    def _wrap_text(self, text: str, draw: ImageDraw.Draw, max_width: int) -> list[str]:
        """
        Разбивает text на список строк, которые не выходят за max_width пикселей.
        Использует textbbox(...) для измерения ширины.
        """
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            left, top, right, bottom = draw.textbbox((0, 0), test_line, font=self.font)
            line_width = right - left

            if line_width <= max_width:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def _calculate_multiline_height(
        self, lines: list[str], draw: ImageDraw.Draw
    ) -> int:
        """
        Считает общую высоту набора строк, исходя из единой «базовой» высоты строки
        (а не реальной высоты каждой конкретной строки). Это обеспечивает
        одинаковые отступы вне зависимости от строчных/прописных букв.
        """
        line_count = len(lines)
        if line_count == 0:
            return 0

        base_line_height = self._get_default_line_height(draw)
        # Общая высота = (кол-во строк) * высота одной строки + промежутки между строками
        return line_count * base_line_height + (line_count - 1) * self.line_spacing

    def _draw_multiline_centered(
        self, draw: ImageDraw.Draw, lines: list[str], start_y: int, img_width: int
    ) -> int:
        """
        Рисует набор строк по центру (горизонтально), начиная с координаты Y = start_y,
        используя фиксированную высоту строки из _get_default_line_height.
        Возвращает конечный Y после последней строки (на случай, если захотите продолжить).
        """
        base_line_height = self._get_default_line_height(draw)

        y = start_y
        for line in lines:
            # Ширина текущей строки (только для горизонтального центрирования)
            left, top, right, bottom = draw.textbbox((0, 0), line, font=self.font)
            line_width = right - left

            x = (img_width - line_width) // 2

            draw.text(
                (x, y),
                line,
                font=self.font,
                fill=self.font_color,
                stroke_width=self.stroke_width,
                stroke_fill=self.stroke_color,
            )
            # Смещаемся на фиксированную высоту + межстрочный отступ
            y += base_line_height + self.line_spacing

        return y

    def add_text_to_image(self, title: str, subtitle: str) -> BytesIO:
        """
        Основной метод:
         - копируем базовое изображение,
         - переносим заголовок и подзаголовок по ширине,
         - рисуем их с обводкой и возвращаем результат в BytesIO (PNG).
        """
        img = self.base_image.copy()
        draw = ImageDraw.Draw(img)
        img_width, img_height = img.size

        # --- Готовим и рисуем заголовок (title) ---
        max_text_width = int(img_width * 0.9)
        title_lines = self._wrap_text(title, draw, max_text_width)
        # Рисуем сверху, отступив text_margin
        title_y = self.text_margin
        end_of_title_y = self._draw_multiline_centered(
            draw=draw, lines=title_lines, start_y=title_y, img_width=img_width
        )

        # --- Готовим и рисуем подзаголовок (subtitle) ---
        subtitle_lines = self._wrap_text(subtitle, draw, max_text_width)

        # Вычисляем высоту всех строк подзаголовка по фиксированной высоте
        subtitle_height = self._calculate_multiline_height(subtitle_lines, draw)
        # Начальная Y-координата для подзаголовка (ниже, от нижнего края)
        subtitle_y = img_height - subtitle_height - self.text_margin * 1.5

        self._draw_multiline_centered(
            draw=draw, lines=subtitle_lines, start_y=subtitle_y, img_width=img_width
        )

        # Возвращаем результат в виде байтового потока (PNG)
        return self._image_to_bytes(img)

    def _image_to_bytes(self, image: Image.Image) -> BytesIO:
        """
        Преобразует PIL.Image в поток байтов (PNG).
        """
        img_byte_array = BytesIO()
        image.save(img_byte_array, format="PNG")
        img_byte_array.seek(0)
        return img_byte_array
