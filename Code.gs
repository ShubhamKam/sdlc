function onOpen() {
  DocumentApp.getUi()
    .createMenu('SDLC Visualization')
    .addItem('Show Visualization', 'showVisualization')
    .addToUi();
}

function showVisualization() {
  var html = HtmlService.createHtmlOutputFromFile('Visualization')
    .setTitle('SDLC Process Visualization')
    .setWidth(800)
    .setHeight(600);
  
  DocumentApp.getUi().showSidebar(html);
} 