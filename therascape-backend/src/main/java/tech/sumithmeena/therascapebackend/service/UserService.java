package tech.sumithmeena.therascapebackend.service;

import tech.sumithmeena.therascapebackend.dto.LoginResponse;
import tech.sumithmeena.therascapebackend.dto.UserLoginRequest;
import tech.sumithmeena.therascapebackend.dto.UserRegistrationRequest;
import tech.sumithmeena.therascapebackend.dto.UserResponse;

public interface UserService {

    UserResponse registerUser(UserRegistrationRequest registrationRequest);

    LoginResponse loginUser(UserLoginRequest loginRequest);

    UserResponse getUserById(String id);

    UserResponse getUserByUsername(String username);

    boolean existsByUsername(String username);

    boolean existsByEmail(String email);
}
