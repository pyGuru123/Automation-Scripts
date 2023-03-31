function sortResponseSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('Form Responses 1');
  var dataRange = sheet.getRange('A:A').getValues();

  var data_range = "A2:S" + dataRange.length;
  Logger.log(data_range);
  var range = sheet.getRange(data_range);
  range.sort({column: 1, ascending:false});
  Logger.log("done");
}
