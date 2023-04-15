function sendmail(username, email) {
  var recipient = email;
  var subject = "Task overdue";
  var body = "Hello " + username + ". Your Clickup task is incomplete and overdue. Please finish it as soon as possible";
  var from = "uzi@gmail.in";
  var password = "hello@123";
  var smtpServer = "smtp.gmail.com";
  var port = 587;
  
  var smtpUsername = from; // The email address you are using to send the email
  
  var options = {
    htmlBody: body,
    name: from
  };
  
  GmailApp.sendEmail(recipient, subject, body, options);
}

function test() {
  sendmail("Madara", "pra35@gmail.com");
}