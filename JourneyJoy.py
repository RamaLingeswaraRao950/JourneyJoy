import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime

# Seat types with price per km and initial seat count
seat_info = {
    "Sleeper": {"desc": "No AC, beds available", "price": 3, "available": 55},
    "AC": {"desc": "Air conditioned, comfy ride", "price": 4, "available": 33},
    "General": {"desc": "Cheapest option, no reservation", "price": 2, "available": 88},
    "Luxury": {"desc": "Premium seats with meals", "price": 5, "available": 22}
}

# --- Utility functions ---


def update_remaining_label(event=None):
    seat_type = seat_type_var.get()
    if seat_type in seat_info:
        remaining_label.config(
            text=f"Remaining seats: {seat_info[seat_type]['available']}",
            fg="blue"
        )
    else:
        remaining_label.config(text="", fg="black")
    validate_inputs()


def validate_inputs(event=None):
    try:
        name = entry_name.get().strip()
        seat_type = seat_type_var.get()
        distance = float(entry_distance.get())
        seats = int(entry_seats.get())

        if not name or seat_type == "Select" or distance <= 0 or seats <= 0:
            book_btn.config(state="disabled")
            fare_label.config(text="")
            return

        if seats > seat_info[seat_type]["available"]:
            fare_label.config(
                text=f"❌ Cannot book {seats} seats! Only {seat_info[seat_type]['available']} available.",
                fg="red"
            )
            book_btn.config(state="disabled")
            return

        fare = seat_info[seat_type]["price"] * distance * seats
        discount = 0.10 if seats >= 5 else (0.05 if distance > 500 else 0)
        final_fare = fare - (fare * discount)

        fare_label.config(
            text=f"Estimated Fare: ₹{final_fare:.2f}" +
            (f" (Discount Applied)" if discount else ""),
            fg="green"
        )
        book_btn.config(state="normal")
    except ValueError:
        fare_label.config(text="")
        book_btn.config(state="disabled")

# --- Pulsing Button Animation ---


def pulse_button(button):
    scale_up = True
    size = 17  # starting font size

    def animate():
        nonlocal scale_up, size
        if scale_up:
            size += 1
            if size >= 20:
                scale_up = False
        else:
            size -= 1
            if size <= 17:
                scale_up = True

        button.config(font=("Times New Roman", size, "bold"))
        button.after(100, animate)  # animation speed

    animate()

# --- Pill button style ---


def make_pill_button_style(btn, bg_color, text_color="white"):
    btn.config(
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        font=("Times New Roman", 17, "bold"),
        padx=30,
        pady=10,
        fg=text_color,
        bg=bg_color,
        activebackground=bg_color,
        activeforeground=text_color
    )

# --- Animated receipt ---


def show_animated_receipt(receipt_text):
    receipt_win = tk.Toplevel(root)
    receipt_win.configure(bg="white")

    win_w, win_h = 400, 300
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    target_x = screen_w - win_w - 50
    target_y = (screen_h // 2) - (win_h // 2)
    start_y = -win_h

    receipt_win.geometry(f"{win_w}x{win_h}+{target_x}+{start_y}")
    receipt_win.attributes("-alpha", 0.0)

    tk.Label(receipt_win, text="🎫 Booking Receipt 🎫",
             font=("Times New Roman", 16, "bold"), bg="white", fg="green").pack(pady=10)
    tk.Label(receipt_win, text=receipt_text, font=("Courier New", 10),
             bg="white", justify="left").pack(padx=10, pady=5)

    # Close button with pulsing effect
    close_btn = tk.Button(receipt_win, text="Close",
                          command=receipt_win.destroy)
    make_pill_button_style(close_btn, bg_color="#2E8B57", text_color="white")
    close_btn.pack(pady=10)
    pulse_button(close_btn)

    alpha, y_pos, step = 0.0, start_y, 10
    bounce_done = False

    def animate():
        nonlocal alpha, y_pos, step, bounce_done
        if alpha < 1.0:
            alpha += 0.05
            receipt_win.attributes("-alpha", alpha)
        if not bounce_done:
            y_pos += step
            if y_pos >= target_y + 20:
                step = -5
            if step < 0 and y_pos <= target_y:
                y_pos = target_y
                bounce_done = True
            receipt_win.geometry(f"{win_w}x{win_h}+{target_x}+{y_pos}")
        if alpha < 1.0 or not bounce_done:
            receipt_win.after(15, animate)

    animate()

# --- Booking function ---


def book_ticket():
    name = entry_name.get().strip()
    seat_type = seat_type_var.get()
    distance = float(entry_distance.get())
    seats = int(entry_seats.get())
    payment_method = payment_var.get()

    if seats > seat_info[seat_type]["available"]:
        status_label.config(text=f"❌ Cannot book {seats} seats! Only {seat_info[seat_type]['available']} available.",
                            fg="red")
        return

    fare = seat_info[seat_type]["price"] * distance * seats
    discount = 0.10 if seats >= 5 else (0.05 if distance > 500 else 0)
    final_fare = fare - (fare * discount)

    ticket_id = f"TKT{random.randint(1000, 9999)}"
    booking_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    seat_info[seat_type]["available"] -= seats
    update_remaining_label()

    receipt = (
        f"{'='*40}\n"
        f"Ticket ID     : {ticket_id}\n"
        f"Passenger     : {name}\n"
        f"Seat Type     : {seat_type}\n"
        f"Seats Booked  : {seats}\n"
        f"Distance      : {distance} km\n"
        f"Total Fare    : ₹{final_fare:.2f}\n"
        f"Payment Mode  : {payment_method}\n"
        f"Booking Time  : {booking_time}\n"
        f"{'='*40}\n"
        f"Thank you for booking with us! 🚆"
    )

    status_label.config(text="✅ Booking Successful!", fg="green")
    show_animated_receipt(receipt)

    entry_name.delete(0, tk.END)
    entry_distance.delete(0, tk.END)
    entry_seats.delete(0, tk.END)
    seat_type_var.set("Select")
    payment_var.set("Cash")
    remaining_label.config(text="")
    fare_label.config(text="")
    book_btn.config(state="disabled")

# --- Center window function ---


def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")


# --- GUI Setup ---
root = tk.Tk()
root.title("JourneyJoy : Seamless Bookings, Joyful Journeys")
center_window(root, 414, 636)
root.resizable(False, False)

# Logo & Tagline
logo_frame = tk.Frame(root, bg="white")
logo_frame.pack(pady=(10, 15))

logo_label = tk.Label(logo_frame, text="🚆 JourneyJoy", font=(
    "Segoe UI", 28, "bold"), fg="#2E8B57", bg="white")
logo_label.pack()

tagline_label = tk.Label(logo_frame, text="Seamless Bookings, Joyful Journeys",
                         font=("Segoe UI", 14, "italic"), fg="#555555", bg="white")
tagline_label.pack()

tk.Label(root, text="Passenger Name:", font=(
    "Times New Roman", 14)).pack(pady=5)
entry_name = tk.Entry(root, font=("Times New Roman", 14))
entry_name.pack()
entry_name.bind("<KeyRelease>", validate_inputs)

tk.Label(root, text="Seat Type:", font=("Times New Roman", 14)).pack(pady=5)
seat_type_var = tk.StringVar(value="Select")
seat_type_menu = ttk.Combobox(root, textvariable=seat_type_var,
                              values=list(seat_info.keys()),
                              state="readonly", font=("Times New Roman", 14))
seat_type_menu.pack()
seat_type_menu.bind("<<ComboboxSelected>>", update_remaining_label)

remaining_label = tk.Label(root, text="", font=("Times New Roman", 11))
remaining_label.pack()

tk.Label(root, text="Travel Distance (km):",
         font=("Times New Roman", 14)).pack(pady=5)
entry_distance = tk.Entry(root, font=("Times New Roman", 14))
entry_distance.pack()
entry_distance.bind("<KeyRelease>", validate_inputs)

tk.Label(root, text="Number of Seats:", font=(
    "Times New Roman", 14)).pack(pady=5)
entry_seats = tk.Entry(root, font=("Times New Roman", 14))
entry_seats.pack()
entry_seats.bind("<KeyRelease>", validate_inputs)

fare_label = tk.Label(root, text="", font=("Times New Roman", 14))
fare_label.pack(pady=5)

tk.Label(root, text="Payment Method:", font=(
    "Times New Roman", 14)).pack(pady=5)
payment_var = tk.StringVar(value="Cash")
payment_menu = ttk.Combobox(root, textvariable=payment_var,
                            values=["Cash", "UPI", "Card"],
                            state="readonly", font=("Arial", 14))
payment_menu.pack()

# Book Ticket button with pulsing effect
book_btn = tk.Button(root, text="Book Ticket",
                     command=book_ticket, state="disabled")
make_pill_button_style(book_btn, bg_color="#2E8B57", text_color="white")
book_btn.pack(pady=17)
pulse_button(book_btn)

status_label = tk.Label(root, text="", font=("Times New Roman", 17, "bold"))
status_label.pack(pady=(5, 10))

root.mainloop()
