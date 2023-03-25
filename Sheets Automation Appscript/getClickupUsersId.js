function fetchUserId(e) {
    var sheet = e.range.getSheet();
    if (sheet.getName() == "Clickup Users") {
     
  
      var API_KEY = 'pk_6xxxx62_QMFSUR5NZ0xxxxxxxxxxxxxx'
      var headers = {
        "Content-Type": "application/json",
        "Authorization": API_KEY
      }
      var options = {
        "headers" : headers,
        "muteHttpExceptions": true
      }
  
      var response = UrlFetchApp.fetch('https://api.clickup.com/api/v2/team', options)
      var data = JSON.parse(response.getContentText());
      members = data['teams'][0]['members'];
  
      var array = [];
  
      for (var i=0; i<members.length; i++){
        member = members[i]['user'];
        var user = [];
        user.push(member['username']);
        user.push(member['id']);
        user.push(member['email']);
        array.push(user);
      }
  
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet2 = ss.getSheetByName("Clickup Users");
      
      sheet2.getRange(2, 1, array.length, array[0].length).setValues(array);
    }
  }