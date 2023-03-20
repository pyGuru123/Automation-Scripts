function sendMail(e) {
    const email = "prajjwal.pathak@kapso.in";
    const html = "New Record Available";
    MailApp.sendEmail({
      to: email,
      subject: 'Form Submit',
      htmlBody: html
    })
  }
  
  function slackNotification() {
    const webhook = "https://hooks.slack.com/services/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";
    var payload = {
      "text": "Hello, everyone!",
      "channel": "D04QUJLEPST"
    }
  
    var options = {
          "method" : "post",
          'contentType': 'application/json',
          "payload" : JSON.stringify(payload),
        }
  
    var response = UrlFetchApp.fetch(webhook, options)
  }
  