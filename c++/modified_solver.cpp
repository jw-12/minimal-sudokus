/* modified version for solving "Sudoku X", "Sudoku X"-modifications
made by Bo Haglund */
/* speed-optimized version of a
simple and short sudoku-solver based on an exact-cover-problem-solver
put into public domain by Guenter Stertenbrink,sterten@aol.com
compiles well with GCC3.2
some explanations are at : http://magictour.free.fr/suexco.txt
a not speed-optimized DOS/Windows-executable with more features
and attached source-code is at http://magictour.free.fr/suexk.exe
Report errors,bugs,improvement suggestions,feedback to sterten@aol.com
there are other programs here which are ~5 times faster, but
they are not public domain and presumably more complicated ;-)
This algo only searches for "naked single" and "hidden single"
I'm not 100% sure, whether this version works correctly with
the M1-array and rows-deletion before start
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <memory.h>
#include <string.h>

#define N 3 // change this for larger sudokus , N=4 for 16*16 etc.
#define N2 N*N
#define N4 N2*N2

static int Rows[ 5 * N4 + 1 ];
static int Row[ 5 * N4 + 1 ][ N2 + 1 ];
static int Cols[ N2 * N4 + 1 ];
static int Col[ N2 * N4 + 1 ][ 6 + 1 ];
static int Ur[ N2 * N4 + 1];
static int Uc[ 5 * N4 + 1 ];
static int V[ 5 * N4 + 1 ];
static int C[ N4 + 1 ];
static int I[ N4 + 1 ];

int A[N2+1][N2+1];
int Node[N4+1],M1[N4*N2];
int i,j,k,l,m0,m1,r,p,r1,c,c1,c2,n=N4*N2,m=4*N4+2*N2,x,y,s,min,clues,nodes;
int diagVers=2;  /* Normal Suduko diagVers=0, Sudoku X diagVers=1, Disjoint Groups = 2 */
char L[66]=".123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#*~";
// char L[66] is needed here for some compilers
FILE *file;

bool g_bIsSudokuX = false;
bool g_bIsSudokuDG = false;
void InitSolver();

int modified_solver()
   {

   p = 0;
   clock();
   if ( (file=fopen("copy_grid.txt","rb"))==NULL )
      {
      printf("\nError opening file \"%s\".\n\n", "copy_grid.txt");
      return -1;
      }

m6:
   i=0;
   for(x=1;x<=N2;x++)
      for(y=1;y<=N2;y++)
         {
m1:
         if(feof(file))
            {
            if(p<3)
               printf("time:%i/%i\n",clock(),CLOCKS_PER_SEC);
            return 0;
            }

         c=fgetc(file);
         j=0;
         if(c=='-' || c=='.'|| c=='0' || c=='*')
            goto m7;
         while(L[j]!=c && j<=N2)
            j++;
         if(j>N2)
            goto m1;
m7:
         A[x][y]=j;i++;
         }

   InitSolver();

for(i=1;i<=n;i++)Ur[i]=0;for(i=1;i<=m;i++)Uc[i]=0;for(i=1;i<=N4;i++)Node[i]=0;
clues=0;for(x=1;x<=N2;x++)for(y=1;y<=N2;y++)
if(A[x][y]){clues++;r=x*N4-N4+y*N2-N2+A[x][y];
for(j=1;j<=Cols[r];j++){c1=Col[r][j];if(Uc[c1]){printf("No solution exists.\n");goto m6;}
Uc[c1]++;for(k=1;k<=9;k++){Ur[Row[c1][k]]++;}}}
for(c=1;c<=m;c++){V[c]=0;for(i=1;i<=9;i++)if(Ur[Row[c][i]]==0)
{V[c]++;x=Row[c][i];Row[c][i]=Row[c][V[c]];Row[c][V[c]]=x;}Rows[c]=V[c];}

m1=0;for(c=1;c<=m;c++)if(V[c]<2 && Uc[c]==0){m1++;M1[m1]=c;}
i=clues;m0=0;nodes=0;
m2:i++;I[i]=0;min=n+1;if(i>N4 || m0)goto m4;
m22:if(m1==0)goto m21;if(Uc[M1[m1]]==0 && V[M1[m1]]==1){C[i]=M1[m1];m1--;goto m3;}
m1--;goto m22;
m21:if(nodes&1) for(c=1;c<=m;c++){if(!Uc[c])if(V[c]<min){min=V[c];C[i]=c;}}
if(!(nodes&1))for(c=m;c>=1;c--){if(!Uc[c])if(V[c]<min){min=V[c];C[i]=c;}}
//I don't like this very much. Better let c start at random position
if(min==0 || min>n)goto m4;
m3:c=C[i];I[i]++;if(I[i]>Rows[c])goto m4;
r=Row[c][I[i]];if(Ur[r])goto m3;m0=0;

if(p){k=N4;j=N2;x=(r-1)/k+1;y=((r-1)%k)/j+1;s=(r-1)%j+1;A[x][y]=s;
  if(i==N4){for(x=1;x<=N2;x++)for(y=1;y<=N2;y++)printf("%c",L[A[x][y]]);printf("\n");if(p==1)goto m6;}}

for(j=1;j<=Cols[r];j++){c1=Col[r][j];Uc[c1]++;}
for(j=1;j<=Cols[r];j++){c1=Col[r][j];
for(k=1;k<=Rows[c1];k++){r1=Row[c1][k];Ur[r1]++;if(Ur[r1]==1)
for(l=1;l<=Cols[r1];l++){c2=Col[r1][l];V[c2]--;
if(Uc[c2]+V[c2]<1)m0=c2;if(Uc[c2]==0 && V[c2]<2){m1++;M1[m1]=c2;}}}}

nodes++;Node[i]++;goto m2;
//m4:i--;c=C[i];r=Row[c][I[i]];if(i==clues){if(p==0)printf("%i\n",Node[N4]);goto m6;}
m4:i--;c=C[i];r=Row[c][I[i]];if(i==clues){if(p==0)fclose(file);return Node[N4];}
for(j=1;j<=Cols[r];j++){c1=Col[r][j];Uc[c1]--;
for(k=1;k<=Rows[c1];k++){r1=Row[c1][k];Ur[r1]--;
if(Ur[r1]==0)for(l=1;l<=Cols[r1];l++){c2=Col[r1][l];V[c2]++;}}}
goto m3;
}

#define ZeroMemory( array ) memset( (array), 0, sizeof( array ) );

void InitSolver()
   {
   /* Here starts initialization code. This code only needs to be executed the first time
   that the solver is called. If the solver then is repeatedly called, the initialization
   code can be lifted out and placed in a separate routine.*/
   m = 4*N4;
   if ( g_bIsSudokuX )
      m += 2*N2;
   else if ( g_bIsSudokuDG )
      m += N4;

   int r = 0;
   for ( int x = 1;  x <= N2;  x++ )
      for ( int y = 1; y <= N2;  y++ )
         for ( int s = 1;  s <= N2;  s++ )
            {
            r++;
            Cols[r]=4;
            Col[r][1] = x*N2-N2+y;
            Col[r][2] = (N*((x-1)/N)+(y-1)/N)*N2+s+N4;
            Col[r][3] = x*N2-N2+s+N4*2;
            Col[r][4] = y*N2-N2+s+N4*3;

            /* Following is additional code for adding columns for "Sudoku X" */
            if ( g_bIsSudokuX )
               {
               if ( x == y )
                  {
                  Col[r][5] = s + N4*4;
                  if ( x == (1 + N2-y) )
                     {
                     Cols[r]=6;
                     Col[r][6]=s+N2+N4*4;
                     }
                  else
                     Cols[r]=5;
                  }
               else if ( x == (1 + N2 - y) )
                  {
                  Cols[r]=5;
                  Col[r][5]=s+N2+N4*4;
                  }
               }
            else if ( g_bIsSudokuDG )
               {
               Cols[r] = 5;
               Col[r][5] = ((x-1)%3 + 3*((y-1)%3))*N2 + s + N4*4;
               }
            }

   ZeroMemory( Rows );
   for ( r = 1;  r <= n;  r++ )
      for ( int c = 1;  c <= Cols[ r ];  c++ )
         {
         int x = Col[ r ][ c ];
         Rows[ x ]++;
         Row[ x ][ Rows[ x ] ] = r;
         }
   /* Here ends the initialization code. */
   }
