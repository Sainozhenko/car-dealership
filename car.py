class Car:
    def __init__(self, make, model, year, price, mileage, id=None):
        if year <1912:
            raise ValueError("Invalid year") 
        from datetime import datetime
        current_year = datetime.now().year
        
        if year > current_year:
            raise ValueError("Year cannot be in the future")
        if not make or not model:
            raise ValueError("Cannot be empty!")
        if price < 0:
            raise ValueError("Price couldn't be negative.")
        if mileage < 0:
            raise ValueError("Mileage couldn't be negative.")

        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.mileage = mileage

    def __str__(self):
        id_part = f"[ID: {self.id}] " if self.id is not None else ""
        return f"{id_part}{self.year} {self.make} {self.model} | ${self.price:,.2f} | {self.mileage:,} km"

    def to_tuple(self):
        return (self.make, self.model, self.year, self.price, self.mileage)



## Test 3 methods....
if __name__ == "__main__":
    car1 = Car("Toyota", "Camry", 1912, 24999.99, 15000)
    car2 = Car("BMW", "X5", 2027, 55999.99, 8000, 7)

    print(car1)
    print(car2)

    print(car1.to_tuple())
    print(car2.to_tuple())