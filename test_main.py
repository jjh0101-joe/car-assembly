import pytest

import main
import parts


def make_state(car_type, engine, brake, steering):
    return {
        "car_type": car_type(),
        "engine": engine(),
        "brake": brake(),
        "steering": steering(),
    }


# 제한조건1: Bosch 제동장치는 Bosch 조향장치와만 호환된다.
def test_bosch_brake_with_bosch_steering_is_valid():
    state = make_state(parts.Sedan, parts.GMEngine, parts.BoschBrake, parts.BoschSteering)
    assert parts.find_violations(**state) == []


def test_bosch_brake_with_non_bosch_steering_is_invalid():
    state = make_state(parts.Sedan, parts.GMEngine, parts.BoschBrake, parts.MobisSteering)
    assert parts.find_violations(**state) != []


def test_bosch_brake_with_non_bosch_steering_fails_test(capsys):
    state = make_state(parts.Sedan, parts.GMEngine, parts.BoschBrake, parts.MobisSteering)
    main.test_produced_car(state)
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "Bosch제동장치에는 Bosch조향장치 이외 사용 불가" in out


# 제한조건2-1: Sedan에는 Continental 제동장치 사용 불가
def test_sedan_with_continental_brake_is_invalid():
    state = make_state(parts.Sedan, parts.GMEngine, parts.ContinentalBrake, parts.MobisSteering)
    assert parts.find_violations(**state) != []


def test_sedan_with_continental_brake_fails_test(capsys):
    state = make_state(parts.Sedan, parts.GMEngine, parts.ContinentalBrake, parts.MobisSteering)
    main.test_produced_car(state)
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "Sedan에는 Continental제동장치 사용 불가" in out


# 제한조건2-2: SUV에는 TOYOTA 엔진 사용 불가
def test_suv_with_toyota_engine_is_invalid():
    state = make_state(parts.SUV, parts.ToyotaEngine, parts.MandoBrake, parts.MobisSteering)
    assert parts.find_violations(**state) != []


def test_suv_with_toyota_engine_fails_test(capsys):
    state = make_state(parts.SUV, parts.ToyotaEngine, parts.MandoBrake, parts.MobisSteering)
    main.test_produced_car(state)
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "SUV에는 TOYOTA엔진 사용 불가" in out


# 제한조건2-3: Truck에는 WIA 엔진 사용 불가
def test_truck_with_wia_engine_is_invalid():
    state = make_state(parts.Truck, parts.WIAEngine, parts.ContinentalBrake, parts.MobisSteering)
    assert parts.find_violations(**state) != []


def test_truck_with_wia_engine_fails_test(capsys):
    state = make_state(parts.Truck, parts.WIAEngine, parts.ContinentalBrake, parts.MobisSteering)
    main.test_produced_car(state)
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "Truck에는 WIA엔진 사용 불가" in out


# 제한조건2-4: Truck에는 Mando 제동장치 사용 불가
def test_truck_with_mando_brake_is_invalid():
    state = make_state(parts.Truck, parts.GMEngine, parts.MandoBrake, parts.MobisSteering)
    assert parts.find_violations(**state) != []


def test_truck_with_mando_brake_fails_test(capsys):
    state = make_state(parts.Truck, parts.GMEngine, parts.MandoBrake, parts.MobisSteering)
    main.test_produced_car(state)
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "Truck에는 Mando제동장치 사용 불가" in out


# 모든 제한조건을 만족하는 정상 조합은 PASS 되어야 한다.
@pytest.mark.parametrize(
    "car_type, engine, brake, steering",
    [
        (parts.Sedan, parts.GMEngine, parts.MandoBrake, parts.MobisSteering),
        (parts.SUV, parts.GMEngine, parts.ContinentalBrake, parts.MobisSteering),
        (parts.Truck, parts.GMEngine, parts.ContinentalBrake, parts.MobisSteering),
        (parts.Sedan, parts.GMEngine, parts.BoschBrake, parts.BoschSteering),
    ],
)
def test_valid_combinations_pass(capsys, car_type, engine, brake, steering):
    state = make_state(car_type, engine, brake, steering)
    assert parts.find_violations(**state) == []
    main.test_produced_car(state)
    out = capsys.readouterr().out
    assert "PASS" in out
