package com.github.alexkuck.geoff;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

public class OfflineGeocoder {
    public static int blat = 30;
    public static int blon = 60;

    public static City locate(final double lat, final double lon) throws NoNearbyCityException, InvalidLatLonException {
        int bucketIndex = getBucketIndex(lat, lon);
        List<Integer> bucketCache = getBucketCache(bucketIndex);
        System.out.println(bucketCache);
        return findNearbyCity(lat, lon, bucketCache);
    }

    private static int getBucketIndex(final double lat, final double lon) {
        double blatDeg = 90 / blat;
        double blonDeg = 180 / blon;
        double alat = Math.abs(lat);
        double alon = Math.abs(lon);

        int m = (int) Math.floor(alat / blatDeg);
        int n = (int) Math.floor(alon / blonDeg);
        int qi = m*blon + n;

        int bpq = blat * blon;
        int quad = getQuad(lat, lon);
        int index = qi + quad * bpq;

        return index;
    }

    private static int getQuad(final double lat, final double lon) {
        if(lat >= 0) {
            if(lon >= 0)
                return 0;   // north east
            return 1;       // north west
        }
        if(lon >= 0)
            return 3;       // south east
        return 2;           // south west
    }

    private static List<Integer> getBucketCache(int bucketIndex) throws NoNearbyCityException, InvalidLatLonException {
        InputStream cacheStream = null;
        BufferedReader reader = null;
        List<Integer> bucketCache = null;

        try {
            cacheStream = OfflineGeocoder.class.getClassLoader().getResourceAsStream("cache");
            reader = new BufferedReader(new InputStreamReader(cacheStream));

            int current = 0;
            String line = "";
            while( (line = reader.readLine()) != null) {
                if(current == bucketIndex) {
                    bucketCache = parseCacheRow(line);
                    break;
                }
                current++;
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (cacheStream != null) {
                try {
                    cacheStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        if(bucketCache == null) {
            throw new InvalidLatLonException("BucketCache was null");
        }

        return bucketCache;
    }

    private static List<Integer> parseCacheRow(final String row) throws NoNearbyCityException {
        String delimiter = "\t";
        String[] rowArray = row.split(delimiter);
        String[] posArray = rowArray[1].split(",");

        if(posArray.length == 0)
            throw new NoNearbyCityException("No cached line positions for bucket: " + rowArray[0]);

        List<Integer> bucketCache = new ArrayList<Integer>();
        for(int i=0; i < posArray.length; i++) {
            Integer pos = Integer.parseInt(posArray[i]);
            bucketCache.add(pos);
        }
        return bucketCache;
    }

    private static City findNearbyCity(final double lat, final double lon, List<Integer> bucketCache) throws NoNearbyCityException {
        InputStream cityStream = null;
        BufferedReader reader = null;
        City nearestCity = null;

        try {
            cityStream = OfflineGeocoder.class.getClassLoader().getResourceAsStream("cities");
            reader = new BufferedReader(new InputStreamReader(cityStream));

            String currentLine      = "";
            int currentPos          = 0;
            int lookingForPos       = bucketCache.get(0);
            boolean inspecting      = false;
            int inspectingBucket    = -1;

            while((currentLine = reader.readLine()) != null) {
                if(currentPos == lookingForPos) {
                    inspecting = true;
                    String delimiter = "\t";
                    String[] cityRow = currentLine.split(delimiter);
                    inspectingBucket = Integer.parseInt(cityRow[0]);
                }
                if(inspecting) {
                    City currentCity = new City(currentLine, lat, lon);
                    if(currentCity.getBucket() != inspectingBucket) {
                        inspecting = false;
                        bucketCache.remove(0);
                        lookingForPos = bucketCache.get(0);
                    } else if(currentCity.isCloser(nearestCity)) {
                        nearestCity = currentCity;
                    }
                }
                currentPos++;
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (cityStream != null) {
                try {
                    cityStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        if(nearestCity == null) {
            throw new NoNearbyCityException("findNearbyCity() should not throw this");
        }

        return nearestCity;
    }
}
