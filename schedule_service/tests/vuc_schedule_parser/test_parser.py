from schedule_service.services.vuc_schedule_parser.parser import ScheduleParser


def test_parse_schedule(
    schedule_parser_instance: ScheduleParser,
    week=8,
    platoon: int | None = None,
) -> None:
    result = schedule_parser_instance.parse_schedule(week=week, platoon=platoon)
    assert len(result) > 0
    platoon_number = result[0].platoon.platoon_number
    for res in result:
        assert res.schedule.date and res.schedule.datetime
        assert len(res.schedule.subjects) > 0
        for sub in res.schedule.subjects:
            assert sub.name
    if not platoon:
        test_parse_schedule(schedule_parser_instance, platoon=platoon_number)


def test_get_days_week(
    schedule_parser_instance: ScheduleParser,
    platoon: int | None = None,
) -> None:
    result = schedule_parser_instance.get_days_week(platoon=platoon)
    assert len(result) > 0
    platoon_number = result[0].days[0].platoons[0]
    for res in result:
        if len(res.days) > 0:
            for day in res.days:

                if platoon:
                    assert len(day.platoons) == 1
                else:
                    assert len(day.platoons) > 0
    if not platoon:
        test_get_days_week(schedule_parser_instance, platoon=platoon_number)


def test_get_platoons(
    schedule_parser_instance: ScheduleParser,
    speciality_code: int | None = None,
) -> None:
    result = schedule_parser_instance.platoons(speciality_code=speciality_code)
    assert len(result) > 0
    _specialty_code = result[0].specialty_code
    for res in result:
        assert res.platoon_number and res.specialty_code
    if not speciality_code:
        test_get_platoons(schedule_parser_instance, speciality_code=_specialty_code)
