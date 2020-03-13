var request = require('request');
const https = require('https');
var apiKey = '2ac32a8f5926afc81899cdbbf83671db0f716ab387870379fa27929b9890474e';


var typeDescription = {
    name: 'FootballAPI',
    type: 'record',
    fields: [{
        name: 'GoalsHome',
        type: {
            name: 'GoalsHome',
            type: 'enum',
            symbols: ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H0', 'Hundefined']
        }
    },
    {
        name: 'GoalsAway',
        type: {
            name: 'GoalsAway',
            type: 'enum',
            symbols: ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H0', 'Hundefined']
        }
    },
    {
        name: "HomeTeam",
        type: 'string'
    },
    {
        name: "AwayTeam",
        type: 'string'
    }, {
        name: 'matchid',
        type: 'string'
    }, {
        name: 'timestamp',
        type: 'double'
    }]
};

var avro = require('avsc');
var type = avro.parse(typeDescription);





var messageBuffer;
var payload =[];

let data = '';
let ad = https.get('https://apifootball.com/api/?action=get_events&league_id=62&from=2019-04-06&to=2019-04-25&APIkey=' + apiKey, (resp) => {
    let data = '';

     //A chunk of data has been recieved.
    resp.on('data', (chunk) => {
        data += chunk;
    });

    // The whole response has been received. Print out the result.
    resp.on('end', () => {

        var kafka = require('kafka-node');
        var HighLevelProducer = kafka.HighLevelProducer;
        var KeyedMessage = kafka.KeyedMessage;
        var Client = kafka.Client;

        //console.log(Client)
        var client = new kafka.KafkaClient('localhost:2181', 'my-client-id', {
            sessionTimeout: 300,
            spinDelay: 100,
            retries: 2
        });

        //console.log(JSON.parse(data));
        //console.log(data[0])
        var d = JSON.parse(data);
        var i = 0

        for (i in d) {

            var kafka = require('kafka-node');
            var HighLevelProducer = kafka.HighLevelProducer;
            var KeyedMessage = kafka.KeyedMessage;
            var Client = kafka.Client;

            //console.log(Client)
            var client = new kafka.KafkaClient('localhost:2181', 'my-client-id', {
                sessionTimeout: 300,
                spinDelay: 100,
                retries: 2
            });

            // For this demo we just log client errors to the console.
            client.on('error', function (error) {
                console.error(error);
            });
            //console.log(d[0])


            var val = {
                GoalsHome: 'H' + 1,
                GoalsAway: 'H' + 2,
                HomeTeam: d[i].match_hometeam_name,
                AwayTeam: d[i].match_awayteam_name,
                matchid: d[i].match_id,
                timestamps: Date.now()
            };


            // Create message and encode to Avro buffer

            messageBuffer = type.toBuffer({
                GoalsHome: 'H' +1,// d[i].match_hometeam_score,
                GoalsAway: 'H' +2,// d[i].match_awayteam_score,
                HomeTeam: d[i].match_hometeam_name,
                AwayTeam: d[i].match_awayteam_name,
                matchid: d[i].match_id,
                timestamp: Date.now()
            });

            console.log(val)


            // Create a new payload
            payload[i] = {
                topic: 'football-kafka',
                messages: messageBuffer,
                attributes: 1 /* Use GZip compression for the payload */
            };

            
        }
        //Send payload to Kafka and log result/error
            var producer = new HighLevelProducer(client);
            //console.log(arr);
            producer.on('ready', function () {
                console.log("inside ready");
                producer.send(payload, function (error, result) {
                    console.info('Sent payload to Kafka: ', payload);
                    if (error) {
                        console.error(error);
                    } else {
                        var formattedResult = result;
                        console.log('result: ', result)
                    }
                });

            });

            // For this demo we just log producer errors to the console.
            producer.on('error', function (error) {
                console.error(error);
            });

    });

}).on("error", (err) => {
    console.log("Error: " + err.message);
});


