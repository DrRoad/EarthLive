package com.siddhantfriends\nasa\spacesapps16;

import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Send HTTP REST Request to upload a Rainfall Record or group of Rainfall Records
 * 
 * @author Andy Bowes
 */
public class RainfallUploader {

	private final String url;

	public RainfallUploader(){
		url = "http://earthlive.westeurope.cloudapp.azure.com:8888/upload";
	}

	public boolean uploadJson(String json) throws IOException{
		OutputStream os = null;
		int responseCode = 500;
		try {
			URL obj = new URL(url);
			HttpURLConnection con = (HttpURLConnection) obj.openConnection();
			con.setRequestMethod("POST");
			con.setRequestProperty("Content-Type", "application/json");
			os = con.getOutputStream();
			os.write(json.getBytes());
			os.flush();
			os.close();
			responseCode = con.getResponseCode();
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				if (os != null){
					os.close();
				}
			} catch (IOException e) {
				
			}
		}
		return responseCode == 200;
	}

}
