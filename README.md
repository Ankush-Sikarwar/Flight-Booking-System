<br/>
<p align="center">
  <a href="http://flight-booking.live/"> </a>

  <h3 align="center">Flight Booking System using Django </h3>

  <p align="center">
    A flight booking system allowed you to book flights
    <br/>
    <br/>
    <a href="http://flight-booking.live/">View Demo</a>
  </p>
</p>



## Table Of Contents

- [Table Of Contents](#table-of-contents)
- [About The Project](#about-the-project)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Authors](#authors)

## About The Project

The Flight Booking System is a comprehensive and user-friendly platform designed to facilitate the seamless booking of flights for travellers and streamline administrative processes for administrators. The system offers a range of features for both users and administrators, ensuring a convenient and efficient experience for all stakeholders.

Features:

* User Features: User Registration and Authentication: Users can create accounts by providing the necessary details. Secure authentication mechanisms ensure the safety of user data.

* Search and Filter Flights: Users can search for flights based on various parameters such as source, destination and date.

* View Flight Details: Detailed flight information, including departure/arrival times, available seats, and pricing.

* Booking and Reservation: Users can book seats for desired flights and have the option to reserve seats

* Payment Integration: A demo integration with multiple payment methods (credit card, debit card, UPI).

* Booking History and Tracking:
Users can view their booking history and track the status of current bookings. Notifications for booking confirmations and updates.

* User Notifications: Real-time notifications for booking confirmations, changes, and flight-related updates.

Admin Features:

* Flight and Schedule Management: Admins can add, edit, or remove flights and schedules. Manage seat availability and update flight details.
 
* Search and Filter Flights: Filtering and searching options based on various parameters  for quick access to specific flights, schedules and booking.

*  User Management: Admins have the ability to manage user accounts. View user details, track booking history, and address user-related issues.

## Built With

Frontend: 
* HTML, CSS, JS, Bootstrap

Backend: 
* Django (Python), SQL Lite, Django ORM

Deployment: 
* Docker, Nginx & Gunicorn, AWS

Version Control: 
* Git

## Getting Started

This is an example of how you may give instructions on setting up your project locally. To get a local copy up and running, follow these steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* python 3.10 or Docker

### Installation

1. Clone the repo

```sh
https://github.com/Ankush-sikarwar/flight_booking.git
```

2. Follow these steps using python

3. Setup .env file under ``` cd flight_booking ```, the project folder where the settings.py file is located in the same folder create .env file and set the value mentioned in .env-example

```sh
python -m venv env
env/Scripts/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

or

4. Follow these steps using the Docker

```docker
docker-compose build
docker-compose up
```

## Usage

#### Flight Booking System - User Flow:

**1. Registration and Login:**

* New users register by providing basic details.
* Existing users log in using their credentials.
* Authentication mechanisms ensure secure access.

**2. Homepage:**

* Users are greeted with a user-friendly homepage.
* Prominent search bar allows users to initiate flight searches.

**3. Flight Search and Filtering:**

* Users input their travel details, such as source, destination and date.

**4. View Flight Details:**

* Search results display available flights with comprehensive details.
Information includes departure/arrival locations, departure/arrival times, available seats, and pricing.

**5. Seat Selection and Booking:**

* Users select desired flights and choose seats.
Option to reserve seats and complete bookings at a later time.

**6. Payment Integration:**

* Seamless demo integration with various payment methods (credit card, debit card, UPI).

**7. Booking Confirmation:**

* Users receive real-time notifications for booking confirmations.
Booking details, including departure time and seat information, are provided.

**8. Booking History and Tracking:**
* Users can view a comprehensive booking history.
Real-time tracking of the status of current bookings and cancelling the bookings.

**9. Logout:** 
* Users can securely log out to end their session.


#### Flight Booking System - Admin Flow:

**1. Admin Login:**
* Admins log in using Gmail and password.

**2.  Homepage:**
* Users are greeted with a user-friendly homepage after, in the sidebar, clicking on the admin portal.

**3. Add Flight:**
* Admins have the ability to add new flights.
* Enter flight details such as flight number, name, type, and capacity.

**4. Manage Flight Details:**
* Admins can view and update details of existing flights.
* Options to edit flight information, update capacity, and manage seat availability.

**5. Add Routes:**
* Admins add new flight routes by specifying departure and arrival locations.
* Enter the distance of each route.

**6. Manage Routes:**
* View and update details of existing routes.
* Options to edit departure/arrival locations updates and distances.

**7. Schedule Management:**

* Admins create schedules for flights, specifying departure and arrival times.
* Assign routes to schedules.

**8. Update Schedule Details:**
* Admins can view and update details of existing schedules.
* Options to edit departure/arrival times and update assigned routes.

**9. Filter and Search:**
* Admins can efficiently filter and search through flights, routes, and schedules.
* Quick access to specific records based on various parameters.

**10. Logout:**
* Admins can securely log out to end their session.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Authors

* **Anup Kumar Mridha** - *MCA Student* - [Ankush Sikarwar](https://github.com/Ankush-sikarwar)

