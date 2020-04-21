#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cstring>
#include <ctime>

#include "modified_solver.h"


using namespace std;

int writeToCopyFile(string cp_grid);
int writeToOutputFile(int row_ind, string puzzle, double exec_time);
string readSolution(int index);

int main( int argc, char const* argv[] )
{
    string grid;
    int file_row_ind = 1; //start from 1
    string copy_grid;
    int rem_indexes [81] = { 0 };
    int rand_ind;
    bool all_tried;
    clock_t start;
    double exec_time;

    //LOOP
    for(;file_row_ind<35786;file_row_ind++) {


        //GET SOLN FROM FILE
        grid = readSolution(file_row_ind);
        //cout<<"current: "<<file_row_ind<<": "<<grid<<endl;

        //string grid = "327458619156972348894316527431587962769241853285639174542193786673825491918764235";
        //string grid = "000010538700000006208005001000000010590300000000090200050103600402500000000026000";
        memset(rem_indexes, 0, sizeof(rem_indexes));
        all_tried = false;

        //start timer
        start = clock();

        while(!all_tried)
        {

            //loop
            copy_grid = grid;

            //remove a clue then solve
            rand_ind = rand() % 81;
            while(rem_indexes[rand_ind] == 1) {
                rand_ind = rand() % 81;
                //cout << "attempted remove " << rand_ind<<endl;
            }

            rem_indexes[rand_ind] = 1;
            copy_grid[rand_ind] = '0';

            //write to file to be read by solver
            writeToCopyFile(copy_grid);

            if (modified_solver() < 2) {
                grid[rand_ind] = '0';
            }

            //check if all have been attempted
            all_tried = true;
            for (int i=0;i<81;i++) {
                if (rem_indexes[i]==0) {
                    all_tried = false;
                    break;
                }
            }
        }

        exec_time = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;

        //cout << grid<<endl;
        //cout << exec_time<<endl;

        //writeToOutputFile(file_row_ind, grid, exec_time);
    }
    return 0;
}


string readSolution(int index) {
    ifstream soln_file("db_solutions_only.csv");
    string line;
    string grid;
    int i=0;
    int j;

    while(i < index) {
        getline(soln_file, line);
        i++;
    }

    j = line.find(",", 0) + 1;

    grid = line.substr(j, line.length());
    soln_file.close();

    return grid;
}


int writeToOutputFile(int row_ind, string puzzle, double exec_time) {
    ofstream write_file ("output.csv", fstream::app);
    write_file << row_ind << "," << puzzle << "," << exec_time << endl;
    write_file.close();
    return 0;
}


int writeToCopyFile(string cp_grid)  //write the grid to test to a file
{
  ofstream copy_file ("copy_grid.txt", std::ofstream::trunc);
  copy_file << cp_grid;
  copy_file.close();
  return 0;
}
