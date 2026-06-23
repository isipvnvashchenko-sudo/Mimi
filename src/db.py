import json
import os

class JSONDatabase:
    def __init__(self, filepath="data/habits.json"):
        self.filepath = filepath
        self._init_db()

    def _init_db(self):
        """Создает файл данных и директорию, если они не существуют."""
        dir_name = os.path.dirname(self.filepath)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        
        if not os.path.exists(self.filepath):
            self.save_data({"habits": []})

    def load_data(self) -> dict:
        """Загружает данные из JSON файла."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"habits": []}

    def save_data(self, data: dict):
        """Сохраняет данные в JSON файл."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)