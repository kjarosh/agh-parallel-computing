writeln("starting");

use BlockDist;
use AllLocalesBarriers;
use CommDiagnostics;
use CyclicDist;
use Barriers;
use Random;
use Time;

config const n = 1024 * 45 * 8;
config const max_val = 100;
config const eps = 0.1;
config const max_iter = n * n * 2;
config const expected_val: real = max_val / 2;

var t: Timer;

const S = {0..n-1};
const BS = S dmapped Block(boundingBox=S);
var u: [BS] real;

proc main() {
    var r = new RandomStream(real, 1);
    for v in u {
        v = r.getNext() * max_val;
    }
    writeln("expected val = ", expected_val);

    t.start();
    coforall L in Locales do on L {
        var localSubdomain = u.localSubdomain();
        writeln("on locale ", here.id, ", domain size ", localSubdomain.size);
        writeln("randomized");

        // startVerboseComm();
        for stepi in 0..max_iter-1 {
            if here.id == 0 && stepi % 1000 == 0 {
                writeln("iteration ", stepi);
            }

            const phase = stepi % 2;
            for i in localSubdomain {
                if i % 2 == phase {
                    var left = (i-1+n) % n;
                    var right = (i+1) % n;
                    u[i] = (u[left] + u[right]) / 2;
                }
            }

            allLocalesBarrier.barrier();

            if stepi % 200 == 0 {
                if checkConvergence(localSubdomain, stepi) { break; }
            }
        }
        stopVerboseComm();

        writeln("done ", here.id);
    }
    t.stop();

    writeln("time = ", t.elapsed());
}

const ErrorSpace = LocaleSpace dmapped Block(LocaleSpace);
var finish$: sync bool;
var globalError: real;

proc checkConvergence(localSubdomain, stepi) {
    var maxErr: real = 0;
    for i in localSubdomain {
        maxErr = max(maxErr, abs(expected_val - u[i]));
    }

    on globalError {
        globalError = max(globalError, maxErr);
    }

    if here.id == 0 {
        finish$.reset();
    }

    allLocalesBarrier.barrier();

    if here.id == 0 {
        var eps2 = globalError / expected_val;
        if eps2 <= eps {
            writeln("Converged! After ", stepi, " steps, err = ", globalError, ", eps = ", eps2);
            finish$ = true;
        } else {
            //  writeln("eps = ", eps2);
            finish$ = false;
        }
        globalError = 0;
    }
    return finish$.readFF();
}
