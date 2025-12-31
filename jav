package pl.ingenico.automation.client;

import io.restassured.http.ContentType;
import io.restassured.response.Response;
import pl.ingenico.automation.model.CreateUserRequest;

import static io.restassured.RestAssured.given;

/**
 * UserApiClient encapsulates all HTTP interactions related to user management.
 *
 * <p>This class acts as a dedicated API client (service layer) responsible
 * for sending requests and receiving responses from the user endpoints.</p>
 *
 * <p>Test classes should never call RestAssured directly.
 * Instead, they should rely on this client to improve readability,
 * maintainability, and reuse of API logic.</p>
 *
 * <p>This design follows common enterprise automation patterns
 * where API communication is separated from test assertions.</p>
 */
public class UserApiClient {

    /**
     * Sends a request to create a new user.
     *
     * @param request the request payload containing user details
     * @return the HTTP response returned by the API
     */
    public Response createUser(CreateUserRequest request) {
        return given()
                .contentType(ContentType.JSON)
                .body(request)
                .when()
                .post("/api/users");
    }

    /**
     * Retrieves details of an existing user by user ID.
     *
     * @param userId the identifier of the user
     * @return the HTTP response returned by the API
     */
    public Response getUser(int userId) {
        return given()
                .when()
                .get("/api/users/" + userId);
    }

    /**
     * Updates an existing user's details.
     *
     * @param userId  the identifier of the user to update
     * @param request the request payload with updated user data
     * @return the HTTP response returned by the API
     */
    public Response updateUser(int userId, CreateUserRequest request) {
        return given()
                .contentType(ContentType.JSON)
                .body(request)
                .when()
                .put("/api/users/" + userId);
    }

    /**
     * Deletes a user by user ID.
     *
     * @param userId the identifier of the user to delete
     * @return the HTTP response returned by the API
     */
    public Response deleteUser(int userId) {
        return given()
                .when()
                .delete("/api/users/" + userId);
    }
}




<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>pl.ingenico</groupId>
    <artifactId>ingenico-api-service-automation</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <java.version>17</java.version>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <restassured.version>5.4.0</restassured.version>
        <junit.version>5.10.1</junit.version>
    </properties>

    <dependencies>

        <!-- Rest Assured -->
        <dependency>
            <groupId>io.rest-assured</groupId>
            <artifactId>rest-assured</artifactId>
            <version>${restassured.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- JSON serialization -->
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.17.1</version>
        </dependency>

        <!-- JUnit 5 -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- AssertJ (korpo standard) -->
        <dependency>
            <groupId>org.assertj</groupId>
            <artifactId>assertj-core</artifactId>
            <version>3.25.3</version>
            <scope>test</scope>
        </dependency>

    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>
        </plugins>
    </build>

</project>





