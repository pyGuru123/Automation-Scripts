var members = {
    "prajjwal pathak" : 61436762,
    "umrah" : 61497114
  }
  
  var API_KEY = ''
  headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
  }
  
  function timestamp(Duedate) {
    date = new Date(Duedate);
    milli = date.getTime()
    stamp = milli.toString().split('.').join('')
    return parseInt(stamp);
  }
  
  function setCellValue(sheet, row, col, value) {
      var range = sheet.getRange(row, col);
      range.setValue(value);
  }
  
  function onAssign(e) {
    var sheet = e.range.getSheet();
    if (sheet.getName() == "Form Responses 1" && e.range.getColumn() == 8) {
  
        row = e.range.getRow();
        var data = sheet.getRange(row, 1, 1, sheet.getLastColumn()).getValues()[0];
  
        var duedate = data[6];
        var duedate = timestamp(duedate);
        Logger.log(duedate);
  
        var assignee = [members[data[3]]]; 
  
        payload = {
          "name" : "Test task from clikcup api",
          "description" : data[4],
          "assignees" : assignee,
          "status" : "open - todo",
          "priority" : Math.floor(data[5]),
          "due_date" : duedate,
          "due_date_time": false
        }
  
        Logger.log(payload);
  
        var options = {
          "method" : "post",
          'contentType': 'application/json',
          "payload" : JSON.stringify(payload),
          "headers" : headers
        }
  
        var response = UrlFetchApp.fetch("https://api.clickup.com/api/v2/list/900200157532/task", options)
        response = JSON.parse(response);
        task_id = response['id']
        task_status = response['status']['status']
        Logger.log(task_id, task_status);
        setCellValue(sheet, row, 9, task_id);
        setCellValue(sheet, row, 10, task_status);
     } 
  }
  