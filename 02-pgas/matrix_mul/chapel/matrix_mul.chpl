use Random;
use Time;
use BlockDist;	


config const seed = 1234 : int;
config const size = 100 : int;
config const repetitions = 1 : int;

const S = {1..size, 1..size};
const BS = S dmapped Block(boundingBox=S);


proc generate_array(seed: int, size: int)
{
	var a: [1..size, 1..size] real;
	fillRandom(a, seed);
	return a;
}

proc singlemul(a, b, i, j, size) : real
{
	var res : atomic real;
	res.write(0.0);
	for it in 1..size {
		res.write(a(it, j) * b(i, it) + res.read());
	}

	return res.read();
}

proc multiply(a, b, size)
{
	var res: [1..size, 1..size] real;

	coforall L in Locales do on L {
        var localSubdomain = a.localSubdomain();

		for (i,j) in localSubdomain {
			// writeln('idx ' + str(i,j) + )
			//a x b
			res(i,j) = singlemul(a,b,i,j,size);
		}
	}
	return res;
}

proc main(args: [] string) {
	var total_time = 0 : real(64);
	var timer = new Timer();

	var a1 : [BS] real = generate_array(seed, size);
	var a2 : [BS] real = generate_array(seed, size);

	for i in 1..repetitions {
		timer.clear();
		timer.start();
		
		var res = multiply(a1, a2, size);

		timer.stop();
		total_time += timer.elapsed();
	}
	writeln((total_time/repetitions):string + "s");
}