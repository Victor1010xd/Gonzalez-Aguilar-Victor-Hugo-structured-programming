def show_menu():
    print("\n=== NETFLIX ===")
    print("Select a genre:")
    print("1. Technology")
    print("2. Action")
    print("3. Science Fiction")


def get_genre():
    option = int(input("Option: "))
    return option


def recommend_content(genre):
    print("\nRecommendations:")
    if genre == 1:
        print("- The Social Dilemma")
        print("- Silicon Valley")
    elif genre == 2:
        print("- Deadly Code")
        print("- Operation Delta")
    elif genre == 3:
        print("- Interstellar")
        print("- Black Mirror")
    else:
        print("Invalid option chosen.")


keep_searching = "Y"

while keep_searching == "Y":
    show_menu()
    selected_genre = get_genre()
    recommend_content(selected_genre)
    
    print("\nWould you like to perform another search? (Y/N)")
    keep_searching = input().upper().strip()

print("Goodbye!")