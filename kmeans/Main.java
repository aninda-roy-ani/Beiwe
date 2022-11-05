package kmeans;

import kmeans.powerStateData.PowerStateFilesReader;

import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {

        KMeansClustering object = new KMeansClustering();
        object.setRow(40);
        object.setColumn(4);
        object.setcRow(10);
        object.setData(PowerStateFilesReader.getPowerStateValues(object.getRow(),object.getColumn()));
        object.showData();
        object.setRandomClusterArray(object.randomClusters(object.getData()));
        object.printClusterArrayAndIndexes(object.getRandomClusterArray(),
                object.newClusters(object.indexArray(object.getData(), object.getRandomClusterArray()),
                        object.getData()));



    }
}