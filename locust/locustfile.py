import random

from locust import FastHttpUser, task

course_with_platoons = {
    3: [123, 133, 183],
    4: [222, 232, 242],
    5: [101, 111, 241],
}

weeks: list[int] = list(range(4, 14))


def rnd_params():
    course = random.choice(list(course_with_platoons.keys()))
    platoon = random.choice(course_with_platoons[course])
    return course, platoon


class Benchmark(FastHttpUser):
    @task(2)
    def test_schedule_week(self):
        course, platoon = rnd_params()
        with self.rest(
            "GET",
            f"/schedule/week?course={course}&week={random.choice(weeks)}&platoon={platoon}",
        ) as resp:
            pass

    @task(1)
    def test_schedule_day_week(self):
        course, platoon = rnd_params()
        with self.rest(
            "GET",
            f"/schedule/day/week?course={course}&platoon={platoon}",
        ) as resp:
            pass
