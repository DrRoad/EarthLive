package com.siddhantfriends.nasa.spaceapps16;

import org.apache.commons.io.FileUtils;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

public class Main {

    private static final String TEST_URL = "http://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGHHE.03/2016/001/3B-HHR-E.MS.MRG.3IMERG.20160101-S000000-E002959.0000.V03E.HDF5.ascii?";
    private static final String PERCIPITATION = "HQprecipitation[0:1:3599][0:1:1799]";
    private static final String TIMESTAMP = "HQobservationTime[0:1:3599][0:1:1799]";
    private static final String LAT_LON = "lat[0:1:1799],lon[0:1:3599]";


    public static void main(String[] args) {
        // Get the lat and long
        getQueryDataToFile(LAT_LON, "LatLon.csv");

        // Get the percipitation
        getQueryDataToFile(PERCIPITATION, "Percipitation.csv");

        // Get timestamp
        getQueryDataToFile(TIMESTAMP, "TimeStamp.csv");

    }

    public static void getQueryDataToFile(String query, String filename) {
        boolean firstLine = true;
        URL url = null;
        try {
            url = new URL(TEST_URL + query);

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
