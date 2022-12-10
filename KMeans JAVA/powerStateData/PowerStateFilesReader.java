package kmeans.powerStateData;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class PowerStateFilesReader {

    public static double[][] getPowerStateValues(int row, int col) throws IOException {
        int index1 = 0, index2 = 0;
        double[] timestamps = new double[40];
        double[] nightTimestamps = new double[40];
        File dir = new File("E:\\pyhton\\psd");

        for (File folder : dir.listFiles()) {
            double timeStampSum = 0.0;
            double nightTimeStampSum = 0.0;
            double count = 0.0;
            double countNight = 0.0;
            for (File inputFolder : folder.listFiles()){
                if (inputFolder.getName().equals("power_state"))
                for (File file : inputFolder.listFiles()) {
                    try (FileReader fr = new FileReader(file); BufferedReader br = new BufferedReader(fr)) {
                        String line;
                        while ((line = br.readLine()) != null) {
                            if (line.startsWith("timestamp")) break;
                        }
                        boolean dataFound = false, nightDataFound = false;
                        int onOffCheck = -1;
                        double pastTimeStamp = 0.0;
                        while ((line = br.readLine()) != null) {
                            String[] splitLine = line.split(",");
                            String[] splitUTCtime = splitLine[1].split("T");
                            String[] splitDate = splitUTCtime[0].split("-");
                            String[] splitTime = splitUTCtime[1].split(":");
                            //2022-08-07T18:34:26.123
                            //double currTimeStamp = (((Integer.parseInt(splitDate[1])-8)*24)+((Integer.parseInt(splitDate[2])-7))*24);
                            double currTimeStamp = Double.parseDouble(splitTime[1]) * 60 + Double.parseDouble(splitTime[2]);
                            if (splitLine[2].equals("Screen turned off") && onOffCheck >= 0) {
                                double screenOnPeriod = currTimeStamp - pastTimeStamp;
                                timeStampSum += screenOnPeriod;
                                if (Integer.parseInt(splitTime[0]) >= 18 && Integer.parseInt(splitTime[0]) < 23) {
                                    nightTimeStampSum += screenOnPeriod;
                                    nightDataFound = true;
                                }
                                dataFound = true;
                                onOffCheck = -1;
                            } else if (splitLine[2].equals("Screen turned on")) {
                                pastTimeStamp = currTimeStamp;
                                onOffCheck = 1;
                            }
                        }
                        if (dataFound) count += 1.0;
                        if (nightDataFound) countNight += 1.0;
                    }
                }
            }
            if( count != 0.0 ) {
                timestamps[index1++] = timeStampSum / count;
                if (countNight != 0.0) {
                    nightTimestamps[index2++] = nightTimeStampSum / countNight;
                }else{
                    nightTimestamps[index2++] = 0.0;
                }
            }
        }
        double[][] powerStateValues = new double[row][col];
        for(int i=0; i<row; i++){
            powerStateValues[i][0] = timestamps[i];
            powerStateValues[i][1] = nightTimestamps[i];
        }

        return powerStateValues;
    }
}
