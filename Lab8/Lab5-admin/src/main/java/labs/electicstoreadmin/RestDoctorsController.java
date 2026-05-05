package labs.electicstoreadmin;

import java.time.Instant;

import org.springframework.security.oauth2.client.ClientAuthorizationException;
import org.springframework.security.oauth2.client.OAuth2AuthorizeRequest;
import org.springframework.security.oauth2.client.OAuth2AuthorizedClient;
import org.springframework.security.oauth2.client.OAuth2AuthorizedClientManager;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;

import static org.springframework.security.oauth2.client.web.client.RequestAttributeClientRegistrationIdResolver.clientRegistrationId;

@RestController
public class RestDoctorsController {

    private final RestClient restClient;
    private final OAuth2AuthorizedClientManager authorizedClientManager;

    public RestDoctorsController(RestClient restClient, OAuth2AuthorizedClientManager authorizedClientManager) {
        this.restClient = restClient;
        this.authorizedClientManager = authorizedClientManager;
    }

    @GetMapping("/api/doctors")
    public String RestIngredientService() {
        return restClient.get()
                .uri("http://localhost:8080/api/doctors")
                .attributes(clientRegistrationId("admin-client"))
                .retrieve()
                .body(String.class);
    }


    @GetMapping("/token")
    public TokenResponse fetchToken() {
        try {
            OAuth2AuthorizedClient authorizedClient = authorizedClientManager
                    .authorize(OAuth2AuthorizeRequest.withClientRegistrationId("admin-client").principal("principal").build());

            if (authorizedClient == null || authorizedClient.getAccessToken() == null) {
                return new TokenResponse("Токен не получен", null, null, null, null, null, null, null);
            }

            return new TokenResponse(
                    authorizedClient.getAccessToken().getTokenValue(),
                    authorizedClient.getAccessToken().getExpiresAt(),
                    authorizedClient.getRefreshToken() != null ? authorizedClient.getRefreshToken().getTokenValue() : null,
                    authorizedClient.getRefreshToken() != null ? authorizedClient.getRefreshToken().getExpiresAt() : null,
                    authorizedClient.getClientRegistration().getRegistrationId(),
                    authorizedClient.getAccessToken().getTokenType().getValue(),
                    authorizedClient.getClientRegistration().getClientId(),
                    authorizedClient.getClientRegistration().getClientSecret()
            );
        } catch (ClientAuthorizationException e) {
            return new TokenResponse("Ошибка авторизации клиента: " + e.getMessage(), null, null, null, null, null, null, null);
        } catch (Exception e) {
            return new TokenResponse("Ошибка при получении токена: " + e.getMessage(), null, null, null, null, null, null, null);
        }
    }
}
