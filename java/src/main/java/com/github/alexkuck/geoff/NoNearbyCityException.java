package com.github.alexkuck.geoff;

public class NoNearbyCityException extends Exception {
    public NoNearbyCityException(String message) {
        super(message);
    }

    public NoNearbyCityException(String message, Throwable ex) {
        super(message, ex);
    }
}
