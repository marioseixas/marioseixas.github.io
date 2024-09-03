function cleartext() {
    var t = document.getElementById("thetext");
    t.value = '';
    updatetextlength();
    updatewords();
}

function selectall() {
    var t = document.getElementById("thetext");
    t.focus();
    t.select();
}

function copyText() {
    var t = document.getElementById("thetext");
    t.select();
    document.execCommand('copy');
}

function updatetextlength() {
    var t = document.getElementById("thetext");
    var c = document.getElementById("characters");
    c.value = t.value.length + ' chars';
}

function updatewords() {
    var t = document.getElementById("thetext");
    var char_count = t.value.length;
    var fullStr = t.value + " ";
    var initial_whitespace_rExp = /^[^A-Za-z0-9]+/gi;
    var left_trimmedStr = fullStr.replace(initial_whitespace_rExp, "");
    var non_alphanumerics_rExp = rExp = /[^A-Za-z0-9]+/gi;
    var cleanedStr = left_trimmedStr.replace(non_alphanumerics_rExp, " ");
    var splitString = cleanedStr.split(" ");
    var word_count = splitString.length - 1;

    var w = document.getElementById("words");
    w.value = word_count + ' words';
}

function updatelines() {
    var t = document.getElementById("thetext").value;
    var c = document.getElementById("lines");

    if (!t) {
        c.value = '0 lines';
    } else {
        c.value = t.split("\n").length + ' lines';
    }
}

function updateparagraphs() {
    var t = document.getElementById("thetext").value;
    var c = document.getElementById("paragraphs");
    for(var r=t.split(/\n\n+/g),n=0,a=0;a<r.length;a++)r[a].length!=0&&n++;
    
    if (!t) {
        c.value = '0 paragraphs';
    } else {
        c.value = n + ' paragraphs';
    }
}

function updatecounts() {
    updatetextlength();
    updatewords();
    updatelines();
    updateparagraphs();
}

function uppercase() {
    var t = document.getElementById("thetext");
    t.value = t.value.toUpperCase();
}

function lowercase() {
    var t = document.getElementById("thetext");
    t.value = t.value.toLowerCase();
}

function capitalizewords() {
    var t = document.getElementById("thetext");

    t.value = (t.value + '').replace(/^(.)|\s(.)/g, function ($1) {
        return $1.toUpperCase();
    });

}

function capitalizesentences() {
    var t = document.getElementById("thetext");

    var tarray = t.value.split(".");
    var tstr = '';
    for (i = 0; i < tarray.length; i++) {
        tarray[i] = ltrim(tarray[i], ' ');
        tstr = tstr + tarray[i].substring(0, 1).toUpperCase() + tarray[i].slice(1).toLowerCase();
        if (i < (tarray.length - 1)) tstr = tstr + '. ';
    }
    t.value = tstr;


    tarray = t.value.split("?");
    tstr = '';
    for (i = 0; i < tarray.length; i++) {
        tarray[i] = ltrim(tarray[i], ' ');
        tstr = tstr + tarray[i].substring(0, 1).toUpperCase() + tarray[i].slice(1);
        if (i < (tarray.length - 1)) tstr = tstr + '? ';
    }
    t.value = tstr;


    tarray = t.value.split("\n");
    tstr = '';
    for (i = 0; i < tarray.length; i++) {
        tarray[i] = ltrim(tarray[i], ' ');
        tstr = tstr + tarray[i].substring(0, 1).toUpperCase() + tarray[i].slice(1);
        if (i < (tarray.length - 1)) tstr = tstr + '\n';
    }
    t.value = tstr;


    tarray = t.value.split("!");
    tstr = '';
    for (i = 0; i < tarray.length; i++) {
        tarray[i] = ltrim(tarray[i], ' ');
        tstr = tstr + tarray[i].substring(0, 1).toUpperCase() + tarray[i].slice(1);
        if (i < (tarray.length - 1)) tstr = tstr + '! ';
    }
    t.value = tstr;
}

function replacetext() {
    var t = document.getElementById("thetext");
    var from = document.getElementById("from");
    var to = document.getElementById("to");

    var cs = document.getElementById("cs");
    var scope;

    var ff = from.value.replace("%N", "\n");
    var tt = to.value.replace("%N", "\n");

    if (cs.checked) scope = 'g';
    else scope = 'gi';

    var temp = t.value;
    temp = temp.replace(new RegExp(ff, scope), tt);
    t.value = temp;

    from.value = '';
    to.value = '';
    updatecounts();
}

function addtext() {
    var t = document.getElementById("thetext");
    var a = document.getElementById("add");
    var p = document.getElementById("addpos");
    var temp = t.value;
    var tstr = '';
    var tarray = t.value.split("\n");

    if (p.value == 'start') {
        for (i = 0; i < tarray.length; i++) {
            insert = a.value.replace("%L", i + 1);
            insert = insert.replace("%N", "\n");
            tstr = tstr + insert + tarray[i];
            if (i < (tarray.length - 1)) tstr = tstr + "\n";
        }
        t.value = tstr;
    } else {
        for (i = 0; i < tarray.length; i++) {
            insert = a.value.replace("%L", i + 1);
            insert = insert.replace("%N", "\n");
            tstr = tstr + tarray[i] + insert;
            if (i < (tarray.length - 1)) tstr = tstr + "\n";
        }
        t.value = tstr;
    }

    a.value = '';
    updatecounts();
}

function ltrim(str, chars) {
    chars = chars || "\\s";
    return str.replace(new RegExp("^[" + chars + "]+", "g"), "");
}

function rtrim(str, chars) {
    chars = chars || "\\s";
    return str.replace(new RegExp("[" + chars + "]+$", "g"), "");
}

function trimtext() {
    var t = document.getElementById("thetext");
    var n = document.getElementById("trimnumber");
    var p = document.getElementById("trimpos");
    var tarray = t.value.split("\n");
    var i;
    var tstr = '';

    if (p.value == 'first') {
        for (i = 0; i < tarray.length; i++) tstr = tstr + tarray[i].substr(n.value) + "\n";
        tstr = rtrim(tstr);
    } else {
        for (i = 0; i < tarray.length; i++) {
            tlen = tarray[i].length;
            tpos = tlen - n.value;
            tstr = tstr + tarray[i].substr(0, tpos) + "\n";
        }
        tstr = rtrim(tstr);
    }

    t.value = tstr;
    updatecounts();
}