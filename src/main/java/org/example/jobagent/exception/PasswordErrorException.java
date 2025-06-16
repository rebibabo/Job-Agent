package org.example.jobagent.exception;

public class PasswordErrorException extends RuntimeException {
    public PasswordErrorException(String message) {
        super(message);
    }
}
