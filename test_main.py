import pytest

import main


@pytest.fixture(autouse=True)
def reset_state():
    main.q0 = 0
    main.q1 = 0
    main.q2 = 0
    main.q3 = 0
    yield
    main.q0 = 0
    main.q1 = 0
    main.q2 = 0
    main.q3 = 0


def set_state(car_type=0, engine=0, brake=0, steering=0):
    main.q0 = car_type
    main.q1 = engine
    main.q2 = brake
    main.q3 = steering


# 제한조건1: Bosch 제동장치는 Bosch 조향장치와만 호환된다.
def test_bosch_brake_with_bosch_steering_is_valid():
    set_state(car_type=main.SEDAN, engine=main.GM, brake=main.BOSCH_B, steering=main.BOSCH_S)
    assert main.is_valid_check() is True


def test_bosch_brake_with_non_bosch_steering_is_invalid():
    set_state(car_type=main.SEDAN, engine=main.GM, brake=main.BOSCH_B, steering=main.MOBIS)
    assert main.is_valid_check() is False


def test_bosch_brake_with_non_bosch_steering_fails_test(capsys):
    set_state(car_type=main.SEDAN, engine=main.GM, brake=main.BOSCH_B, steering=main.MOBIS)
    main.test_produced_car()
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "Bosch제동장치에는 Bosch조향장치 이외 사용 불가" in out


# 제한조건2-1: Sedan에는 Continental 제동장치 사용 불가
def test_sedan_with_continental_brake_is_invalid():
    set_state(car_type=main.SEDAN, engine=main.GM, brake=main.CONTINENTAL, steering=main.MOBIS)
    assert main.is_valid_check() is False


def test_sedan_with_continental_brake_fails_test(capsys):
    set_state(car_type=main.SEDAN, engine=main.GM, brake=main.CONTINENTAL, steering=main.MOBIS)
    main.test_produced_car()
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "Sedan에는 Continental제동장치 사용 불가" in out


# 제한조건2-2: SUV에는 TOYOTA 엔진 사용 불가
def test_suv_with_toyota_engine_is_invalid():
    set_state(car_type=main.SUV, engine=main.TOYOTA, brake=main.MANDO, steering=main.MOBIS)
    assert main.is_valid_check() is False


def test_suv_with_toyota_engine_fails_test(capsys):
    set_state(car_type=main.SUV, engine=main.TOYOTA, brake=main.MANDO, steering=main.MOBIS)
    main.test_produced_car()
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "SUV에는 TOYOTA엔진 사용 불가" in out


# 제한조건2-3: Truck에는 WIA 엔진 사용 불가
def test_truck_with_wia_engine_is_invalid():
    set_state(car_type=main.TRUCK, engine=main.WIA, brake=main.CONTINENTAL, steering=main.MOBIS)
    assert main.is_valid_check() is False


def test_truck_with_wia_engine_fails_test(capsys):
    set_state(car_type=main.TRUCK, engine=main.WIA, brake=main.CONTINENTAL, steering=main.MOBIS)
    main.test_produced_car()
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "Truck에는 WIA엔진 사용 불가" in out


# 제한조건2-4: Truck에는 Mando 제동장치 사용 불가
def test_truck_with_mando_brake_is_invalid():
    set_state(car_type=main.TRUCK, engine=main.GM, brake=main.MANDO, steering=main.MOBIS)
    assert main.is_valid_check() is False


def test_truck_with_mando_brake_fails_test(capsys):
    set_state(car_type=main.TRUCK, engine=main.GM, brake=main.MANDO, steering=main.MOBIS)
    main.test_produced_car()
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "Truck에는 Mando제동장치 사용 불가" in out


# 모든 제한조건을 만족하는 정상 조합은 PASS 되어야 한다.
@pytest.mark.parametrize(
    "car_type, engine, brake, steering",
    [
        (main.SEDAN, main.GM, main.MANDO, main.MOBIS),
        (main.SUV, main.GM, main.CONTINENTAL, main.MOBIS),
        (main.TRUCK, main.GM, main.CONTINENTAL, main.MOBIS),
        (main.SEDAN, main.GM, main.BOSCH_B, main.BOSCH_S),
    ],
)
def test_valid_combinations_pass(capsys, car_type, engine, brake, steering):
    set_state(car_type=car_type, engine=engine, brake=brake, steering=steering)
    assert main.is_valid_check() is True
    main.test_produced_car()
    out = capsys.readouterr().out
    assert "PASS" in out
