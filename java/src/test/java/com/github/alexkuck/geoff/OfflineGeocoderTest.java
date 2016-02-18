import org.junit.Test;
import static org.junit.Assert.*;
import com.github.alexkuck.geoff.*;

public class OfflineGeocoderTest {

    @Test public void testWashDC() {
        int geonameId = 4140963;
        String cityName = "Washington, D.C.";
        double lat = 38.905740;
        double lon = -77.030361;

        try {
            City maybeCity = OfflineGeocoder.locate(38.905740, -77.030361);
            assertEquals("geonameId for " + cityName, maybeCity.getGeonameId(), geonameId);
        } catch (NoNearbyCityException e) {
            e.printStackTrace();
        } catch (InvalidLatLonException e) {
            e.printStackTrace();
        }
    }
}
