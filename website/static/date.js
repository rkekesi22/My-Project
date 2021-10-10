var d = new Date();
month = d.getMonth();
year = d.getFullYear();

month = month + 1

console.log(month)
console.log(year)



calendar.setAttribute('href', `${year}/${month}`);