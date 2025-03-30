# Description: A simple Home Affairs registration form with validation and data saving.
import flet as ft
import json

def main(page: ft.Page):
    # Set page properties for mobile-like window size
    page.title = "Home Affairs"
    page.window_full_screen = True  # Enable fullscreen mode
    page.window_resizable = True  # Allow resizing
    page.scroll = ft.ScrollMode.ALWAYS  # Enable scrolling for the entire page

    # Feedback for different fields
    gender_feedback = ft.Text(color="red", weight="bold")
    nationality_feedback = ft.Text(color="red", weight="bold")
    names_feedback = ft.Text(color="red", weight="bold")
    surname_feedback = ft.Text(color="red", weight="bold")
    id_feedback = ft.Text(color="red", weight="bold")
    ID_feedback = ft.Text(color="red", weight="bold")
    address_feedback = ft.Text(color="red", weight="bold")
    marital_feedback = ft.Text(color="red", weight="bold")
    feedback = ft.Text(color="blue", weight="bold")
    day_feedback = ft.Text(color="red", weight="bold")
    month_feedback = ft.Text(color="red", weight="bold")
    year_feedback = ft.Text(color="red", weight="bold")
    date_of_birth_feedback = ft.Row([day_feedback, month_feedback,year_feedback])

    # Clear errors when submitting the form
    def clear_feedback():
        names_feedback.value = ""
        surname_feedback.value = ""
        id_feedback.value = ""
        ID_feedback.value = ""
        address_feedback.value = ""
        gender_feedback.value = ""
        nationality_feedback.value = ""
        marital_feedback.value = ""
        day_feedback.value = ""
        month_feedback.value = ""
        year_feedback.value = ""
        date_of_birth_feedback.value = ""
        feedback.value = ""  # Nationality changed handler (to show 'Other' field)

        page.update()

    # Gender dropdown
    gender_dropdown = ft.Dropdown(
        label="Gender",
        value="Please Select",  # Default value (not in options list)
        options=[
            ft.dropdown.Option("Male"),
            ft.dropdown.Option("Female")
        ],
    )

    # Nationality dropdown
    nationality_dropdown = ft.Dropdown(
        label="Nationality",
        value="Please Select",  # Default value (not in options list)
        options=[
            ft.dropdown.Option("Black"),
            ft.dropdown.Option("Coloured"),
            ft.dropdown.Option("White"),
            ft.dropdown.Option("Indian/Asian"),
            ft.dropdown.Option("Other")
        ],
    )

    # Other Nationality input (hidden by default)
    other_nationality = ft.TextField(label="Specify Other Nationality", visible=False)

    def nationality_changed(e):
        other_nationality.visible = nationality_dropdown.value == "Other"

        page.update()
    nationality_dropdown.on_change = nationality_changed

    # Marital Status dropdown
    marital_status_dropdown = ft.Dropdown(
        label="Marital Status",
        value="Please Select",  # Default value (not in options list)
        options=[
            ft.dropdown.Option("Single"),
            ft.dropdown.Option("Married"),
            ft.dropdown.Option("Divorced"),
            ft.dropdown.Option("Widowed"),
        ],
    )

    # Date of birth Dropdown option ranges
    days = [str(x) for x in range(1, 32)]  # str since options are strings, not integers
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    years = [str(y) for y in range(1900, 2025)]  # str since options are strings, not integers
    
    # Date of Birth dropdown
    day = ft.Dropdown(label="Day", width=120, value="Please Select", options=[ft.dropdown.Option(day) for day in days])
    month = ft.Dropdown(label="Month", width=150, value="Please Select", options=[ft.dropdown.Option(month) for month in months])
    year = ft.Dropdown(label="Year", width=150, value="Please Select", options=[ft.dropdown.Option(year) for year in years])
    
    date_of_birth = ft.Row([day, ft.Text("/"), month, ft.Text("/"),year],alignment=ft.MainAxisAlignment.CENTER)  # not using ft.text gives error
    date_of_birth_label = ft.Text("Date of Birth", size=20, weight="bold")

    # Create Text input fields
    names = ft.TextField(label="First Name")
    surname = ft.TextField(label="Last Name")
    id_number = ft.TextField(label="Enter ID Number", autofocus=True)
    ID_number = ft.TextField(label="Enter ID Number", autofocus=True)
    address = ft.TextField(label="Physical Address", height=100, multiline=True)
    
    def error_handler(e):
        clear_feedback()  # Clear previous feedback
        has_errors = False  # Flag to track errors

        try:
            # Validate Names
            if not names.value.strip():  # Check if the names field is empty
                names_feedback.value = "Names cannot be empty."
                has_errors = True
            elif not names.value.replace(" ", "").isalpha():
                names_feedback.value = "Names must only contain alphabetic characters."
                has_errors = True

            # Validate Surname
            if not surname.value.strip():  # Check if the surname field is empty
                surname_feedback.value = "Surname cannot be empty."
                has_errors = True
            elif not surname.value.isalpha():
                surname_feedback.value = "Surname must only contain alphabetic characters."
                has_errors = True

            # Validate ID Number
            id_number_cleaned = id_number.value.strip()
            if not id_number_cleaned.isdigit() or len(id_number_cleaned) != 13:
                id_feedback.value = "ID Number must be 13 digits long and numeric."
                has_errors = True

            # Validate Gender selection
            if gender_dropdown.value == "Please Select":
                gender_feedback.value = "Please select a Gender."
                has_errors = True

            # Validate Date of Birth
            if day.value == "Please Select":
                day_feedback.value = "Please select a day."
                has_errors = True
            if month.value == "Please Select":
                month_feedback.value = "Please select a month."
                has_errors = True
            if year.value == "Please Select":
                year_feedback.value = "Please select a year."
                has_errors = True  

             # Validate Nationality selection
            if nationality_dropdown.value == "Please Select":
                nationality_feedback.value = "Please select a Nationality."
                has_errors = True

            # If "Other" is selected for Nationality, ensure it's filled
            if nationality_dropdown.value == "Other" and not other_nationality.value.strip():
                nationality_feedback.value = "Please specify your nationality if 'Other' is selected."
                has_errors = True

            # Validate Marital Status selection
            if marital_status_dropdown.value == "Please Select":
                marital_feedback.value = "Please select a Marital Status."
                has_errors = True

            # Validate Physical Address
            if not address.value.strip():
                address_feedback.value = "Physical Address cannot be empty."
                has_errors = True

        except Exception as e:
            feedback.value = f"Unexpected Error: {str(e)}"
            has_errors = True  # Mark an error occurred

        finally:
            page.update()

        return has_errors  # Return True if errors exist, False otherwise # Check if the user has entered a valid name
        


    # Save data to a JSON file
    def save_data(e):
        if error_handler(e):  # Check for errors
            return  # Don't save if there are errors
        user_data = "data.json"

        # Prepare the user data to be saved as a dictionary
        info = {
            "Names": names.value,
            "Surname": surname.value,
            "ID Number": id_number.value,
            "Date of Birth": f"{day.value}/{month.value}/{year.value}",
            "Gender": gender_dropdown.value,
            "Nationality": nationality_dropdown.value,
            "Marital Status": marital_status_dropdown.value,
            "Physical Address": address.value
        }
        
        try:
            new_id = id_number.value  # Get the ID from the input field to search for duplicates
            try:
                with open(user_data, 'r') as file:  # Open the file in read mode
                    data = json.load(file)  # Load existing JSON data
            except (FileNotFoundError, json.JSONDecodeError):
                data = []    #If file doesn't exist or is invalid, initialize an empty list
            
            for record in data:  # Loop through each record in the data
                if record.get("ID Number") == new_id:  # ID found
                    feedback.value = "You are already in the database."
                    page.update() 
                    return  # Exit the loop after finding the ID
            
            data.append(info)  # Append the new user info to the list
            with open(user_data, 'w') as file:  # Open the file and rewrite the updated data
                json.dump(data, file, indent=4)  # Save the list with indentation for readability
            feedback.value = "Data saved successfully!"  # Success feedback

        except Exception as e:
            feedback.value = f"Error saving data: {str(e)}"  # Error feedback

        finally:
            page.update()  # Update the page to reflect the feedback


    def search_id(e):
         # Validate ID Number
        has_errors = False  # Flag to track errors
        ID_number_cleaned = ID_number.value.strip()  # Get the input ID and remove leading/trailing spaces

        # Check if the ID field is empty
        if ID_number_cleaned == "":
            ID_feedback.value = "ID Number cannot be empty."
            has_errors = True

        # Validate if the ID is 13 digits long and numeric
        if not ID_number_cleaned.isdigit() or len(ID_number_cleaned) != 13:
            ID_feedback.value = "ID Number must be 13 digits long and numeric."
            has_errors = True

        # Exit the function if there are errors
        if has_errors:
            return

        # Get the ID from the input field to search for duplicates
        ID_to_search = ID_number_cleaned
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
            
            for record in data:  # Loop through each record in the data
                if record.get("ID Number") == ID_to_search:  # ID found
                    feedback.value = "You are already in the database." 
                    return  # Exit the loop after finding the ID
                
            id_feedback.value = "You are not in the database. Please REGISTER."
            

        except FileNotFoundError:
            feedback.value = "The file 'data.json' was not found."
        except json.JSONDecodeError:
            feedback.value = "Error decoding JSON. The file might be corrupted."
        except Exception as e:
            feedback.value = f"An unexpected error occurred: {e}"
        finally:    
            page.update()

    def print_data(e):  # PRINT all users info on terminal
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
            print(data)  # Print the contents of the file
            
        except FileNotFoundError:
            print("The file 'data.json' was not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON. The file might be corrupted.")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

    def print_summary(e):  # PRINT all users' info on terminal
      # Read data once
        with open("data.json", "r") as file:
            data = json.load(file)

        # Count genders
        male_count = sum(1 for record in data if record.get("Gender") == "Male")
        female_count = sum(1 for record in data if record.get("Gender") == "Female")

        print(f"Male: {male_count}")
        print(f"Female: {female_count}")
                # Count nationalities
        nationality_counts = {
        "Black": sum(1 for record in data if record.get("Nationality") == "Black"),
        "White": sum(1 for record in data if record.get("Nationality") == "White"),  
        "Coloured": sum(1 for record in data if record.get("Nationality") == "Coloured"),
        "Indian/Asian": sum(1 for record in data if record.get("Nationality") == "Indian/Asian"),
        "Other": sum(1 for record in data if record.get("Nationality") == "Other")
        }

        # Find the most common nationality
        highest_nationality = max(nationality_counts, key=nationality_counts.get)
        highest_count = nationality_counts[highest_nationality]

        print(f"{highest_nationality} is most common among users with ({highest_count} people)")



    def go_to_second_page(e):
        page.go("/second")

    def go_home(e):
        page.go("/")

    def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    controls=[
                        ft.Text("Welcome To The Department Of Home Affairs", size=20, weight="bold"),
                        ID_number,
                        ID_feedback,
                        feedback,
                        ft.Row([
                            ft.ElevatedButton("Search", on_click=search_id),
                            ft.ElevatedButton("REGISTER", on_click=go_to_second_page),  
                            ft.ElevatedButton("Print Data", on_click=print_data),
                            ft.ElevatedButton("Print Summary", on_click=print_summary)
                        ])
                    ]
                )
            )

        elif page.route == "/second":
            page.views.append(
                ft.View(
                    "/second",
                    controls=[
                        ft.Text("Home Affairs Main Window", size=28, weight="bold"),
                        ft.Row([
                            ft.Column([  # Left side column
                                id_number,
                                id_feedback,
                                names,
                                names_feedback,
                                surname,
                                surname_feedback,
                                address,
                                address_feedback,
                                date_of_birth_label,
                                date_of_birth,date_of_birth_feedback,
                                ], width=350),  # Adjust width to control space
                            # Right side column
                            ft.Column([
                                gender_dropdown, gender_feedback,
                                marital_status_dropdown, marital_feedback,
                                nationality_dropdown, nationality_feedback,
                                other_nationality,
                            ], width=350),  # Adjust width to control space
                        ]),  # Close Row list
                        ft.Row([
                            ft.ElevatedButton("Back to Home", on_click=go_home),
                            ft.ElevatedButton("Save", on_click=save_data)
                        ]),  # close Row list
                        feedback
                    ]
                )
            )

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
