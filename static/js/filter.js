var currentDate = new Date().toISOString().split('T')[0];
document.getElementById("departure-input").value=currentDate;
console.log(currentDate);