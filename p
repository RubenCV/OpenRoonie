program openRoon;

function int sum0toX (int input){
	var int ret;
	ret = input + 1;
	return ret;
}


main {

	var int x1;
	
	x1 = 10;
	x1 = sum0toX(x1);

	print("X1: ", x1,"\n");
}