program avance1;

main {
	var int x1;
	var int i;
	
	x1 = 0;
	i = 0;
	
	while (i < 10){
		x1 = x1 + i;
		i = i + 1;
	}
	
	print(x1);
}