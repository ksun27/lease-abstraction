import pandas as pd
import numpy as np
from faker import Faker
fake = Faker()

# Generate synthetic lease data
num_leases = 100

# Helper function to generate rent history
def generate_rent_history():
    return [round(np.random.uniform(500, 5000), 2) for _ in range(np.random.randint(1, 5))]

# Helper function for financial records score
def financial_records_score():
    return np.random.randint(300, 850)

# Helper function for generating landlord legal identity and contact
def landlord_info():
    return fake.company(), fake.phone_number()

# Generating data
data = {
    "Tenant Full Name": [fake.name() for _ in range(num_leases)],
    "Tenant Current Address": [fake.address() for _ in range(num_leases)],
    # incorrect, should be previous rental leases attached in pdf form
    "Rent History": [generate_rent_history() for _ in range(num_leases)],
    # incorrect, should be pdfs of offer letters, bank stubs, etc.
    "Financial Records Score": [financial_records_score() for _ in range(num_leases)],
    "Landlord Legal Identity": [landlord_info()[0] for _ in range(num_leases)],
    "Landlord Contact Information": [landlord_info()[1] for _ in range(num_leases)],
    "Base Rent": np.random.uniform(500, 5000, num_leases).round(2),
    "Total Price": np.random.uniform(1000, 7000, num_leases).round(2),
    # incorrect, should be textual data explaining tenant rights
    "Tenant Rights": np.random.randint(1, 10, num_leases),
    # incorrect, should be textual data explaining landlord responsibilities
    "Landlord Responsibilities": np.random.randint(1, 10, num_leases),
    # incorrect, should be which parties are liable for which taxes
    "Taxes Responsibility": np.random.choice(["Tenant", "Landlord"], num_leases),
    # incorrect, should be description of reimbursements tenant is responsible for to landlord
    "Reimbursements": np.random.uniform(100, 1000, num_leases).round(2),
    "Property Description": [fake.sentence() for _ in range(num_leases)],
    "Title Insurance": np.random.choice(["Yes", "No"], num_leases),
    "Security Deposit": np.random.uniform(500, 3000, num_leases).round(2),
    "Lease Start Date": [fake.date_between(start_date="-3y", end_date="today") for _ in range(num_leases)],
    "Lease Expiration Date": [fake.date_between(start_date="today", end_date="+3y") for _ in range(num_leases)],
    # incorrect, should be description of permissible uses of the leased property
    "Permissible Uses": [fake.word() for _ in range(num_leases)],
    "Termination Notice Period": np.random.randint(30, 180, num_leases),
    # incorrect, should be description of additional provisions
    "Additional Provisions": np.random.randint(1, 10, num_leases)
}

df = pd.DataFrame(data)

df.head()  # Displaying the first few rows to check the generated data
