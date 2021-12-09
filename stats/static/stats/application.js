$(document).ready(function() {

// referenced: https://github.com/grobconnolly/Work-Day-Scheduler
var today = new Date();
var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
var dateTime = date+' '+time;
console.alert(dateTime, "Hello, world!");


});