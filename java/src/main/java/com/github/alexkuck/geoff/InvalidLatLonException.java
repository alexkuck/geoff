package com.github.alexkuck.geoff;

public class InvalidLatLonException extends Exception {
    public InvalidLatLonException(String message) {
        super(message);
    }

    public InvalidLatLonException(String message, Throwable ex) {
        super(message, ex);
    }
}
