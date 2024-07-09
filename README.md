# car-rental-services

# Car Rentify Project README

Welcome to the Car Rentify project! This README provides an overview of the project structure, features, setup instructions, and more.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [File Structure](#file-structure)
6. [Technologies Used](#technologies-used)
7. [Contributing](#contributing)
8. [License](#license)

## Project Overview

The Car Rentify project is a Django-based web application for managing car rentals. It allows users to browse cars, view details, make reservations, and complete payments using Flutterwave integration.

## Features

- **User Authentication**: Users can sign up, log in, and manage their profiles.
- **Car Listings**: Displays a list of available cars with details.
- **Reservation**: Users can select a car, fill out a reservation form, and confirm bookings.
- **Payment Integration**: Integrates with Flutterwave for secure payment processing.
- **Email Notifications**: Sends confirmation emails for successful reservations.
- **Responsive Design**: Ensures usability across various devices.

## Installation

To run the Car Rentify project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd carRentify
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env` and configure the necessary environment variables like `FLUTTERWAVE_PUBLIC_KEY`.

5. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   Open your web browser and go to `http://localhost:8000/` to view the Car Rentify application.

## Usage

- **Browse Cars**: Navigate to the home page to see available cars.
- **View Car Details**: Click on a car to see its details.
- **Make a Reservation**: Fill out the reservation form on the car details page and proceed to payment.
- **Complete Payment**: Use the integrated Flutterwave payment system for secure transactions.
- **View Reservation Confirmation**: Upon successful payment, users are redirected to a confirmation page with reservation details.

## File Structure

- **`showroom/`**: Django application folder containing models, views, templates, and forms.
- **`static/`**: Static files like CSS, JavaScript, and images.
- **`templates/`**: HTML templates for rendering pages.

## Technologies Used

- **Python**: Backend logic and Django framework.
- **Django**: Web framework for building the application.
- **HTML/CSS**: Frontend structure and styling.
- **JavaScript**: Client-side scripting for interactivity.
- **Flutterwave**: Payment gateway integration.
- **Bootstrap**: Frontend framework for responsive design.

## Contributing

Contributions are welcome! If you'd like to contribute to the Car Rentify project, please fork the repository and submit a pull request with your proposed changes.

## License

This project is licensed under the [MIT License](LICENSE).
