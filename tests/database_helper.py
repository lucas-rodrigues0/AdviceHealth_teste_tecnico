from models import Customer, Car, ModelEnum, ColorEnum, Session


def seed_database():
    """Insert some data for development and testing"""
    session = Session()

    customer1 = Customer(name="Joao Silva", email="joaomail@email.com")
    customer2 = Customer(name="Helena Castro", email="hcastro@email.com")
    customer3 = Customer(name="Renata Barreto", email="re.barreto@email.com")
    customer4 = Customer(name="Rafael Xavier", email="")
    car1 = Car(model=ModelEnum.convertible, color=ColorEnum.gray, owner=customer2)
    car2 = Car(model=ModelEnum.hatch, color=ColorEnum.yellow, owner=customer4)
    car3 = Car(model=ModelEnum.sedan, color=ColorEnum.blue, owner=customer4)
    car4 = Car(model=ModelEnum.convertible, color=ColorEnum.blue, owner=customer1)
    car5 = Car(model=ModelEnum.sedan, color=ColorEnum.gray, owner=customer4)

    try:
        session.add(customer1)
        session.add(customer2)
        session.add(customer3)
        session.add(customer4)
        session.flush()

        session.add(car1)
        session.add(car2)
        session.add(car3)
        session.add(car4)
        session.add(car5)

        session.commit()

    except Exception as err:
        print(err)
