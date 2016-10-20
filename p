program avance1; 

main {
	var int myInt;
	var bool isBigger;
		
	var int i;
	i = 0;
	while (i < 10)
	{
	 	isBigger = i <= myInt;
		
		if (isBigger)
		{
			myInt = myInt + i;
		}
		i = i + 1;
	}
}