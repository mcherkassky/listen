function getUniques(array){
    var length = array.length;
    var ArrayWithUniqueValues = [];

    var objectCounter = {};

    for (i = 0; i < length; i++) {
        var currentMemboerOfArrayKey = JSON.stringify(array[i]);
        var currentMemboerOfArrayValue = array[i];
        if (objectCounter[currentMemboerOfArrayKey] === undefined){
             ArrayWithUniqueValues.push(currentMemboerOfArrayValue);
             objectCounter[currentMemboerOfArrayKey] = 1;
        }else{
            objectCounter[currentMemboerOfArrayKey]++;
        }
    }
    return ArrayWithUniqueValues
};

function compareListeners(a,b) {
  if (a.listeners < b.listeners)
     return -1;
  if (a.listeners > b.listeners)
    return 1;
  return 0;
}
