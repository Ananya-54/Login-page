# Tkinter OTP Authentication System using Twilio and SQLite

This project is a Python-based GUI application for user registration and OTP-based login verification. It uses the Tkinter library for the interface, SQLite for local database storage, and Twilio API for sending OTPs via SMS.

## Features

- User Registration with name, username, phone number, and email
- Phone number stored in E.164 format (e.g., +91XXXXXXXXXX)
- OTP-based Login Verification
- OTP is generated and sent via Twilio SMS
- OTPs are securely stored and verified using SQLite

## Technologies Used

- Python 3.x
- Tkinter (GUI)
- SQLite (Database)
- Twilio (SMS OTP)
- `random` (OTP generation)

## Prerequisites

- Python installed on your system
- Twilio account with verified phone number
- `twilio` Python package installed

You can install Twilio using pip:

```bash
pip install twilio
