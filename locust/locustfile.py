import random

from locust import HttpUser, task

course_with_platoons = {
    3: [123, 133, 183, 193, 203, 213, 213],
    4: [102, 112, 142, 152, 222, 232, 242],
    5: [101, 111, 241, 251, 261, 371, 381],
}

weeks: list[int] = list(range(1, 19))

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


class Benchmark(HttpUser):
    @task(4)
    def test_schedule_week(self):
        course = random.choice(list(course_with_platoons.keys()))
        platoon = random.choice(course_with_platoons[course])
        self.client.get(
            f"/schedule/week?course={course}&week={random.choice(weeks)}&platoon={platoon}",
        )

    @task(4)
    def test_workbook_relevance(self):
        course = random.choice(list(course_with_platoons.keys()))
        self.client.get(f"/workbook/relevance/{course}")

    @task(2)
    def test_schedule_day_week(self):
        course = random.choice(list(course_with_platoons.keys()))
        platoon = random.choice(course_with_platoons[course])
        self.client.get(f"/schedule/day/week?course={course}&platoon={platoon}")

    @task(1)
    def test_schedule_platoons(self):
        course = random.choice(list(course_with_platoons.keys()))
        self.client.get(f"/schedule/platoons?course={course}")
