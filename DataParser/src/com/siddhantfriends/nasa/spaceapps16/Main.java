package com.siddhantfriends.nasa.spaceapps16;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {

    // DATA PARSER
    public static final String LAT_LON = "LatLon.csv";
    public static final String PERCIPITATION = "Percipitation.csv";
    public static final String TIME_STAMP = "TimeStamp.csv";

    public static List<String> latitude = new ArrayList<>();
    public static List<String> longitude = new ArrayList<>();
    public static List<List<String>> percipitation = new ArrayList<>();
    public static List<List<String>> timeStamp = new ArrayList<>();

    public static void main(String[] args) {
        // get latitude and longitude
        File file = new File(LAT_LON);
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                String[] data = line.split(",");
                List<String> dataList = Arrays.asList(data);
                if ("lat".equalsIgnoreCase(dataList.get(0))) {
                    latitude = (dataList.subList(1, (dataList.size())));
                } else if ("lon".equalsIgnoreCase(dataList.get(0))) {
                    longitude = (dataList.subList(1, (dataList.size())));
                }
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // get percipitation
        file = new File(PERCIPITATION);
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] data = line.split(",");
                List<String> dataList = Arrays.asList(data);
                percipitation.add(dataList.subList(1, dataList.size()));
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // get timestamp
        file = new File(TIME_STAMP);
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] data = line.split(",");
                List<String> dataList = Arrays.asList(data);
                dataList = dataList.subList(1, dataList.size());
                for (int i = 0; i < dataList.size(); i++) {
                    String time = dataList.get(i).trim();
                    int ftime = 0;              // ToDo - Add MM from time here
                    if (!time.equalsIgnoreCase("-9999")) {
                        ftime = Integer.parseInt(time) + ftime;
                        dataList.set(i, Integer.toString(ftime));;
                    } else {
                        dataList.set(i, null);
                    }

                }
                timeStamp.add(dataList);
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


        // output json
        StringBuilder jsonBuilder = new StringBuilder();
        for (int i = 0; i < percipitation.size(); i++) {
            List<String> percipitationLat = percipitation.get(i);
            String jsonString = "";
            jsonString += "[";
            for (int j = 0; j < percipitationLat.size(); j++) {
                String percipitationLonLat = percipitationLat.get(j).trim();

                if(!percipitationLonLat.equalsIgnoreCase("-9999.9")) {
                    // This is the case where you generate all the data



                    String temp = "{ \"timestamp\": \"\", \"lat\": " + latitude.get(j)
                            + ", \"lon\": " + longitude.get(i) + ", \"precipitation:\" " + percipitationLonLat + " }";

                    if(!temp.trim().equalsIgnoreCase("")) {
                        if (!jsonString.equalsIgnoreCase("[")) {
                            jsonString +=", ";
                        }
                        jsonString += temp;
                    }
                }
            }

            jsonString += "]";
            // ToDo - Send Post here
            System.out.println(jsonString);
        }

    }


}
