package com.siddhantfriends.nasa.spaceapps16;

import org.apache.commons.io.FileUtils;

import java.io.*;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {


    private static final String PERCIPITATION = "HQprecipitation[0:1:3599][0:1:1799]";
    private static final String TIMESTAMP = "HQobservationTime[0:1:3599][0:1:1799]";
    private static final String LAT_LON = "lat[0:1:1799],lon[0:1:3599]";


    // DATA PARSER
    public static final String LAT_LON_FILE = "LatLon.csv";
    public static final String PERCIPITATION_FILE = "Percipitation.csv";
    public static final String TIMESTAMP_FILE = "TimeStamp.csv";
    public static final String URLS_FILE = "urls.txt";

    public static List<String> latitude = new ArrayList<>();
    public static List<String> longitude = new ArrayList<>();
    public static List<List<String>> percipitation = new ArrayList<>();
    public static List<List<String>> timeStamp = new ArrayList<>();
    public static RainfallUploader rainfallUploader = new RainfallUploader();

    public static void main(String[] args) {
        // Read urls
        // get latitude and longitude
        File file = new File(URLS_FILE);
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                String[] data = line.split(",");
                String urlString = data[0];
                String StartTime = getDateTime(data[1]);
                String StopTime = getDateTime(data[2]);


                // Get the lat and long
                getQueryDataToFile(urlString, LAT_LON, LAT_LON_FILE);

                // Get the percipitation
                getQueryDataToFile(urlString, PERCIPITATION, PERCIPITATION_FILE);

                // Get timestamp
                getQueryDataToFile(urlString, TIMESTAMP, TIMESTAMP_FILE);



                // get latitude and longitude
                File file2 = new File(LAT_LON_FILE);
                try (BufferedReader bufferedReader = new BufferedReader(new FileReader(file2))) {
                    String line2;

                    while ((line2 = bufferedReader.readLine()) != null) {
                        String[] data2 = line2.split(",");
                        List<String> dataList = Arrays.asList(data2);
                        if ("lat".equalsIgnoreCase(dataList.get(0))) {
                            latitude = (dataList.subList(1, (dataList.size())));
                        } else if ("lon".equalsIgnoreCase(dataList.get(0))) {
                            longitude = (dataList.subList(1, (dataList.size())));
                        }
                    }
                    bufferedReader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }

                // get percipitation
                file2 = new File(PERCIPITATION_FILE);
                try (BufferedReader bufferedReader = new BufferedReader(new FileReader(file2))) {
                    String line2;
                    while ((line2 = bufferedReader.readLine()) != null) {
                        String[] data2 = line2.split(",");
                        List<String> dataList = Arrays.asList(data2);
                        percipitation.add(dataList.subList(1, dataList.size()));
                    }
                    bufferedReader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }

                // get timestamp
                file2 = new File(TIMESTAMP_FILE);
                try (BufferedReader bufferedReader = new BufferedReader(new FileReader(file2))) {
                    String line2;
                    while ((line2 = bufferedReader.readLine()) != null) {
                        String[] data2 = line2.split(",");
                        List<String> dataList = Arrays.asList(data2);
                        dataList = dataList.subList(1, dataList.size());
                        for (int i = 0; i < dataList.size(); i++) {
                            String time = dataList.get(i).trim();
                            int ftime = Integer.parseInt(StartTime.substring(10, 12));
                            if (!time.equalsIgnoreCase("-9999")) {
                                ftime = Integer.parseInt(time) + ftime;
                                dataList.set(i, Integer.toString(ftime));;
                            } else {
                                dataList.set(i, null);
                            }

                        }
                        timeStamp.add(dataList);
                    }
                    bufferedReader.close();
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



                            String temp = "{ \"timestamp\": \"" + StartTime + "\", \"latitude\": " + latitude.get(j)
                                    + ", \"longitude\": " + longitude.get(i) + ", \"precipitation\": " + percipitationLonLat + " }";

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
                    try {
                        rainfallUploader.uploadJson(jsonString);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }


            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

    public static String getDateTime(String time) {
        // Input format  =  StartGranuleDateTime=2015-03-31T19:00:00.000
        // Output format = YYYYMMDDHHmm
        String[] tempArr = time.split("=");
        String temp = tempArr[1];
        tempArr = temp.split("T");
        String timeDate = tempArr[0];
        String timeTime = tempArr[1];
        tempArr = timeDate.split("-");
        timeDate = tempArr[0] + tempArr[1] + tempArr[2];
        tempArr = timeTime.split(":");
        timeTime = tempArr[0] + tempArr[1];
        return timeDate + timeTime;
    }

    public static void getQueryDataToFile(String urlString, String query, String filename) {
        boolean firstLine = true;
        URL url = null;
        try {
            url = new URL(urlString + query);

            URLConnection urlConnection = url.openConnection();
            BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            StringBuilder builder = new StringBuilder();
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                if (firstLine) {            // Skipping first line - this is basically file name
                    firstLine = false;
                    continue;
                }
                builder.append(inputLine + "\n");
            }

            File exportFile = new File(filename);
            FileUtils.writeStringToFile(exportFile,builder.toString());

            in.close();
            System.out.println("Success!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
