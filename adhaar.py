import random
import csv

def generate_fake_aadhaar_number():
    # Generates a 12-digit random number (not real, no Verhoeff validation)
    return f"{random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}"

def generate_fake_entry():
    names = ["Priya Sharma", "Aditi Verma", "Sanya Khan", "Kavya Nair", "Ishita Das"]
    genders = ["Female"]
    years = [str(random.randint(1985, 2005)) for _ in range(5)]
    
    return {
        "Name": random.choice(names),
        "Gender": random.choice(genders),
        "DOB": f"{random.choice(years)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        "Aadhaar Number": generate_fake_aadhaar_number(),
        "Masked Aadhaar": "XXXX-XXXX-" + generate_fake_aadhaar_number()[-4:]
    }

# Generate dataset
with open("synthetic_aadhaar_dataset.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Gender", "DOB", "Aadhaar Number", "Masked Aadhaar"])
    writer.writeheader()
    for _ in range(1000):  # Adjust count as needed
        writer.writerow(generate_fake_entry())
