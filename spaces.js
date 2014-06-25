var util = require('util');
var fs = require('fs');

/**
 * @param {Errors[]} errorsCollection
 */
module.exports = function(errorsCollection) {
    var errorCount = 0;
    /**
     * Fixes spacing errors.
     */

    var json = {};

    errorsCollection.forEach(function(errors) {
        var file = errors.getFilename();
        var file_contents = fs.readFileSync(file, 'utf-8');
        var lines = file_contents.split('\n');

        if (!errors.isEmpty()) {
           var list = [];

            errors.getErrorList().forEach(function(error) {
                list.push({
                    line: error.line,
                    column: error.column,
                    message: error.message
                })
                errorCount++;
            });

            json[file] = list;

            list = list.reverse();
            list.forEach(function(error) {
                var line = error.line - 1;
                var str = lines[line];
                var col = error.column;
                while (str.charAt(col) != '+' && str.charAt(col) != '-') col++;
                lines[line] = str.substring(0, col) + ' ' + str.substring(col);
                console.log(str +  ' --> ' + lines[line]);
            });

            file_contents = lines.join('\n');

            // console.log('--preview formatted: ' + file + ' --')
            // console.log(file_contents) // print formatted source
            fs.writeFileSync(file, file_contents);  // write formatted source
        }

    });

    console.log('end', json, errorCount)
};
