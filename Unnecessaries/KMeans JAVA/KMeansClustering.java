package kmeans;

import java.util.Arrays;
import java.util.Random;

public class KMeansClustering {

    private int row, column, cRow;
    private double[][] data = new double[row][column];
    private double[][] randomClusterArray = new double[cRow][column];

    public KMeansClustering() {
    }

    public int getRow() {
        return row;
    }

    public void setRow(int row) {
        this.row = row;
    }

    public int getColumn() {
        return column;
    }

    public void setColumn(int column) {
        this.column = column;
    }

    public int getcRow() {
        return cRow;
    }

    public void setcRow(int cRow) {
        this.cRow = cRow;
    }

    public double[][] getData() {
        return data;
    }

    public void setData(double[][] data) {
        this.data = data;
    }

    public double[][] getRandomClusterArray() {
        return randomClusterArray;
    }

    public void setRandomClusterArray(double[][] randomClusterArray) {
        this.randomClusterArray = randomClusterArray;
    }

    public double[][] initializingRandomData() {
        Random random = new Random();
        double data[][] = new double[row][column];
        for(int i=0; i<row; i++){
            for(int j=0; j<column; j++){
                data[i][j] = (int)random.nextDouble(900)+100.0;
            }
        }

        this.setRandomClusterArray(this.randomClusters(data));
        return data;
    }

    public void showData(){
        String arrayDescription = "\nRow: " + this.row + "\nColoumn: " + this.column + "\nNumber of clusters: " + this.cRow +"\n\nData:\n";
        for(int i=0; i< this.row; i++) {
            for (int j = 0; j < this.column; j++) {
                arrayDescription += this.data[i][j] + " ";
            }
            arrayDescription += "\n";
        }
        System.out.println(arrayDescription);
    }

    public double[][] randomClusters(double[][] data){
        Random random = new Random();
        int[] index = new int[this.cRow];
        double[][] clusters = new double[this.cRow][this.column];
        for(int i=0; i<this.cRow; i++){
            index[i] = random.nextInt(this.row);
            for(int j=0; j<i; j++){
                if (index[j] == index[i]) {
                    --i;
                    break;
                }
            }
        }
        System.out.println("Random Clusters:");
        for(int i=0; i<this.cRow; i++){
            for(int j=0; j<this.column; j++) {
                clusters[i][j] = data[index[i]][j];
                System.out.print(clusters[i][0]+" ");
            }
            System.out.println("");
        }
        System.out.println("");
        return clusters;
    }

    public int[] indexArray(double[][] data, double[][] clusters){
        int[] indexes = new int[this.row];
        for(int i=0; i<this.row; i++){
            double val = 99999999;
            int index = 99;
            for(int j=0; j<this.cRow; j++){
                double valNew = 0;
                for(int k=0; k<this.column; k++) {
                    //System.out.println("here"+ valNew + " " + val + " " + i + " " + j + " " + k);
                    valNew += Math.pow((data[i][k] - clusters[j][k]), 2);
                }
                if (valNew<val) {
                    index = j;
                    val = valNew;
                }
            }
            indexes[i] = index;
        }
        String array = "IndexArray:\n";
        for(int i=0; i<this.row; i++)
            array += indexes[i] + " ";
        System.out.println(array+"\n");
        return indexes;
    }

    public double[][] newClusters(int[] indexes, double[][] data){
        double[][] clusters = new double[this.cRow][this.column];
        for(int i=0; i<this.cRow; i++){
            double[] sum = new double[this.column];
            for(int k=0; k<this.column; k++) {
                sum[k] = 0;
            }
            int count = 0;
            for(int j=0; j<this.row; j++){
                if (indexes[j] == i){
                    ++count;
                    for(int k=0; k<this.column; k++) {
                        sum[k] += data[j][k];
                    }
                }
            }
            for(int k=0; k<this.column; k++) {
                clusters[i][k] =  sum[k]/count;
            }
        }
        return clusters;
    }

    public void printClusterArrayAndIndexes(double[][] oldClusters, double[][] newClusters){
        System.out.println("Old Clusters: ");
        for(int i=0; i<this.cRow; i++){
            for(int k=0; k<this.column; k++) {
                System.out.print(oldClusters[i][k] + " ");
            }
            System.out.println("");
        }
        System.out.println("\nNew Clusters: ");
        for(int i=0; i<this.cRow; i++){
            for(int k=0; k<this.column; k++) {
                System.out.print(newClusters[i][k] + " ");
            }
            System.out.println("");
        }
        System.out.println("");
        for(int i=0; i<this.cRow; i++){
            for(int j=0; j<this.column; j++){
                if (oldClusters[i][j] != newClusters[i][j]){
                    printClusterArrayAndIndexes(newClusters,this.newClusters(this.indexArray(this.getData(), newClusters),this.getData()));
                    return;
                }
            }
        }
        System.out.println("\n\nFinal ClusterArray: ");
        for(int i=0; i<this.cRow; i++){
            for(int k=0; k<this.column; k++) {
                System.out.print(newClusters[i][k] + " ");
            }
            System.out.println("");
        }
        System.out.print("\nFinal ");
        int[] indexArray = this.indexArray(this.getData(),newClusters);

        for(int i=0; i<this.cRow; i++){
            int groupNo = i+1;
            System.out.print("Group " + groupNo + " : ");
            for (int j=0; j<this.row; j++){
                if (indexArray[j] == i){
                    int serialNo = j+1;
                    System.out.print( serialNo+ "  ");
                }
            }
            System.out.println("");
        }
        return;
    }
}
