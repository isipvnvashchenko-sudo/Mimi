from datetime import datetime, timedelta
from src.db import JSONDatabase

class HabitService:
    def __init__(self, db: JSONDatabase):
        self.db = db

    def add_habit(self, name: str) -> dict:
        """Добавляет новую привычку с валидацией имени."""
        if not name or not name.strip():
            raise ValueError("Название не может быть пустым")
        if len(name) > 100:
            raise ValueError("Название не должно превышать 100 символов")

        data = self.db.load_data()
        

        next_id = max([h["id"] for h in data["habits"]], default=0) + 1
        
        new_habit = {
            "id": next_id,
            "name": name.strip(),
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "is_active": True,
            "logs": []
        }
        
        data["habits"].append(new_habit)
        self.db.save_data(data)
        return new_habit

    def get_all_active_habits(self) -> list:
        """Возвращает список всех неудаленных привычек."""
        data = self.db.load_data()
        return [h for h in data["habits"] if h.get("is_active", True)]

    def check_habit(self, habit_id: int, date_str: str = None) -> bool:
        """Отмечает выполнение привычки на указанную дату (по умолчанию сегодня)."""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            
        data = self.db.load_data()
        for habit in data["habits"]:
            if habit["id"] == habit_id and habit.get("is_active", True):
                if date_str in habit["logs"]:
                    return False 
                habit["logs"].append(date_str)
                self.db.save_data(data)
                return True
        raise KeyError(f"Привычка с ID {habit_id} не найдена")

    def delete_habit(self, habit_id: int) -> bool:
        """Мягкое удаление (Soft Delete) привычки по ID."""
        data = self.db.load_data()
        for habit in data["habits"]:
            if habit["id"] == habit_id and habit.get("is_active", True):
                habit["is_active"] = False
                self.db.save_data(data)
                return True
        raise KeyError(f"Привычка с ID {habit_id} не найдена")

    def calculate_streak(self, logs: list) -> int:
        """Рассчитывает текущую серию (streak) непрерывного выполнения."""
        if not logs:
            return 0
        
        
        sorted_dates = sorted(list(set([datetime.strptime(d, "%Y-%m-%d").date() for d in logs])), reverse=True)
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        
        if sorted_dates[0] < yesterday and sorted_dates[0] != today:
            return 0
            
        streak = 0
        expected_date = sorted_dates[0]
        
    
        if expected_date != today and expected_date != yesterday:
            return 0

        for date in sorted_dates:
            if date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            else:
                break
        return streak