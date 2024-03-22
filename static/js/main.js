function closeTab() {
  window.close();
}

function getCurrentDateTime() {
  const now = new Date();
  const day = String(now.getDate()).padStart(2, '0');
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const year = now.getFullYear();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');

  return {
    date: `${day}/${month}/${year}`,
    time: `${hours}:${minutes}`
  };
}

function updateDateTime() {
  const dateTime = getCurrentDateTime();
  document.getElementById('date').textContent = dateTime.date;
  document.getElementById('time').textContent = dateTime.time;
}

document.addEventListener('DOMContentLoaded', updateDateTime);