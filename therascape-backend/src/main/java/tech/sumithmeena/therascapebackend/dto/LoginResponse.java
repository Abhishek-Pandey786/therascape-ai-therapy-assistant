package tech.sumithmeena.therascapebackend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class LoginResponse {
    private boolean success;
    private String message;
    private UserResponse user;
    private String token;

    public LoginResponse(boolean success, String message, UserResponse user) {
        this.success = success;
        this.message = message;
        this.user = user;
        this.token = null;
    }
}
