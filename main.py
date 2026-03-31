import csv
from collections import Counter
from car import Car
from database import (
    initialize_database, import_cars, add_car, get_all_cars,
    get_car_by_id, update_car, delete_car, search_cars
)

def show_menu():
    print("\n" + "="*40)
    print("   🚗  CAR DEALERSHIP MANAGER")
    print("="*40)
    print("1. Add Car")
    print("2. View All Cars")
    print("3. Update Car")
    print("4. Delete Car")
    print("5. Search Cars")
    print("6. Statistics")
    print("7. Filter by price")
    print("8. Export inventory to CSV")
    print("9. Exit")
    return input("Make your choice:\n").strip()


def add_car_flow():
    try:
        make = input("Make: ")
        model = input("Model: ")
        year = int(input("Year: "))
        price = float(input("Price: "))
        mileage = int(input("Mileage: "))

        car = Car(make, model, year, price, mileage)
        add_car(car)

        print(f"Car added successfully (ID:{car.id})")
    except ValueError as e:
        print(f"Invalid input: {e}")


def view_all_cars_flow():
    cars = get_all_cars()
    if not cars:
        print("No cars in inventory.")
        return

    print("\n Sort by:")
    print("1. Price low → high")
    print("2. Price high → low")
    print("3. Year newest → oldest")
    print("4. Year oldest → newest")
    print("5. No sorting / default")
    
    choice = input("Choose sorting option: ").strip()
    
    if choice == "1":
        cars.sort(key=lambda c: c.price)
    elif choice == "2":
        cars.sort(key=lambda c: c.price, reverse=True)
    elif choice == "3":
        cars.sort(key=lambda c: c.year, reverse=True)
    elif choice == "4":
        cars.sort(key=lambda c: c.year)
    
    print("\n Inventory:")
    for car in cars:
        print(car)


def update_car_flow():
    try:
        car_id = int(input("Enter car ID to update: "))
    except ValueError:
        print("Invalid ID")
        return

    car = get_car_by_id(car_id)
    if not car:
        print("Car not found")
        return

    print(f"\n Current details:\n{car}\n")
    print("Enter new values (press Enter to keep current)")

    new_make = input(f"Make [{car.make}]: ").strip()
    if new_make:
        car.make = new_make

    new_model = input(f"Model [{car.model}]: ").strip()
    if new_model:
        car.model = new_model

    new_year = input(f"Year [{car.year}]: ").strip()
    if new_year:
        try:
            car.year = int(new_year)
        except ValueError:
            print("Invalid year input, keeping old value")

    new_price = input(f"Price [{car.price}]: ").strip()
    if new_price:
        try:
            car.price = float(new_price)
        except ValueError:
            print("Invalid price input, keeping old value")

    new_mileage = input(f"Mileage [{car.mileage}]: ").strip()
    if new_mileage:
        try:
            car.mileage = int(new_mileage)
        except ValueError:
            print("Invalid mileage input, keeping old value")

    try:
        update_car(car)
        print("Car updated successfully")
    except ValueError as e:
        print(f"Error updating car: {e}")


def delete_car_flow():
    try:
        car_id = int(input("Enter car ID to delete: "))
    except ValueError:
        print("Invalid ID")
        return

    car = get_car_by_id(car_id)
    if not car:
        print("Car not found")
        return

    print(f"\n Selected car:\n{car}")
    confirm = input("Are you sure you want to delete this car? (y/n): ").strip().lower()

    if confirm == "y":
        success = delete_car(car_id)
        if success:
            print("Car deleted successfully")
        else:
            print("Car could not be deleted")
    else:
        print("Deletion cancelled")


def search_cars_flow():
    keyword = input("Enter search keyword: ").strip()
    if not keyword:
        print("No keyword entered")
        return

    results = search_cars(keyword)
    if not results:
        print("No matching cars found")
        return

    print(f"\n Found {len(results)} car(s):")
    for car in results:
        print(car)


def show_statistics():
    cars = get_all_cars()
    if not cars:
        print("No cars in inventory.")
        return

    total = len(cars)
    avg_price = sum(c.price for c in cars) / total

    makes = [c.make for c in cars if c.make] 
    most_common_make = Counter(makes).most_common(1)[0][0] if makes else "N/A"

    print("\n Inventory Statistics:")
    print(f"Total cars: {total}")
    print(f"Average price: ${avg_price:,.2f}")
    print(f"Most common make: {most_common_make}")


def price_filter_flow():
    try:
        max_price = float(input("Show cars under price $: "))
    except ValueError:
        print("Invalid price")
        return

    cars = get_all_cars()
    filtered = [c for c in cars if c.price <= max_price]

    if not filtered:
        print(f"No cars under ${max_price:,.2f}")
        return

    print(f"\n Cars under ${max_price:,.2f}:")
    for car in filtered:
        print(car)


def export_to_csv():
    cars = get_all_cars()
    if not cars:
        print("No cars to export.")
        return

    filename = input("Enter filename (e.g., inventory.csv): ").strip()
    if not filename:
        filename = "inventory.csv"

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Make", "Model", "Year", "Price", "Mileage"])
        for c in cars:
            writer.writerow([c.id, c.make, c.model, c.year, c.price, c.mileage])

    print(f"Inventory exported to {filename}")


def main():
    initialize_database()
    import_cars()

    while True:
        choice = show_menu()
        if choice == "1":
            add_car_flow()
        elif choice == "2":
            view_all_cars_flow()
        elif choice == "3":
            update_car_flow()
        elif choice == "4":
            delete_car_flow()
        elif choice == "5":
            search_cars_flow()
        elif choice == "6":
            show_statistics()
        elif choice == "7":
            price_filter_flow()
        elif choice == "8":
            export_to_csv()    
        elif choice == "9":
            print("Goodbye! 👋")
            break
        
        else:
            print("Invalid choice. Please enter 1–9.")


if __name__ == "__main__":
    main()