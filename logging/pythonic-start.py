# https://www.youtube.com/watch?v=bsU7AFjh4m8
# "import this" at terminal to get python philosophy

import os
from datetime import datetime

class FitnessTracker:
    def log_food(self, item, calories, date=None):
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        f = open("food.csv", 'a')
        f.write(f'{date},{item},{calories}\n')
        f.close()
        print(f'Appended food {item} ({calories} kcal) on {date}.')


    def log_activity(self, activity, calories_burned, date=None):
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        f = open("activities.csv", 'a')
        f.write(f'{date},{activity},{calories_burned}\n')
        f.close()
        print(f'Appended activity {activity} ({calories_burned} kcal) on {date}.')

    def run_day_summary(self, date):
        food = []
        if os.path.exists("food.csv"):
            f = open("food.csv")
            for line in f:
                parts = line.strip().split(',')
                if parts[0] == date:
                    food.append(int(parts[2]))
            f.close()
        else:
            print("Could not reach food.csv.")
        activity = []
        if os.path.exists("activities.csv"):
            f = open("activities.csv")
            for line in f:
                parts = line.strip().split(',')
                if parts[0] == date:
                    activity.append(int(parts[2]))
            f.close()
        else:
            print("Could not reach activities.csv.")

        food_total = sum(food)
        activity_total = sum(activity)
        net = food_total - activity_total
        print(f"Summary for {date}")
        print(f"  Food total:       {food_total}")
        print(f"  Activity total:   {activity_total}")
        print(f"  Net               {net} kcal")


tracker = FitnessTracker()
tracker.log_food("Banana", 100)
tracker.log_activity("Running", 50)
tracker.run_day_summary("2025-11-23")

