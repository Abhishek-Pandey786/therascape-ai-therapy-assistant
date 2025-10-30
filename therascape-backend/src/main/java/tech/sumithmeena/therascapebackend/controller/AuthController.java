package tech.sumithmeena.therascapebackend.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import tech.sumithmeena.therascapebackend.dto.LoginResponse;
import tech.sumithmeena.therascapebackend.dto.UserLoginRequest;
import tech.sumithmeena.therascapebackend.dto.UserRegistrationRequest;
import tech.sumithmeena.therascapebackend.dto.UserResponse;
import tech.sumithmeena.therascapebackend.service.UserService;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
@CrossOrigin(origins = "*") // For development only, restrict in production
public class AuthController {

    private final UserService userService;

    @PostMapping("/register")
    public ResponseEntity<?> registerUser(@RequestBody UserRegistrationRequest registrationRequest) {
        try {
            UserResponse userResponse = userService.registerUser(registrationRequest);
            return ResponseEntity.status(HttpStatus.CREATED).body(userResponse);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("An error occurred during registration: " + e.getMessage());
        }
    }

    @PostMapping("/login")
    public ResponseEntity<LoginResponse> loginUser(@RequestBody UserLoginRequest loginRequest) {
        // Basic validation
        if (loginRequest.getUsername() == null || loginRequest.getUsername().isEmpty() ||
            loginRequest.getPassword() == null || loginRequest.getPassword().isEmpty()) {
            LoginResponse errorResponse = new LoginResponse(false, "Username and password are required", null, null);
            return ResponseEntity.badRequest().body(errorResponse);
        }

        System.out.println("Login request received for user: " + loginRequest.getUsername());
        LoginResponse loginResponse = userService.loginUser(loginRequest);

        if (loginResponse.isSuccess()) {
            return ResponseEntity.ok(loginResponse);
        } else {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(loginResponse);
        }
    }

    @GetMapping("/check-username/{username}")
    public ResponseEntity<Boolean> checkUsernameExists(@PathVariable String username) {
        boolean exists = userService.existsByUsername(username);
        return ResponseEntity.ok(exists);
    }

    @GetMapping("/check-email/{email}")
    public ResponseEntity<Boolean> checkEmailExists(@PathVariable String email) {
        boolean exists = userService.existsByEmail(email);
        return ResponseEntity.ok(exists);
    }
}
