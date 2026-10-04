const filterDate = document.getElementById('reservation-filter-date');
const bookingList = document.getElementById('booking-list');
const jsonBox = document.getElementById('bookings-json');
const statusText = document.getElementById('reservation-status');

async function loadReservations() {
    const date = filterDate.value;
    statusText.textContent = 'Loading...';
    try {
        const response = await fetch(date ? `/api/bookings/?date=${encodeURIComponent(date)}` : '/api/bookings/');
        const selected = await response.json();
        if (!response.ok) throw new Error(selected.error || 'Unable to retrieve bookings.');
        if (!selected.length) {
            bookingList.innerHTML = '<div class="empty">No Booking</div>';
        } else {
            bookingList.innerHTML = selected.map(b => `
                <div class="booking-card">
                    <strong>${escapeHtml(b.first_name)}</strong><br>
                    Date: ${b.reservation_date}<br>
                    Time: ${b.reservation_slot}<br>
                    Guests: ${b.number_of_guests}<br>
                    Occasion: ${escapeHtml(b.occasion)}
                </div>`).join('');
        }
        statusText.textContent = `Showing bookings for ${date}.`;

        const allResponse = await fetch('/api/bookings/');
        const allBookings = await allResponse.json();
        jsonBox.textContent = JSON.stringify(allBookings, null, 2);
    } catch (error) {
        statusText.textContent = error.message;
        bookingList.innerHTML = '<div class="empty">No Booking</div>';
        jsonBox.textContent = '[]';
    }
}

function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
}

filterDate.addEventListener('change', loadReservations);
loadReservations();
