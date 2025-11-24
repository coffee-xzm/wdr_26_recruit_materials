#include<iostream>
#include<cmath>
using namespace std;

float zero(float a,float b,float c)
{
	float value = -b/2*a;
	return value;
}

float morethanzero1(float a,float b,float c)
{
	float temp1 = -b+sqrt(b*b-4*a*c);
	float value1 = temp1 / 2*a;
	return value1;
}

float morethanzero2(float a,float b,float c)
{
	float temp2 = -b-sqrt(b*b-4*a*c);
	float value2 = temp2 / 2*a;
	return value2;
}

void lessthanzero(float a,float b,float c)
{
	cout<<"该方程无实数根"<<endl;
}

int main()
{
	float a,b,c;
	cin>>a>>b>>c;
	float delta = b*b-4*a*c;
	if(delta == 0)
	{
		float value = zero(a,b,c);
		cout<<value<<endl;
	}
	else if(delta > 0)
	{
		float value1 = morethanzero1(a,b,c);
		float value2 = morethanzero2(a,b,c);
		cout<<value1<<" "<<value2<<endl;
	}
	else
	{
		lessthanzero(a,b,c);
	}
	return 0;
}
