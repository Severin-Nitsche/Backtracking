import java.util.ArrayList;

public class SudokuSolver {

  private static boolean test(byte[][] sudoku, int y, int x) {
    for(int i = 0; i < 9; i++) {
      if(x != i) {
        if(sudoku[y][i] == sudoku[y][x]) return false;
      }
      if(y != i) {
        if(sudoku[i][x] == sudoku[y][x]) return false;
      }
    }
    int qx = x / 3;
    int qy = y / 3;
    for(int i = 0; i < 3; i++) {
      for(int j = 0; j < 3; j++) {
        if(qy*3+i != y || qx*3+j != x) {
          if(sudoku[qy*3+i][qx*3+j] == sudoku[y][x]) return false;
        }
      }
    }
    return true;
  }

  /**
  *
  * @params byte[][] sudoku - the sudoku with sudoku[y][x]. Free Entries have to be -1.
  *
  */
  public static byte[][] solve(byte[][] sudoku) {
    ArrayList<int[]> lastIndecies = new ArrayList<int[]>();
    int k = 1;
    for(int i = 0; i < sudoku.length; i++) {
      for(int j = 0; j < sudoku[i].length; j++) {

        boolean con = true;

        if(sudoku[i][j] == -1) {
          con = false;
          int[] index = {i,j};
          lastIndecies.add(index);
          for(k=k; k<10; k++) {
            sudoku[i][j] = (byte)k;
            if(test(sudoku, i, j)) {
              con = true;
              k = 1;
              break;
            }
          }
        }

        if(con) continue;
        sudoku[i][j] = -1;
        lastIndecies.remove(lastIndecies.size()-1);
        int last[] = lastIndecies.get(lastIndecies.size()-1);
        lastIndecies.remove(lastIndecies.size()-1);
        k = sudoku[last[0]][last[1]] + 1;
        sudoku[last[0]][last[1]] = -1;
        i = last[0];
        j = last[1] - 1;
      }
    }
    return sudoku;
  }

  public static void print(byte[][] sudoku) {
    for(int i = 0; i < sudoku.length; i++) {
      for(int j = 0; j < sudoku[i].length; j++) {
        System.out.print((j%3==0&&j!=0?" || ":" | ")+sudoku[i][j]);
      }
      System.out.println(((i+1)%3==0&&i!=0?"\n--------------------------------------":""));
    }
    System.out.println();
  }

  public static void main(String[] args) {
    byte[][] sudoku = {
      {1,2,3, 4,5,6, 7,8,9},
      {4,5,6, 7,8,9, 1,2,3},
      {7,8,9, 1,2,3, 4,5,6},

      {2,3,4, 5,6,7, 8,9,1},
      {5,6,7, 8,9,1, 2,3,4},
      {8,9,1, 2,3,4, 5,6,7},

      {3,4,5, 6,7,8, 9,1,2},
      {6,7,8, 9,1,2, 3,4,5},
      {9,1,2, 3,4,5, 6,7,8},
    };
    for(int i = 0; i<1000; i++) {
      sudoku[(int)(Math.random()*9)][(int)(Math.random()*9)] = -1;
    }
    print(sudoku);
    solve(sudoku);
    print(sudoku);
  }

}
