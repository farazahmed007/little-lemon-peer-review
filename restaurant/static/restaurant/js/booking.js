const slots = ['17:00','18:00','19:00','20:00','21:00','22:00'];
const form = document.getElementById('booking-form');
const dateInput = document.getElementById('reservation_date');
const slotSelect = document.getElementById('reservation_slot');
const message = document.getElementById('form-message');
const slotStatus = document.getElementById('slot-status');

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    return parts.length === 2 ? parts.pop().split(';').shift() : '';
}

function renderSlots(bookedSlots = []) {
    slotSelect.innerHTML = '<option value="">Select a time</option>';
    let available = 0;
    slots.forEach(slot => {
        const option = document.createElement('option');
        option.value = slot;
        option.textContent = slot;
        if (bookedSlots.includes(slot)) {
            option.disabled = true;
            option.textContent = `${slot} — Booked`;
        } else {
            available += 1;
        }
        slotSelect.appendChild(option);
    });
    slotStatus.textContent = available ? `${available} slot(s) available.` : 'No slots available for this date.';
}

async function loadAvailability() {
    const selectedDate = dateInput.value;
    if (!selectedDate) return;
    slotStatus.textContent = 'Checking availability...';
    try {
        const response = await fetch(`/api/bookings/?date=${encodeURIComponent(selectedDate)}`);
        const bookings = await response.json();
        if (!response.ok) throw new Error(bookings.error || 'Could not load bookings.');
        renderSlots(bookings.map(booking => booking.reservation_slot));
    } catch (error) {
        renderSlots([]);
        message.textContent = error.message;
        message.className = 'form-message error';
    }
}

dateInput.addEventListener('change', loadAvailability);

form.addEventListener('submit', async event => {
    event.preventDefault();
    message.textContent = '';
    message.className = 'form-message';
    const data = Object.fromEntries(new FormData(form).entries());
    data.number_of_guests = Number(data.number_of_guests);

    if (!data.first_name.trim()) { message.textContent = 'First name is required.'; message.className = 'form-message error'; return; }
    if (!data.reservation_date || !data.reservation_slot) { message.textContent = 'Please choose a date and available slot.'; message.className = 'form-message error'; return; }

    try {
        const response = await fetch('/api/bookings/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
            body: JSON.stringify(data),
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Booking failed.');
        message.textContent = 'Reservation confirmed successfully!';
        message.className = 'form-message success';
        form.reset();
        dateInput.value = data.reservation_date;
        document.getElementById('number_of_guests').value = 1;
        document.getElementById('occasion').value = 'Birthday';
        await loadAvailability();
    } catch (error) {
        message.textContent = error.message;
        message.className = 'form-message error';
        await loadAvailability();
    }
});

loadAvailability();
