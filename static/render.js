// Adapted from: https://github.com/sawmac/display-markdown


(function () {
  // var file = file || readme_location;
  const input = document.querySelector('textarea');
  input.addEventListener('change', updateMarkdown);
  function updateMarkdown(e) {
      displayListener(e.target.value)
  }

  var file = readme_location
  var reader = new stmd.DocParser();
  var writer = new stmd.HtmlRenderer();
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if(xhr.readyState === 4 && xhr.status === 200) {
      display(xhr);
    }
  };

  function display(xhr) {
    var parsed = reader.parse(xhr.responseText);
    var content = writer.renderBlock(parsed);
    document.getElementsByClassName('markdown')[0].innerHTML = content;

    /* try to extract h1 title and use as title for page
       if no h1, use name of file
    */
    try {
      document.title = document.querySelector('h1').textContent
    } catch (e) {
      document.title = file;
    }
  }

  function displayListener(text) {
     var parsed = reader.parse(text);
    var content = writer.renderBlock(parsed);
    document.getElementsByClassName('markdown')[0].innerHTML = content;

    /* try to extract h1 title and use as title for page
       if no h1, use name of file
    */
    try {
      document.title = document.querySelector('h1').textContent
    } catch (e) {
      document.title = file;
    }
  }

  xhr.open('GET', file);
  xhr.send();
})();



// function display(xhr) {
//    console.log(xhr.responseText)
//   var parsed = reader.parse(xhr.responseText);
//   console.log(parsed)
//   var content = writer.renderBlock(parsed);
//   document.getElementsByClassName('markdown')[0].innerHTML = content;
//
//   /* try to extract h1 title and use as title for page
//      if no h1, use name of file
//   */
//   try {
//     document.title = document.querySelector('h1').textContent
//   } catch (e) {
//     document.title = file;
//   }
// }
