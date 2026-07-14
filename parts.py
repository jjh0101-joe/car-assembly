from abc import ABC, abstractmethod


class CarType(ABC):
    name = ""


class Sedan(CarType):
    name = "Sedan"


class SUV(CarType):
    name = "SUV"


class Truck(CarType):
    name = "Truck"


class Engine(ABC):
    name = ""
    broken = False

    @abstractmethod
    def is_compatible_with(self, car_type):
        raise NotImplementedError


class GMEngine(Engine):
    name = "GM"

    def is_compatible_with(self, car_type):
        return True


class ToyotaEngine(Engine):
    name = "TOYOTA"

    def is_compatible_with(self, car_type):
        return not isinstance(car_type, SUV)


class WIAEngine(Engine):
    name = "WIA"

    def is_compatible_with(self, car_type):
        return not isinstance(car_type, Truck)


class BrokenEngine(Engine):
    name = "고장난 엔진"
    broken = True

    def is_compatible_with(self, car_type):
        return True


class BrakeSystem(ABC):
    name = ""

    @abstractmethod
    def is_compatible_with_car(self, car_type):
        raise NotImplementedError

    def is_compatible_with_steering(self, steering):
        return True


class MandoBrake(BrakeSystem):
    name = "Mando"

    def is_compatible_with_car(self, car_type):
        return not isinstance(car_type, Truck)


class ContinentalBrake(BrakeSystem):
    name = "Continental"

    def is_compatible_with_car(self, car_type):
        return not isinstance(car_type, Sedan)


class BoschBrake(BrakeSystem):
    name = "Bosch"

    def is_compatible_with_car(self, car_type):
        return True

    def is_compatible_with_steering(self, steering):
        return isinstance(steering, BoschSteering)


class SteeringSystem(ABC):
    name = ""


class BoschSteering(SteeringSystem):
    name = "Bosch"


class MobisSteering(SteeringSystem):
    name = "Mobis"


CAR_TYPES = {1: Sedan, 2: SUV, 3: Truck}
ENGINES = {1: GMEngine, 2: ToyotaEngine, 3: WIAEngine, 4: BrokenEngine}
BRAKE_SYSTEMS = {1: MandoBrake, 2: ContinentalBrake, 3: BoschBrake}
STEERING_SYSTEMS = {1: BoschSteering, 2: MobisSteering}


def find_violations(car_type, engine, brake, steering):
    violations = []
    if not engine.is_compatible_with(car_type):
        violations.append(f"{car_type.name}에는 {engine.name}엔진 사용 불가")
    if not brake.is_compatible_with_car(car_type):
        violations.append(f"{car_type.name}에는 {brake.name}제동장치 사용 불가")
    if not brake.is_compatible_with_steering(steering):
        violations.append(f"{brake.name}제동장치에는 Bosch조향장치 이외 사용 불가")
    return violations
