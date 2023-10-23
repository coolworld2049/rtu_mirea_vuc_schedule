import random

from locust import HttpUser, task

course_with_platoons = {
    3: [123, 133, 183],
    4: [102, 112, 142],
    5: [101, 111, 241],
}

weeks: list[int] = list(range(1, 19))

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


class Benchmark(HttpUser):
    @task(2)
    def test_schedule_week(self):
        course = random.choice(list(course_with_platoons.keys()))
        platoon = random.choice(course_with_platoons[course])
        self.client.get(
            f"/schedule/week?course={course}&week={random.choice(weeks)}&platoon={platoon}",
        )

    @task(1)
    def test_schedule_day_week(self):
        course = random.choice(list(course_with_platoons.keys()))
        platoon = random.choice(course_with_platoons[course])
        self.client.get(f"/schedule/day/week?course={course}&platoon={platoon}")

    @task(1)
    def test_schedule_platoons(self):
        course = random.choice(list(course_with_platoons.keys()))
        self.client.get(f"/schedule/platoons?course={course}")
