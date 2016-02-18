package com.github.alexkuck.geoff;

import java.lang.Integer;

public class City {
    // 3	2399697	Libreville	GA	01	578156	0.39241	9.45356	2012-04-25
    // bucket, geonameid, city name (utf8), country code, admin1 code, population, lat, lon, modification date

    private int bucket;
    private int geonameId;
    private String cityName;
    private String countryCode;
    private String admin1Code;
    private int population;
    private double lat;
    private double lon;
    private String modDate;
    private double distance;

    public City(String row, double myLat, double myLon) {
        parseRow(row);
        distance = distanceTo(myLat, myLon);
    }

    private void parseRow(String row) {
        String delimiter = "\t";
        String[] cityRow = row.split(delimiter);

        this.bucket = Integer.parseInt(cityRow[0]);
        this.geonameId = Integer.parseInt(cityRow[1]);
        this.cityName = cityRow[2];
        this.countryCode = cityRow[3];
        this.admin1Code = cityRow[4];
        this.population = Integer.parseInt(cityRow[5]);
        this.lat = Double.parseDouble(cityRow[6]);
        this.lon = Double.parseDouble(cityRow[7]);
        this.modDate = cityRow[8];
    }

    public double distanceTo(double myLat, double myLon) {
        double latDif = this.getLat() - myLat;
        double lonDif = this.getLon() - myLon;
        double sumOfSquares = Math.pow(latDif, 2) + Math.pow(lonDif, 2);
        double distance = Math.sqrt(sumOfSquares);
        return distance;
    }

    public boolean isCloser(City comparingCity) {
        if(comparingCity == null)
            return true;
        if(this.getDistance() < comparingCity.getDistance())
            return true;
        return false;
    }

    public int getBucket() {
        return this.bucket;
    }

    public int getGeonameId() {
        return this.geonameId;
    }

    public String getCityName() {
        return this.cityName;
    }

    public String getAdmin1Code() {
        return this.admin1Code;
    }

    public long getPopulation() {
        return this.population;
    }

    public double getLat() {
        return this.lat;
    }

    public double getLon() {
        return this.lon;
    }

    public String getModDate() {
        return this.modDate;
    }

    public double getDistance() {
        return this.distance;
    }
}
