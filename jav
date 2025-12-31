package pl.ingenico.automation.config;

import io.restassured.RestAssured;

import java.io.InputStream;
import java.util.Properties;

/**
 * TestConfig is responsible for initializing global test configuration.
 *
 * <p>This class loads test-related properties from the {@code application.properties}
 * file located in the test resources and applies them to the RestAssured configuration.</p>
 *
 * <p>Currently, it sets the {@code baseURI} used by RestAssured, so individual
 * test cases and API clients do not need to hardcode environment-specific values.</p>
 *
 * <p>The configuration is loaded once using a static initialization block,
 * ensuring that it is executed before any tests are run.</p>
 *
 * <p>This approach is commonly used in enterprise test automation frameworks
 * to centralize environment configuration (e.g. dev, test, staging).</p>
 */
public class TestConfig {

    /**
     * Static initialization block that is executed when the class is loaded.
     *
     * <p>It reads the {@code application.properties} file from the classpath,
     * loads all properties, and applies the base URL configuration
     * to RestAssured.</p>
     *
     * <p>If the configuration file cannot be loaded, the test execution
     * is stopped immediately by throwing a runtime exception.</p>
     */
    static {
        Properties properties = new Properties();
        try (InputStream is = TestConfig.class
                .getClassLoader()
                .getResourceAsStream("application.properties")) {

            properties.load(is);
            RestAssured.baseURI = properties.getProperty("base.url");

        } catch (Exception e) {
            throw new RuntimeException("Cannot load test configuration", e);
        }
    }

    /**
     * Triggers the static initialization of this class.
     *
     * <p>This method does not contain any logic by itself, but calling it
     * explicitly ensures that the static configuration block is executed.</p>
     *
     * <p>It is typically invoked in a {@code @BeforeAll} setup method
     * in test classes.</p>
     */
    public static void init() {
        // trigger static block
    }
}








package pl.ingenico.automation.model;

/**
 * CreateUserRequest represents the request payload used to create or update a user
 * via the API.
 *
 * <p>This class is a Data Transfer Object (DTO) that maps directly to the JSON
 * structure expected by the user-related endpoints.</p>
 *
 * <p>It is used by API client classes to serialize Java objects into JSON
 * when sending HTTP requests.</p>
 *
 * <p>Keeping request models separated from test logic improves readability,
 * reusability, and maintainability of the test automation framework.</p>
 */
public class CreateUserRequest {

    /**
     * The name of the user to be created or updated.
     */
    private String name;

    /**
     * The job title or role assigned to the user.
     */
    private String job;

    /**
     * Creates a new {@code CreateUserRequest} with the given user details.
     *
     * @param name the name of the user
     * @param job  the job title or role of the user
     */
    public CreateUserRequest(String name, String job) {
        this.name = name;
        this.job = job;
    }

    /**
     * Returns the user's name.
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





package pl.ingenico.automation.model;

/**
 * CreateUserRequest represents the request payload used to create or update a user
 * via the API.
 *
 * <p>This class is a Data Transfer Object (DTO) that maps directly to the JSON
 * structure expected by the user-related endpoints.</p>
 *
 * <p>It is used by API client classes to serialize Java objects into JSON
 * when sending HTTP requests.</p>
 *
 * <p>Keeping request models separated from test logic improves readability,
 * reusability, and maintainability of the test automation framework.</p>
 */
public class CreateUserRequest {

    /**
     * The name of the user to be created or updated.
     */
    private String name;

    /**
     * The job title or role assigned to the user.
     */
    private String job;

    /**
     * Creates a new {@code CreateUserRequest} with the given user details.
     *
     * @param name the name of the user
     * @param job  the job title or role of the user
     */
    public CreateUserRequest(String name, String job) {
        this.name = name;
        this.job = job;
    }

    /**
     * Returns the user's name.
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


package pl.ingenico.automation.tests;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import pl.ingenico.automation.client.UserApiClient;
import pl.ingenico.automation.config.TestConfig;
import pl.ingenico.automation.model.CreateUserRequest;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * UserCrudTest verifies the basic CRUD operations for user-related endpoints.
 *
 * <p>This test class demonstrates an end-to-end API test flow using
 * CREATE, READ, UPDATE, and DELETE operations.</p>
 *
 * <p>The test focuses on validating HTTP status codes and basic response behavior,
 * rather than internal API implementation details.</p>
 *
 * <p>All API interactions are delegated to {@link UserApiClient},
 * keeping test logic clean and readable.</p>
 */
public class UserCrudTest {

    private static UserApiClient userApiClient;

    /**
     * Initializes global test configuration and API client before any tests are executed.
     */
    @BeforeAll
    static void setup() {
        TestConfig.init();
        userApiClient = new UserApiClient();
    }

    /**
     * Executes a full CRUD flow for user management.
     *
     * <p>The test validates:
     * <ul>
     *     <li>User creation</li>
     *     <li>User retrieval</li>
     *     <li>User update</li>
     *     <li>User deletion</li>
     * </ul>
     *
     * <p>This test serves as a reference example for API automation
     * in an enterprise-style framework.</p>
     */
    @Test
    void shouldPerformUserCrudFlow() {

        // CREATE
        CreateUserRequest createRequest =
                new CreateUserRequest("Tomasz", "QA Engineer");

        var createResponse = userApiClient.createUser(createRequest);
        assertThat(createResponse.statusCode()).isEqualTo(201);

        String userId = createResponse.jsonPath().getString("id");
        assertThat(userId).isNotNull();

        // READ
        var getResponse = userApiClient.getUser(2);
        assertThat(getResponse.statusCode()).isEqualTo(200);

        // UPDATE
        CreateUserRequest updateRequest =
                new CreateUserRequest("Tomasz", "Senior QA Engineer");

        var updateResponse = userApiClient.updateUser(2, updateRequest);
        assertThat(updateResponse.statusCode()).isEqualTo(200);

        // DELETE
        var deleteResponse = userApiClient.deleteUser(2);
        assertThat(deleteResponse.statusCode()).isEqualTo(204);
    }
}




