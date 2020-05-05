use Time;
use Random;
use CommDiagnostics;

config const size = 12;

proc getMinor(tab, column, size) {
    var n = size - 1;
    var minor: [1..n, 1..n] real;
    var k = 1;
    var l = 1;
    for i in 2..size do {
        for j in 1..size do {
            if j != column then {
                minor(k, l) = tab(i, j);
                l += 1;
            }
        }
        l = 1;
        k += 1;
    }
    return minor;
}

proc calculateDet(tab, size): real {
    if size == 1 then {
        return tab(1, 1);
    }
    var det: real = 0.0;
    for j in 1..size do {
        var minor = getMinor(tab, j, size);
        var sig = 0;
        if j % 2 == 0 then
            sig = 1;
        else
            sig = -1;
        det += tab(1, j) * sig * calculateDet(minor, size - 1);
    }
    return det;
}

proc copy(matrix, size) {
    var tab: [1..size, 1..size] real;
    for i in 1..size {
        for j in 1..size {
            tab(i, j) = matrix(i, j);
        }
    }
    return tab;
}

proc main() {
    var timer = new Timer();
    timer.start();
    var sum: atomic real = 0;
    var matrix: [1..size, 1..size] real;
    fillRandom(matrix);
    writeln("tab: ", matrix);

    startVerboseComm();
    coforall L in Locales do on L {
        writeln("here id ", here.id);
        var tab = copy(matrix, size);
        var res = 0.0;
        for j in (here.id+1)..size by numLocales {
            var minor = getMinor(tab, j, size);
            var sig = 0;
            if j % 2 == 0 then
                sig = 1;
            else
                sig = -1;
            res += tab(1, j) * sig * calculateDet(minor, size - 1);
        }
        sum.fetchAdd(res);
    }
    stopVerboseComm();
    writeln("det ", sum);
    timer.stop();
    writeln("time ", timer.elapsed());
}
