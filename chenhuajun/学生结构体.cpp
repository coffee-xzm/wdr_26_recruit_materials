#include<iostream>
using namespace std;

struct Student
{
	string name;
	int id;
	int score;
};

void printStudent(const Student& s)
{
	cout<<s.name<<" "<<s.id<<" "<<s.score<<endl;
}

Student* findTopStudent(Student arr[], int n)
{
	Student* topStudent = &arr[0];
	for(int i=1;i<n;i++)
	{
		if(arr[i].score>(*topStudent).score)
		{
			topStudent = &arr[i];
		}
		return topStudent;
	}
}

int main() 
{
    int n;
    cin >> n;
    Student students[n];

    for (int i = 0; i < n; i++)
	{
    	cin >> students[i].name >> students[i].id >> students[i].score;
	}
	Student* topStudent = findTopStudent(students, n);
	printStudent(*topStudent);
	return 0;
}
