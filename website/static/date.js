var d = new Date();
month = d.getMonth.toString;
year = d.getFullYear();

console.log(month)
console.log(year)

calendar.setAttribute('href', month+"/"+year);