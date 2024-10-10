from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
   # create_patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the patient
    patient = Patient(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)



def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False

def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
     # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_patient= patient



def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    """
    TODO: Part 2
    """
    #  search_caregiver_schedule <date>
    #  check 1: check if there is a current logged-in user
    global current_caregiver
    global current_patient
    if (current_caregiver is None) and (current_patient is None):
        print("Please login first!")
        return

    # check 2: the length for tokens need to be exactly 1 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    # check 3: tokens[1] should be a date
    if (len(tokens[1]) != 10) or (tokens[1][2] != "-") or (tokens[1][5] != "-"):
        print("Please try again, date should be in the format mm-dd-yyyy!")
        return

    if (int(tokens[1][:2]) > 12) or (int(tokens[1][3:5]) > 31):
        print("Please try again, date is not valid!")
        return

    date = tokens[1]
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])

    cm_caregiver = ConnectionManager()
    conn_caregiver = cm_caregiver.create_connection()
    cursor_caregiver = conn_caregiver.cursor(as_dict=True)

    cm_vaccine = ConnectionManager()
    conn_vaccine = cm_vaccine.create_connection()
    cursor_vaccine = conn_vaccine.cursor(as_dict=True)

    caregivers_availability = "SELECT * FROM Availabilities " \
                              "WHERE Time = %s " \
                              "ORDER BY Username"
    vaccines_availability = "SELECT * FROM Vaccines"

    try:
        d = datetime.datetime(year, month, day)
        cursor_caregiver.execute(caregivers_availability, d)
        print("Available caregivers:")
        name = None
        for row in cursor_caregiver:
            name = row['Username']
            print(name)
        if name is None:
            print('None')

        # Number of available doses left for each vaccine
        cursor_vaccine.execute(vaccines_availability)
        print("Available vaccines:")
        for row in cursor_vaccine:
            print(row['Name'], " ", row['Doses'])

    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please try again!")
    except Exception as e:
        print("Please try again!")
        print("Error:", e)

    finally:
        cm_caregiver.close_connection()
        cm_vaccine.close_connection()
    return

      
    

def reserve(tokens):
    """
    TODO: Part 2
    """
    # reserve <date> <vaccine>
    global current_patient
    global current_caregiver

    # check 1: check if the logged-in user is a patient
    if current_caregiver is None and current_patient is None:
        print("Please login first!")
        return

    if current_patient is None:
        print("Please login as a patient!")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    # check 3: tokens[1] should be a date
    if (len(tokens[1]) != 10) or (tokens[1][2] != "-") or (tokens[1][5] != "-"):
        print("Please try again, date should be in the format mm-dd-yyyy!")
        return

    if (int(tokens[1][:2]) > 12) or (int(tokens[1][3:5]) > 31):
        print("Please try again, date is not valid!")
        return

    date = tokens[1]
    # input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])

    vaccine_name = tokens[2]

    cm_caregiver = ConnectionManager()
    conn_caregiver = cm_caregiver.create_connection()
    cursor_caregiver = conn_caregiver.cursor(as_dict=True)

    cm_vaccine = ConnectionManager()
    conn_vaccine = cm_vaccine.create_connection()
    cursor_vaccine = conn_vaccine.cursor(as_dict=True)

    cm_appointment = ConnectionManager()
    conn_appointment = cm_appointment.create_connection()
    cursor_appointment = conn_appointment.cursor(as_dict=True)

    select_caregiver = "SELECT TOP 1 Username FROM Availabilities " \
                            "WHERE Time = %s " \
                            "ORDER BY Username"
    select_vaccine = "SELECT Doses FROM Vaccines " \
                            "WHERE Name = %s"
    select_appointment = "SELECT TOP 1 ID FROM Appointments " \
                            " ORDER BY ID DESC"

    try:
        d = datetime.datetime(year, month, day)
        cursor_caregiver.execute(select_caregiver, d)
        assigned_caregiver = None
        for row in cursor_caregiver:
            assigned_caregiver = row['Username']

        # check if there is an available caregiver
        if assigned_caregiver is None:
            print("No Caregiver is available!")
            cm_caregiver.close_connection()
            cm_vaccine.close_connection()
            cm_appointment.close_connection()
            return

        print('step1: ', assigned_caregiver)

        cursor_vaccine.execute(select_vaccine, vaccine_name)
        # check if there is enough doses
        get_vaccine = cursor_vaccine.fetchone()
        if get_vaccine is None:
            print('Not enough available doses!')
            cm_caregiver.close_connection()
            cm_vaccine.close_connection()
            cm_appointment.close_connection()
            return
        doses = get_vaccine['Doses']
        # check if there is enough doses
        if doses < 1:
            print('Not enough available doses!')
            cm_caregiver.close_connection()
            cm_vaccine.close_connection()
            cm_appointment.close_connection()
            return

        print('step2: ', doses)

        # get appointment id
        cursor_appointment.execute(select_appointment)
        appointmentID = 0
        for row in cursor_appointment:
            appointmentID = row['ID']
        appointmentID = int(appointmentID) + 1

        print('step3:', appointmentID)

    except pymssql.Error as e:
        print("Error occurred")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
    finally:
        cm_caregiver.close_connection()
        cm_vaccine.close_connection()
        cm_appointment.close_connection()

    print("Appointment ID: {}, Caregiver username: {}".format(appointmentID, assigned_caregiver))

    # insert all the information into Appointments table
    cm_insert = ConnectionManager()
    conn_insert = cm_insert.create_connection()
    cursor_insert = conn_insert.cursor()
    insert_appointments = "INSERT INTO Appointments VALUES (%s, %s, %s, %s, %s)"

    try:
        cursor_insert.execute(insert_appointments, (appointmentID, current_patient.username, assigned_caregiver, vaccine_name, d))
        conn_insert.commit()
    except pymssql.Error as e:
        print("Error occurred")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
    finally:
        cm_insert.close_connection()

    # delete everything that need to be deleted, remove caregiver and decrease dose
    cm_remove = ConnectionManager()
    conn_remove = cm_remove.create_connection()
    cursor_remove = conn_remove.cursor()
    delete_caregiver = "DELETE FROM Availabilities " \
                        "WHERE Username = %s AND Time = %s"
    try:
        cursor_remove.execute(delete_caregiver, (assigned_caregiver, d))
        conn_remove.commit()
        vaccine = Vaccine(vaccine_name, doses)
        vaccine.decrease_available_doses(1)

    except pymssql.Error as e:
        print("Error occurred")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
    finally:
         cm_remove.close_connection()
    return



def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    """
    TODO: Extra Credit
    """
    pass


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    '''
    TODO: Part 2
    '''
    # show_appointments
    global current_caregiver
    global current_patient

    #  check 1: the length for tokens need to be exactly 1
    if len(tokens) != 1:
        print("Please try again!")
        return

    # check 2: check if the user's already logged in
    if current_caregiver is None and current_patient is None:
        print('Please login first!')
        return

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    if current_caregiver is not None:
        appointment_for_caregivers = "SELECT ID, Vname AS vaccine_name, Time , Pname AS patient_name " \
                                   "FROM Appointments " \
                                   "WHERE Cname = %s " \
                                   "ORDER BY ID"
        try:
            cursor.execute(appointment_for_caregivers, current_caregiver.username)
            for row in cursor:
                print(row['ID'], " ", row['vaccine_name'], " ", row['Time'], " ", row['patient_name'])

        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()
        return

    else:
        appointment_for_patients = "SELECT ID, Vname AS vaccine_name, Time , Cname AS caregiver_name " \
                                     "FROM Appointments " \
                                     "WHERE Pname = %s " \
                                     "ORDER BY ID"

        try:
            cursor.execute(appointment_for_patients, current_patient.username)
            for row in cursor:
                print(row['ID'], " ", row['vaccine_name'], " ", row['Time'], " ", row['caregiver_name'])

        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()
        return


    

def logout(tokens):
    """
    TODO: Part 2
    """
    global current_caregiver
    global current_patient
    if len(tokens)!=1:
        print("Please try again!")
        return
    if current_caregiver is None and current_patient is None:
        print("Pleasw login first!")
        return
    if current_caregiver is not None or current_patient is not None:
        current_caregiver = None
        current_patient = None
        print('Successfully logged out!')
        return
    else:
        print('Please try again!')
        
        return
    
    
def strong_password(password):
    
       # a. at least 8 characters
       if len(password) < 8:
           print("Please try again, a strong password should have at least 8 characters!")
           return False

       # b. a mixture of both uppercase and lowercase letters
       with_uppercase = False
       with_lowercase = False
       for char in password:
           if char.isupper():
               with_uppercase = True
           elif char.islower():
               with_lowercase = True
       if (not with_uppercase) or (not with_lowercase):
           print("Please try again, a strong password should be a mixture of both uppercase and lowercase letters!")
           return False
       #c. with a mixture of letters and numbers
       with_number=False
       with_letter=False
       for char in password:
           if char.isalpha():
               with_letter=True
           elif char.isdigit():
               with_number=True
           if (not with_letter) or (not with_number):
               print("Please try again, a strong password should be a mixture of both numbers and letters!")
               return False
      # d. inclusion of at least one special character, from "!","@", "#", "?"
       special_characters=["!","@","#","?"]
       with_special_char=False
       for char in password:
          if char in special_characters:
              with_special_char=True
              break
       if not with_special_char:
         print("Please try again, a strong password should include at least one special character")
         return False
       return True
      


        
       
            
            
        
    

def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == cancel:
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
