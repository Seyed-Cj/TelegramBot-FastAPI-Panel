const apiUrl = '/bot';
const statusElem = document.getElementById('status');
const tokenInput = document.getElementById('token');
const onButton = document.getElementById('on');
const offButton = document.getElementById('off');

async function fetchStatus() {
  try {
    const response = await fetch(`${apiUrl}/status`);
    const data = await response.json();
    statusElem.textContent = data.status;
    statusElem.classList.remove('error');
    onButton.disabled = data.status === 'active';
    offButton.disabled = data.status === 'inactive';
  } catch (error) {
    statusElem.textContent = 'Error';
    statusElem.classList.add('error');
    onButton.disabled = false;
    offButton.disabled = false;
  }
}

async function sendRequest(endpoint) {
  const token = tokenInput.value;
  if (!token) {
    alert('Please enter admin token');
    return;
  }
  try {
    const response = await fetch(`${apiUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      alert(data.message);
      fetchStatus();
    } else {
      alert('Error: ' + response.statusText);
    }
  } catch (error) {
    alert('Error: ' + error.message);
  }
}

function turnOn() {
  sendRequest('/on');
}

function turnOff() {
  sendRequest('/off');
}
fetchStatus();