# 🚆 JourneyJoy  
**Seamless Bookings, Joyful Journeys**

JourneyJoy is a modern, GUI-based train ticket booking system built using Python and Tkinter.  
It offers a beautiful, responsive interface with real-time validation, animated receipts, and a smooth booking experience.

## 🎯 Features

- 👤 Passenger name input with real-time validation  
- 🎟️ Multiple seat types with availability tracking  
- 📏 Distance-based fare calculation with smart discounts  
- 📉 Auto fare estimation with instant feedback  
- 💳 Payment method selection
- 📃 Animated booking receipt popup with details  
- 💡 Pulsing and styled buttons for a modern feel  
- ✅ Input validation and error handling  
- 🖼️ Clean and centered layout with branding and tagline  

## 🛠️ Tech Stack

| Area        | Tech Used            | Description                                  |
|-------------|----------------------|----------------------------------------------|
| 🐍 Backend   | **Python**           | Core language powering the application       |
| 🖼️ GUI       | **Tkinter**          | Native GUI library for creating the interface|
| 🧠 Logic     | **Custom Python**    | Includes fare calculations, animations, etc. |
| 🎨 Styling   | **Tkinter Widgets**  | Buttons, labels, combo boxes with custom styles |

## 💰 Fare Calculation Logic

- Base fare = `price_per_km × distance × number_of_seats`
- Discounts:
  - 🎁 **10% off** for 5 or more seats
  - ✈️ **5% off** for distances over 500 km

## 🧾 Booking Receipt

Upon successful booking, an animated window pops up showing:

- Ticket ID  
- Passenger Name  
- Seat Type & Quantity  
- Travel Distance  
- Final Fare  
- Payment Method  
- Timestamp  

> 🎉 "Thank you for booking with us!" message included!
