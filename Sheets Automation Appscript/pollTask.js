function sendmail(username, email) {
  const html = "Hello " + username + " <br/>Your task is incomplete and overdue. Please finish it as soon as possible";
  MailApp.sendEmail({
    to: email,
    subject: 'Task overdue',
    htmlBody: html
  })
}

function checkTaskStatus() {
  var API_KEY = '61430062_QMFSUBN1MJRE'
  headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
  }

  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = spreadsheet.getSheetByName('Form Responses 1');

  var range = sheet.getDataRange();
  var values = range.getValues();
  for (var i=1; i<values.length; i++) {
    var row = values[i];
    taskStatus = row[row.length - 1];
    taskID = row[row.length - 2];

    if (taskID != "" && taskStatus != "") {
      if (!(["done", "closed"].includes(taskStatus))) {

        duedate = row[row.length - 5];
        slack_id = getSlackUser(row[row.length - 6]);

        endpoint = "https://api.clickup.com/api/v2/task/" + taskID;

        var options = {
        "method" : "get",
        "headers" : headers
        }

        var response = UrlFetchApp.fetch(endpoint, options)
        response = JSON.parse(response);

        status = response['status']['status'];
        if (!(["done", "closed"].includes(status))) {
            duedate = new Date(duedate);
            current_date = new Date();
            if (current_date > duedate) {
              var email = response['assignees'][0]['email'];
              var username = response['assignees'][0]['username'];
              
              sendmail(username, email);
              overdue_msg = `Hello ${username}\nYour task is incomplete and overdue. Please finish it as soon as possible.`;
              sendSlackMessage(slack_id, overdue_msg);
              Logger.log("Notification sent to " + username);
              Utilities.sleep(1000);
            }
        }
        else {
          var range = sheet.getRange(i+1, row.length);
          range.setValue(status);
        }
      }
    }
  }
}

// function sendEmail() {
//   var recipient = "recipient@example.com"; // Replace with the email address of the person you want to send the email to
//   var subject = "Email Subject";
//   var body = "Email Body";
//   var from = "person1@example.com"; // Replace with the email address of the person whose email you want to send from
//   var password = "password"; // Replace with the password of the email account you want to send from

//   GmailApp.sendEmail(recipient, subject, body, {
//     from: from,
//     replyTo: from,
//     name: "Sender Name",
//     htmlBody: body
//   });
// }