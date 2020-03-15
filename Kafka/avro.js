var avroSchema = {
    name: 'MyAwesomeType',
    type: 'record',
    fields: [
        {
            name: 'id',
            type: 'string'
        }, {
            name: 'timestamp',
            type: 'double'
        }, {
            name: 'enumField',
            type: {
                name: 'EnumField',
                type: 'enum',
                symbols: ['sym1', 'sym2', 'sym3']
            }
        }]
};

var avro = require('avsc');
var type = avro.parse(avroSchema);