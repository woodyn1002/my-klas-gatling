import com.typesafe.config.{Config, ConfigFactory}
import io.gatling.core.Predef._
import io.gatling.http.Predef._

class RegisterSimulation extends Simulation {

  val simConfig: Config = ConfigFactory.load("simulation.conf")

  val httpProtocol = http
    .baseUrl(simConfig.getString("baseUrl"))

  val scn = scenario("RegisterSimulation")
    .feed(csv("registrations.csv").queue)
    .foreach(session => session("lectureIds").as[String].split(" ").toSeq, "lectureId") {
      exec(http("register lectures")
        .post("/students/${studentId}/register")
        .body(StringBody("""{"lectureId":${lectureId}}""")).asJson
        .check(status.is(200)))
    }

  setUp(
    scn.inject(atOnceUsers(simConfig.getInt("register.numUsers")))
  ).protocols(httpProtocol)
}
