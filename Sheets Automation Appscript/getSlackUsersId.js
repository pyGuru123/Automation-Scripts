function fetchSlackUserID(e) {
  var sheet = e.range.getSheet();
  if (sheet.getName() == "Slack Users") {

    var key = "";
    var headers = {
        "Authorization": `Bearer ${key}`,
        "Content-type": "application/x-www-form-urlencoded"
    }
    var options = {
      "headers" : headers,
    }

    var response = UrlFetchApp.fetch("https://slack.com/api/users.list", options)
    var users_data = JSON.parse(response.getContentText());
    members = users_data['members'];
    Logger.log(members.length);
    var array = [];

    for (var i=0; i<members.length; i++){
      member = members[i];
      if (member['deleted'] == false) {
          var user = [];
          user.push(member['name']);
          user.push(member['id']);
          user.push(member['real_name']);
          array.push(user);
      }
      
    }

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet2 = ss.getSheetByName("Slack Users");
    sheet2.getRange(2, 1, array.length, array[0].length).setValues(array);
    Logger.log("Slack users Updated")
  }
}