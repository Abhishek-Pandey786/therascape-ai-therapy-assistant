package tech.sumithmeena.therascapebackend.service.impl;

import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import tech.sumithmeena.therascapebackend.dto.LoginResponse;
import tech.sumithmeena.therascapebackend.dto.UserLoginRequest;
import tech.sumithmeena.therascapebackend.dto.UserRegistrationRequest;
import tech.sumithmeena.therascapebackend.dto.UserResponse;
import tech.sumithmeena.therascapebackend.model.User;
import tech.sumithmeena.therascapebackend.repository.UserRepository;
import tech.sumithmeena.therascapebackend.security.JwtService;
import tech.sumithmeena.therascapebackend.service.UserService;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    @Override
    public UserResponse registerUser(UserRegistrationRequest registrationRequest) {
        // Auto-generate username from email if not provided
        String username = registrationRequest.getUsername();
        if (username == null || username.isEmpty()) {
            username = registrationRequest.getEmail().split("@")[0];
            registrationRequest.setUsername(username);
        }

        // Check if username or email already exists
        if (userRepository.existsByUsername(registrationRequest.getUsername())) {
            throw new IllegalArgumentException("Username already exists");
        }

        if (userRepository.existsByEmail(registrationRequest.getEmail())) {
            throw new IllegalArgumentException("Email already exists");
        }

        // Create new user
        User user = new User();
        user.setUsername(registrationRequest.getUsername());
        user.setPassword(passwordEncoder.encode(registrationRequest.getPassword())); // Password is now securely hashed
        user.setEmail(registrationRequest.getEmail());
        user.setFullName(registrationRequest.getFullName());
        user.setActive(true);

        User savedUser = userRepository.save(user);

        return mapToUserResponse(savedUser);
    }

    @Override
    public LoginResponse loginUser(UserLoginRequest loginRequest) {
        try {
            // Debug logging
            System.out.println("Login attempt for user: " + loginRequest.getUsername());

            // Basic validation
            if (loginRequest.getUsername() == null || loginRequest.getUsername().isEmpty() ||
                    loginRequest.getPassword() == null || loginRequest.getPassword().isEmpty()) {
                return new LoginResponse(false, "Username and password are required", null, null);
            }

            // Check if user exists in database by username or email
            User user = userRepository.findByUsername(loginRequest.getUsername())
                    .orElse(userRepository.findByEmail(loginRequest.getUsername())
                            .orElse(null));

            if (user == null) {
                System.out.println("User not found: " + loginRequest.getUsername());
                return new LoginResponse(false, "Invalid username or password", null, null);
            }

            System.out.println("Found user: " + user.getUsername() + ", Active: " + user.isActive());
            System.out.println("Stored password hash: " + user.getPassword());

            // Check if user is active
            if (!user.isActive()) {
                return new LoginResponse(false, "Account is inactive", null, null);
            }

            // Verify password manually using PasswordEncoder
            boolean passwordMatches = passwordEncoder.matches(loginRequest.getPassword(), user.getPassword());
            System.out.println("Password matches: " + passwordMatches);

            if (!passwordMatches) {
                return new LoginResponse(false, "Invalid username or password", null, null);
            }

            // Generate JWT token directly without Spring Security authentication
            // This avoids potential issues with the AuthenticationManager
            UserDetails userDetails = org.springframework.security.core.userdetails.User.builder()
                    .username(user.getUsername())
                    .password("") // Don't include the actual password in the token
                    .authorities("ROLE_USER")
                    .build();

            String jwt = jwtService.generateToken(userDetails);
            System.out.println("Generated JWT token for user: " + user.getUsername());

            // Create successful response
            UserResponse userResponse = mapToUserResponse(user);
            return new LoginResponse(true, "Login successful", userResponse, jwt);

        } catch (Exception e) {
            System.err.println("Login error: " + e.getMessage());
            e.printStackTrace();
            return new LoginResponse(false, "Authentication failed: " + e.getMessage(), null, null);
        }
    }

    @Override
    public UserResponse getUserById(String id) {
        return userRepository.findById(id)
                .map(this::mapToUserResponse)
                .orElseThrow(() -> new IllegalArgumentException("User not found with id: " + id));
    }

    @Override
    public UserResponse getUserByUsername(String username) {
        return userRepository.findByUsername(username)
                .map(this::mapToUserResponse)
                .orElseThrow(() -> new IllegalArgumentException("User not found with username: " + username));
    }

    @Override
    public boolean existsByUsername(String username) {
        return userRepository.existsByUsername(username);
    }

    @Override
    public boolean existsByEmail(String email) {
        return userRepository.existsByEmail(email);
    }

    private UserResponse mapToUserResponse(User user) {
        return new UserResponse(
                user.getId(),
                user.getUsername(),
                user.getEmail(),
                user.getFullName(),
                user.isActive());
    }
}
