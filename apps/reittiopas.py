from ti700.app import TerminalApp
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

import time
import logging
import requests

logger = logging.getLogger(__name__)

DEFAULT_STOP = "HSL:1432164"


class Reittiopas(TerminalApp):
    appname = "next bus / train from Reittiopas"

    _transport = RequestsHTTPTransport(
        url='https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql',
        use_json=True,
    )

    client = Client(transport=_transport, fetch_schema_from_transport=True,)

    def prompt(self, text=""):
        '''Sends a question waits for a response

        game.promt("What is your name? ")
        user then presses types a response and return key
        and this function returns that response

        CASE-SENSITIVE
        '''
        self.send(text, trailing_newline=False)
        response = self.read_line()
        return response

    def start(self):
        self.send("Welcome to Reittiopas")

        stop_id = self.prompt("\nPlease enter stop ID (feed:number, e.g., {0}): ".format(DEFAULT_STOP))
        if stop_id == '':
            stop_id = DEFAULT_STOP

#        query = gql("""
#        {
#          stop(id: "HSL:1432164") {
#            name
#            stoptimesWithoutPatterns {
#              scheduledArrival
#              realtimeArrival
#              arrivalDelay
#              scheduledDeparture
#              realtimeDeparture
#              departureDelay
#              realtime
#              realtimeState
#              serviceDay
#              headsign
#              trip {
#                route{
#                  shortName
#                }
#              }
#            }
#          }  
#        }
#        """)

        query = gql('query($stopId:String!) {stop(id: $stopId) {name stoptimesWithoutPatterns{ scheduledDeparture realtime headsign trip{ route{ shortName } } } } }')

        try:
            result = self.client.execute(query, variable_values={"stopId": stop_id})
            
            stop_name = result['stop']['name']
            transports = result['stop']['stoptimesWithoutPatterns']

            self.send("From stop {0}".format(stop_name))
            for transport in transports:
                self.send("Bus {0} is leaving for {1} at {2}".format(transport['trip']['route']['shortName'], transport['headsign'], time.strftime("%H:%M", time.gmtime(transport['scheduledDeparture']))))
        except requests.exceptions.HTTPError as http_error:
            self.send("Stop not found")
            logger.warn("Request failed with exception %s.", http_error)
        except Exception as exception:
            logger.warn("Request failed with exception %s.", exception, exc_info=True)


if __name__ == '__main__':
    from terminalconn import TerminalSerial
    ro = Reittiopas(TerminalSerial())

