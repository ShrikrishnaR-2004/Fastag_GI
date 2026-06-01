# FASTag Customer Management Portal - Detailed Project Prompt

Build a complete **FASTag Customer Management Portal** using **Python Flask**, **MySQL**, **Bootstrap 5**, **HTML/CSS/JavaScript**, and **Flask-SQLAlchemy**.

The application should be production-style, responsive, secure, and user-friendly.

---

## Project Overview

The system is a customer-facing FASTag portal where users can:

* Create an account
* Login securely
* Manage FASTag vehicles
* View wallet balance
* Recharge FASTag wallet
* View toll transaction history
* Track toll spending analytics
* Raise complaints
* Manage profile and KYC information
* Download transaction statements
* Receive notifications

The project should use role-based authentication with:

* Customer
* Administrator

---

## Technical Requirements

### Backend

* Python 3.12+
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-WTF
* Flask-Migrate
* MySQL
* argon2id Password Hashing

### Frontend

* Bootstrap 5
* HTML5
* CSS3
* JavaScript
* Chart.js

### Security

* Password hashing
* CSRF protection
* Session management
* Google reCAPTCHA v2
* Email verification
* Forgot password functionality
* Input validation
* SQL injection protection

---

# Authentication Module

## Signup Page

Fields:

* Full Name
* Email Address
* Mobile Number
* Password
* Confirm Password
* Accept Terms Checkbox
* Google reCAPTCHA

Validation:

* Email uniqueness
* Strong password policy
* Mobile number validation
* Password confirmation matching
* CAPTCHA verification

After registration:

* Send verification email
* User status becomes active only after verification

---

## Login Page

Fields:

* Email or Mobile Number
* Password
* Remember Me
* Google reCAPTCHA

Features:

* Secure login
* Session creation
* Remember me option
* Login activity tracking

---

## Forgot Password

Flow:

* User enters email
* Reset token generated
* Email sent
* New password creation page

---

# Customer Dashboard

After login, display:

### Welcome Section

* Customer Name
* Current Date
* Last Login Time

### Statistics Cards

* Current Wallet Balance
* Number of Vehicles
* Total Toll Transactions
* Monthly Toll Spending
* Last Recharge Amount
* Pending Complaints

---

## Dashboard Charts

### Monthly Toll Spending

Line Chart displaying:

* Jan
* Feb
* Mar
* Apr
* May
* Jun

---

### Most Used Toll Plazas

Pie Chart showing:

* Plaza Name
* Visit Count

---

### Monthly Trips

Bar Chart showing:

* Number of toll crossings per month

---

# Vehicle Management Module

Customers can manage multiple vehicles.

Vehicle Information:

* Vehicle Number
* Vehicle Type
* Manufacturer
* Model
* Registration Date
* FASTag Number
* RFID Tag Number
* Tag Status
* Expiry Date

Functions:

* Add Vehicle
* Edit Vehicle
* View Vehicle
* Remove Vehicle
* Search Vehicle

Vehicle Status:

* Active
* Suspended
* Expired

---

# FASTag Management

For every vehicle display:

* FASTag Number
* FASTag Status
* Tag Issue Date
* Expiry Date
* Current Balance

Actions:

* Block FASTag
* Request Replacement
* Activate New FASTag
* View Tag Details

---

# Wallet Management

Wallet Overview:

* Current Balance
* Auto Recharge Status
* Minimum Balance Threshold

Recharge Options:

* ₹200
* ₹500
* ₹1000
* ₹2000
* Custom Amount

Recharge Methods:

* UPI
* Debit Card
* Credit Card
* Net Banking

Store recharge history.

---

## Auto Recharge

Customer can configure:

* Enable Auto Recharge
* Threshold Amount
* Recharge Amount

Example:

When balance drops below ₹300,
automatically recharge ₹1000.

---

# Toll Transaction Module

Display all toll deductions.

Fields:

* Transaction ID
* Date
* Time
* Vehicle Number
* Toll Plaza
* Location
* Amount Deducted
* Remaining Balance
* Transaction Status

Filters:

* Date Range
* Vehicle
* Toll Plaza
* State

Search:

* Transaction ID
* Toll Plaza

Exports:

* PDF
* Excel

---

# Spending Analytics

Provide analytics dashboard.

Metrics:

* Total Monthly Spend
* Average Toll Cost
* Most Used Route
* Most Visited Toll Plaza

Charts:

* Monthly Spending
* Toll Plaza Distribution
* Yearly Expenses

---

# Complaint Management Module

Users can raise complaints.

Complaint Types:

* Double Toll Deduction
* Wrong Toll Charge
* Recharge Failure
* FASTag Not Detected
* Refund Issue
* Other

Fields:

* Subject
* Description
* Screenshot Upload

Complaint Status:

* Pending
* In Progress
* Resolved
* Closed

Complaint Tracking Page.

---

# Notifications Module

Show:

* Toll Deductions
* Wallet Recharge
* Low Balance Alerts
* Complaint Updates
* FASTag Expiry Reminders

Notification Types:

* In-App
* Email
* SMS (Optional)

---

# Profile Module

Profile Fields:

* Name
* Email
* Mobile Number
* Address
* State
* City

KYC Information:

* PAN Number
* Aadhaar Number
* Driving License Number

Document Upload:

* Aadhaar
* PAN
* Vehicle RC

Verification Status:

* Verified
* Pending
* Rejected

---

# Statement Downloads

Generate:

* Monthly Statement
* Annual Statement
* Recharge Report
* Toll Usage Report

Formats:

* PDF
* Excel

---

# Database Design

Create MySQL tables:

1. users
2. vehicles
3. fastags
4. wallets
5. recharge_history
6. toll_transactions
7. complaints
8. notifications
9. user_documents
10. password_resets
11. email_verifications
12. admin_users
13. audit_logs

Include proper:

* Primary Keys
* Foreign Keys
* Indexing
* Constraints

---

# Admin Panel

Separate login.

Admin Features:

### Dashboard

* Total Customers
* Active FASTags
* Revenue Statistics
* Complaints Summary

### User Management

* View Users
* Suspend Users
* Activate Users

### Vehicle Management

* View Vehicles
* Edit Vehicles

### Complaint Management

* Assign Complaint
* Resolve Complaint

### Reports

* Revenue Report
* Transaction Report
* Customer Report

---

# UI Design Requirements

Use:

* Modern Bootstrap 5 Admin Theme
* Responsive Layout
* Sidebar Navigation
* Top Navigation Bar
* Light Mode
* Dark Mode

Pages:

* Login
* Signup
* Dashboard
* Vehicles
* Transactions
* Wallet
* Complaints
* Notifications
* Profile
* Settings

---

# Additional Features

Implement:

* REST API support
* JWT Authentication API
* Email Notifications
* Activity Logs
* Audit Trails
* Search Functionality
* Pagination
* Sorting
* File Upload Validation
* Error Logging
* Role-Based Access Control

---

# Deliverables

Generate:

1. Complete Flask Project Structure
2. MySQL Database Schema
3. SQL Scripts
4. Models
5. Routes
6. Templates
7. CSS Files
8. JavaScript Files
9. Authentication Logic
10. Dashboard Pages
11. Admin Panel
12. API Endpoints
13. Installation Guide
14. Requirements.txt
15. README.md

The code should follow Flask best practices, use Blueprints, be modular, scalable, secure, and ready for deployment on Linux, Apache/Nginx, or cPanel hosting.
