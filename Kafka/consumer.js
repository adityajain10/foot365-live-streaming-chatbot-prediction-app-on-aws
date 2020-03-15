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
            name: 'timestamps',
            type: 'double'
        }]
};
var exists;
var avro = require('avsc');
var type = avro.parse(typeDescription);
var AWS = require('aws-sdk');
AWS.config.update({

    region: "us-east-1",
    endpoint: "http://dynamodb.us-east-1.amazonaws.com"
});
var ddb = new AWS.DynamoDB.DocumentClient()

var kafka = require('kafka-node');
var HighLevelConsumer = kafka.HighLevelConsumer;
var Client = kafka.Client;

var client = new kafka.KafkaClient('localhost:2181');
var topics = [{
    topic: 'football-kafka'
}];

var options = {
    autoCommit: true,
    fetchMaxWaitMs: 1000,
    fetchMaxBytes: 1024 * 1024,
    encoding: 'buffer'
};
var consumer = new kafka.Consumer(client, topics, options);

consumer.on('message', function (message) {
    var buf = new Buffer(message.value, 'binary'); // Read string into a buffer.
    var decodedMessage = type.fromBuffer(buf.slice(0)); // Skip prefix.
    console.log(decodedMessage);
    const params = {
        TableName: "livescore",
        Key:
            {
                "matchid": decodedMessage.matchid
            }
    };
    exists = false
    const tem = ddb.get(params).promise()

    tem.then(function (result) {
        if (result.Item != undefined && result.Item != null) {
            exists = true;
        }

        if (exists) {
            console.log("Exists");
            var par = {
                TableName: "livescore",
                Key: {
                    "matchid": decodedMessage.matchid
                },
                UpdateExpression: "set GoalsHome = :gh, GoalsAway=:ga, timestamps=:ts",
                ConditionExpression: "matchid = :num",
                ExpressionAttributeValues: {
                    ":gh": decodedMessage.GoalsHome,
                    ":ga": decodedMessage.GoalsAway,
                    ":ts": decodedMessage.timestamps,
                    ":num": decodedMessage.matchid
                },
                ReturnValues: "UPDATED_NEW"
            };
            //console.log(par)
            console.log("Attempting a conditional update...");
            const r1 = ddb.update(par).promise()
            r1.then(function (data) {
                if (!data) {
                    console.error("Unable to update item. Error JSON:", JSON.stringify(data, null, 2));
                } else {
                    console.log("UpdateItem succeeded:", JSON.stringify(data, null, 2));
                }
            });
        } else {
            console.log("not exists");
            var row = {
                GoalsHome: decodedMessage.GoalsHome,
                GoalsAway: decodedMessage.GoalsAway,
                HomeTeam: decodedMessage.HomeTeam,
                AwayTeam: decodedMessage.AwayTeam,
                matchid: decodedMessage.matchid,
                timestamps: decodedMessage.timestamp
            }
            var par = {
                TableName: "livescore",
                Item: row
            }
            ddb.put(par, function (err, data) {
                console.log("inside")
                if (err) {
                    console.log("Unable to read item. Error JSON:", JSON.stringify(err, null, 2));

                } else {
                    console.log("PutItem succeeded:", JSON.stringify(data, null, 2));

                }
            });
        }
    });
});

consumer.on('error', function (err) {
    console.log('error', err);
});

process.on('SIGINT', function () {
    consumer.close(true, function () {
        process.exit();
    });
});


