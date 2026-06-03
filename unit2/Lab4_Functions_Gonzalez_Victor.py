def generate_email(name,lastname):
    email=name.lower()+lastname.lower()+"@utd.edu.mx"
    return email

another = "yes"
while another == "yes":
    print("Welcome to the institutional email generator!")
    name = input("Enter your name: ")
    lastname = input("Enter your last name: ")
    print("Your institutional email is: "+generate_email(name,lastname))
    another= input("Do you want to generate another email? (yes/no): ").lower()
if another == "no":
    print("Thank you for using the institutional email generator. Goodbye!")