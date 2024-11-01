# Vaccine Scheduling Application

This application is a command-line interface (CLI) for scheduling vaccine appointments, designed to be deployed by hospitals or clinics. It allows interaction between patients, caregivers, and administrators, and manages vaccine inventory. The application is backed by a Microsoft Azure-hosted SQL database.

---

## Features

### Database Schema Design

The application is built on a structured database schema hosted on Microsoft Azure, with three primary management areas:

- **Patient Management**: Enables patients to register, log in, and schedule vaccine appointments.
- **Caregiver Management**: Supports caregivers (hospital staff) in logging in and administering appointments.
- **Vaccine Inventory Management**: Tracks the availability and reservation status of vaccine doses to ensure accurate and timely administration.

### Appointment Scheduling

Patients can schedule or cancel vaccine appointments based on caregiver availability and the current vaccine inventory. This streamlined scheduling process helps clinics ensure efficient vaccine administration and resource management.

---

## Entity Sets

The application’s database schema consists of the following core entities:

- **Patients**: Individuals who want to receive the vaccine.
- **Caregivers**: Employees responsible for administering vaccines.
- **Vaccines**: Inventory of available vaccine doses.

---

This design ensures a secure and efficient management process for scheduling, administering, and tracking vaccine appointments.

