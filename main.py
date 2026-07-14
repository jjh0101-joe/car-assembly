import time
import sys

from parts import CAR_TYPES, ENGINES, BRAKE_SYSTEMS, STEERING_SYSTEMS, find_violations

CLEAR_SCREEN = "\033[H\033[2J"

CarType_Q = 0
Engine_Q = 1
brakeSystem_Q = 2
SteeringSystem_Q = 3
Run_Test = 4

LABELS = {
    CarType_Q: "차량 타입",
    Engine_Q: "엔진",
    brakeSystem_Q: "제동장치",
    SteeringSystem_Q: "조향장치",
}

STATE_KEYS = {
    CarType_Q: ("car_type", CAR_TYPES),
    Engine_Q: ("engine", ENGINES),
    brakeSystem_Q: ("brake", BRAKE_SYSTEMS),
    SteeringSystem_Q: ("steering", STEERING_SYSTEMS),
}


def new_state():
    return {"car_type": None, "engine": None, "brake": None, "steering": None}


def delay(ms):
    t = ms / 1000.0
    time.sleep(t)


def clear():
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def show_menu(step):
    clear()
    if step == CarType_Q:
        print("        ______________")
        print("       /|            |")
        print("  ____/_|_____________|____")
        print(" |                      O  |")
        print(" '-(@)----------------(@)--'")
        print("===============================")
        print("어떤 차량 타입을 선택할까요?")
        for num, cls in CAR_TYPES.items():
            print(f"{num}. {cls.name}")
    elif step in STATE_KEYS:
        print(f"어떤 {LABELS[step]}을(를) 선택할까요?")
        print("0. 뒤로가기")
        _, registry = STATE_KEYS[step]
        for num, cls in registry.items():
            print(f"{num}. {cls.name}")
    elif step == Run_Test:
        print("멋진 차량이 완성되었습니다.")
        print("0. 처음 화면으로 돌아가기")
        print("1. RUN")
        print("2. Test")
    print("===============================")


def is_valid_range(step, ans):
    if step == CarType_Q:
        if ans < 1 or ans > len(CAR_TYPES):
            print(f"ERROR :: {LABELS[step]}은(는) 1 ~ {len(CAR_TYPES)} 범위만 선택 가능")
            return False
    elif step in STATE_KEYS:
        _, registry = STATE_KEYS[step]
        if ans < 0 or ans > len(registry):
            print(f"ERROR :: {LABELS[step]}은(는) 0 ~ {len(registry)} 범위만 선택 가능")
            return False
    elif step == Run_Test:
        if ans < 0 or ans > 2:
            print("ERROR :: Run 또는 Test 중 하나를 선택 필요")
            return False
    return True


def select(step, ans, state):
    key, registry = STATE_KEYS[step]
    instance = registry[ans]()
    state[key] = instance
    print(f"{LABELS[step]}으로 {instance.name}을(를) 선택하셨습니다.")


def run_produced_car(state):
    violations = find_violations(state["car_type"], state["engine"], state["brake"], state["steering"])
    if violations:
        print("자동차가 동작되지 않습니다")
        return
    if state["engine"].broken:
        print("엔진이 고장나있습니다.")
        print("자동차가 움직이지 않습니다.")
        return

    print(f"Car Type : {state['car_type'].name}")
    print(f"Engine   : {state['engine'].name}")
    print(f"Brake    : {state['brake'].name}")
    print(f"Steering : {state['steering'].name}")
    print("자동차가 동작됩니다.")


def test_produced_car(state):
    violations = find_violations(state["car_type"], state["engine"], state["brake"], state["steering"])
    if violations:
        print(f"FAIL\n{violations[0]}")
    else:
        print("PASS")


def main():
    step = CarType_Q
    state = new_state()
    while True:
        show_menu(step)
        buf = input("INPUT > ").strip()

        if buf == "exit":
            print("바이바이")
            break

        try:
            ans = int(buf)
        except ValueError:
            print("ERROR :: 숫자만 입력 가능")
            delay(800)
            continue

        if not is_valid_range(step, ans):
            delay(800)
            continue

        if ans == 0:
            if step == Run_Test:
                step = CarType_Q
            elif step > CarType_Q:
                step -= 1
            continue

        if step in STATE_KEYS:
            select(step, ans, state)
            delay(800)
            step += 1
        elif step == Run_Test:
            if ans == 1:
                run_produced_car(state)
                delay(2000)
            elif ans == 2:
                print("Test...")
                delay(1500)
                test_produced_car(state)
                delay(2000)


if __name__ == "__main__":
    main()
