package pl.ingenico.automation.model;

/**
 * UserResponse represents a response object returned by the user-related API endpoints.
 *
 * <p>This class is a Data Transfer Object (DTO) used to map JSON response data
 * into a Java object.</p>
 *
 * <p>It is primarily used in API tests to access response fields in a type-safe
 * and readable way, instead of relying directly on JSON path expressions.</p>
 *
 * <p>The fields of this class correspond to the attributes returned by the API
 * when a user is created or updated.</p>
 */
public class UserResponse {

    /**
     * Unique identifier of the user returned by the API.
     */
    private String id;

    /**
     * Name of the user.
     */
    private String name;

    /**
     * Job title or role assigned to the user.
     */
    private String job;

    /**
     * Timestamp indicating when the user was created.
     * This field is not always used directly in tests,
     * but is kept for completeness and future extensions.
     */
    private String createdAt;

    /**
     * Returns the unique identifier of the user.
     *
     * @return user id
     */
    public String getId() {
        return id;
    }

    /**
     * Returns the name of the user.
     *
     * @return user name
     */
    public String getName() {
        return name;
    }

    /**
     * Returns the user's job title or role.
     *
     * @return user job
     */
    public String getJob() {
        return job;
    }
}
