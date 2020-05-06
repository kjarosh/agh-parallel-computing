// in allows changing the parameter inside function, inout allows changing it outside but writes on exit, ref changes immediately
proc inc(ref x: int) : void
{
	x = x+1;
}

var a = 1;
writeln("before: " + (a : string));
inc(a);
writeln("after: " + (a : string));