import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide"
)

# Store data
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "patients" not in st.session_state:
    st.session_state.patients = []

if "appointments" not in st.session_state:
    st.session_state.appointments = []

if "bills" not in st.session_state:
    st.session_state.bills = []

def login():

    st.title("🏥 Hospital Management System")
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    role = st.selectbox(
        "Role",
        ["Admin", "Doctor", "Nurse", "Receptionist"]
    )

    if st.button("Login", use_container_width=True):

        if username and password:

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role

            st.rerun()

        else:
            st.error("Enter username and password.")


def patients():

    return [p["Name"] for p in st.session_state.patients]

def dashboard():

    st.title("🏥 Dashboard")
    st.write("Welcome to the Hospital Management System.")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Patients", len(st.session_state.patients))
    c2.metric("Appointments", len(st.session_state.appointments))
    c3.metric("Available Beds", 24)
    c4.metric("Bills", len(st.session_state.bills))

    st.divider()

    st.subheader("Quick Actions")

    st.info("👤 Patient Registration")
    st.info("📅 Appointment Management")
    st.info("💳 Billing & Payment")

def patient_registration():

    st.title("👤 Patient Registration")

    with st.form("patient_form"):

        name = st.text_input("Patient Name")
        age = st.number_input("Age", 0, 120, 18)
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )
        phone = st.text_input("Phone")
        address = st.text_area("Address")

        blood = st.selectbox(
            "Blood Group",
            ["Unknown", "A+", "A-", "B+", "B-",
             "AB+", "AB-", "O+", "O-"]
        )

        history = st.text_area("Medical History")

        save = st.form_submit_button(
            "Register Patient",
            use_container_width=True
        )

    if save:

        if not name:
            st.error("Enter patient name.")

        else:

            patient_id = f"P{len(st.session_state.patients)+1:04d}"

            st.session_state.patients.append({
                "ID": patient_id,
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Phone": phone,
                "Address": address,
                "Blood": blood,
                "History": history
            })

            st.success(
                f"Patient registered! ID: {patient_id}"
            )

    if st.session_state.patients:

        st.subheader("Registered Patients")

        st.dataframe(
            st.session_state.patients,
            use_container_width=True
        )

def appointments():

    st.title("📅 Appointments")

    names = patients()

    if not names:
        st.warning("Register a patient first.")
        return

    patient = st.selectbox("Patient", names)
    doctor = st.text_input("Doctor Name")

    department = st.selectbox(
        "Department",
        [
            "General Medicine",
            "Cardiology",
            "Neurology",
            "Orthopedics",
            "Pediatrics"
        ]
    )

    appointment_date = st.date_input(
        "Date",
        min_value=date.today()
    )

    if st.button(
        "Book Appointment",
        use_container_width=True
    ):

        if not doctor:
            st.error("Enter doctor name.")

        else:

            st.session_state.appointments.append({
                "Patient": patient,
                "Doctor": doctor,
                "Department": department,
                "Date": str(appointment_date)
            })

            st.success("Appointment booked!")

    if st.session_state.appointments:

        st.dataframe(
            st.session_state.appointments,
            use_container_width=True
        )

def medical_records():

    st.title("🩺 Medical Records")

    names = patients()

    if not names:
        st.warning("Register a patient first.")
        return

    patient = st.selectbox("Patient", names)

    diagnosis = st.text_area("Diagnosis")
    treatment = st.text_area("Treatment")
    prescription = st.text_area("Prescription")

    if st.button(
        "Save Record",
        use_container_width=True
    ):

        if diagnosis or treatment or prescription:
            st.success(
                f"Medical record saved for {patient}."
            )
        else:
            st.error("Enter medical information.")


# -------------------- LABORATORY --------------------

def laboratory():

    st.title("🧪 Laboratory")

    names = patients()

    if not names:
        st.warning("Register a patient first.")
        return

    patient = st.selectbox("Patient", names)

    test = st.selectbox(
        "Test",
        [
            "Blood Test",
            "Urine Test",
            "X-Ray",
            "ECG",
            "CT Scan"
        ]
    )

    status = st.selectbox(
        "Status",
        ["Requested", "In Progress", "Completed"]
    )

    result = st.text_area("Result")

    if st.button(
        "Save Laboratory Record",
        use_container_width=True
    ):

        st.success(
            f"{test} saved for {patient}."
        )

def pharmacy():

    st.title("💊 Pharmacy")

    names = patients()

    if not names:
        st.warning("Register a patient first.")
        return

    patient = st.selectbox("Patient", names)

    medicine = st.text_input("Medicine")
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1
    )

    available = st.selectbox(
        "Availability",
        ["Available", "Out of Stock"]
    )

    if st.button(
        "Dispense Medicine",
        use_container_width=True
    ):

        if not medicine:
            st.error("Enter medicine name.")

        elif available == "Out of Stock":
            st.error("Medicine is out of stock.")

        else:
            st.success(
                f"{quantity} × {medicine} given to {patient}."
            )

def billing():

    st.title("💳 Billing & Payment")

    names = patients()

    if not names:
        st.warning("Register a patient first.")
        return

    patient = st.selectbox("Patient", names)

    consultation = st.number_input(
        "Consultation Charge",
        min_value=0.0
    )

    laboratory = st.number_input(
        "Laboratory Charge",
        min_value=0.0
    )

    medicine = st.number_input(
        "Medicine Charge",
        min_value=0.0
    )

    total = consultation + laboratory + medicine

    st.metric(
        "Total Amount",
        f"₹ {total:,.2f}"
    )

    status = st.selectbox(
        "Payment Status",
        ["Pending", "Paid"]
    )

    if st.button(
        "Generate Bill",
        use_container_width=True
    ):

        bill_id = f"B{len(st.session_state.bills)+1:04d}"

        st.session_state.bills.append({
            "Bill ID": bill_id,
            "Patient": patient,
            "Total": total,
            "Status": status
        })

        st.success(
            f"Bill {bill_id} generated!"
        )

    if st.session_state.bills:

        st.dataframe(
            st.session_state.bills,
            use_container_width=True
        )

def beds():

    st.title("🛏️ Inpatient & Beds")

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Beds", 30)
    c2.metric("Occupied", 6)
    c3.metric("Available", 24)

    names = patients()

    if not names:
        st.warning("Register a patient first.")
        return

    patient = st.selectbox("Patient", names)

    ward = st.selectbox(
        "Ward",
        ["General", "ICU", "Private"]
    )

    bed = st.number_input(
        "Bed Number",
        1,
        30,
        1
    )

    if st.button(
        "Allocate Bed",
        use_container_width=True
    ):

        st.success(
            f"Bed {bed} allocated to {patient}."
        )

def reports():

    st.title("📊 Reports")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Patients",
        len(st.session_state.patients)
    )

    c2.metric(
        "Appointments",
        len(st.session_state.appointments)
    )

    c3.metric(
        "Bills",
        len(st.session_state.bills)
    )

    c4.metric(
        "Available Beds",
        24
    )

if not st.session_state.logged_in:

    login()

else:

    # SIDEBAR

    st.sidebar.title("🏥 HMS")

    st.sidebar.write(
        f"User: **{st.session_state.username}**"
    )

    st.sidebar.write(
        f"Role: **{st.session_state.role}**"
    )

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Patient Registration",
            "Appointments",
            "Medical Records",
            "Laboratory",
            "Pharmacy",
            "Billing & Payment",
            "Beds / Inpatient",
            "Reports"
        ]
    )

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.rerun()

    # PAGE SELECTION

    if menu == "Dashboard":
        dashboard()

    elif menu == "Patient Registration":
        patient_registration()

    elif menu == "Appointments":
        appointments()

    elif menu == "Medical Records":
        medical_records()

    elif menu == "Laboratory":
        laboratory()

    elif menu == "Pharmacy":
        pharmacy()

    elif menu == "Billing & Payment":
        billing()

    elif menu == "Beds / Inpatient":
        beds()

    elif menu == "Reports":
        reports()