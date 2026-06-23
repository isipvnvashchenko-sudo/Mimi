import pytest
import os
from datetime import datetime, timedelta
from db import JSONDatabase
from services import HabitService

TEST_DB_PATH = "test_habits.json"

@pytest.fixture
def temp_service():
    """Фикстура для создания изолированной временной БД на каждый тест."""
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    db = JSONDatabase(filepath=TEST_DB_PATH)
    service = HabitService(db)
    yield service
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_add_habit_success(temp_service):
    habit = temp_service.add_habit("Медитация")
    assert habit["id"] == 1
    assert habit["name"] == "Медитация"
    assert habit["is_active"] is True
    assert len(temp_service.get_all_active_habits()) == 1

def test_add_habit_empty_name_raises_error(temp_service):
    with pytest.raises(ValueError, match="Название не может быть пустым"):
        temp_service.add_habit("   ")

def test_add_habit_too_long_name_raises_error(temp_service):
    with pytest.raises(ValueError, match="Название не должно превышать 100 символов"):
        temp_service.add_habit("A" * 101)

def test_check_habit_success(temp_service):
    temp_service.add_habit("Бег")
    today = datetime.now().strftime("%Y-%m-%d")
    result = temp_service.check_habit(1, today)
    assert result is True
    
    result_duplicate = temp_service.check_habit(1, today)
    assert result_duplicate is False

def test_check_habit_not_found(temp_service):
    with pytest.raises(KeyError):
        temp_service.check_habit(999)

def test_delete_habit_soft_delete(temp_service):
    temp_service.add_habit("Чтение")
    temp_service.delete_habit(1)
    assert len(temp_service.get_all_active_habits()) == 0

def test_streak_calculation_basic(temp_service):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    
    logs = [today.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d"), two_days_ago.strftime("%Y-%m-%d")]
    assert temp_service.calculate_streak(logs) == 3

def test_streak_calculation_with_gap(temp_service):
    four_days_ago = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")
    logs = [four_days_ago]
    assert temp_service.calculate_streak(logs) == 0