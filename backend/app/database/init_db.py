from app.models.database import Base, engine, SessionLocal
from app.models.database import Machine, Operator
from app.core.security import get_password_hash

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Örnek makineler
    machines = [
        Machine(name="Pres Makinesi 1", type="press", ideal_cycle_time=2.5),
        Machine(name="Kaynak Makinesi 1", type="welding", ideal_cycle_time=1.8),
        Machine(name="Enjeksiyon Makinesi 1", type="injection", ideal_cycle_time=3.2),
    ]
    
    for machine in machines:
        db.add(machine)
    
    # Örnek operatör
    operator = Operator(
        name="Ahmet Yılmaz",
        email="ahmet@fabrika.com",
        password_hash=get_password_hash("operator123"),
        role="operator"
    )
    db.add(operator)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized with sample data")
